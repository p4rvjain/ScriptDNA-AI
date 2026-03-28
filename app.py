from flask import Flask, request, jsonify, render_template, session, redirect
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pytesseract
from PIL import Image
import nltk
from nltk.tokenize import sent_tokenize
import cv2
import numpy as np
import random

nltk.download('punkt')
nltk.download('punkt_tab')

app = Flask(__name__)
app.secret_key = "scriptdna_secret"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load model
model_name = "roberta-base-openai-detector"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "dugtrio" and password:
            session["user"] = username
            return redirect("/home")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")


# -------- DETECTION --------
def detect_text(text):
    if not text.strip():
        return 0.0

    text = text[:512]

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    model_score = probs[0][1].item() * 100

    avg_word_len = sum(len(w) for w in text.split()) / max(len(text.split()), 1)
    sentence_count = len(sent_tokenize(text))
    punctuation_ratio = sum(1 for c in text if c in ",.!?") / max(len(text), 1)

    heuristic_score = 0

    if avg_word_len > 5:
        heuristic_score += 10
    if sentence_count > 5:
        heuristic_score += 10
    if punctuation_ratio < 0.02:
        heuristic_score += 10

    final_score = (0.7 * model_score) + (0.3 * heuristic_score)
    return round(min(final_score, 100), 2)


def analyze_sentences(text):
    sentences = sent_tokenize(text)
    results = []

    for s in sentences:
        score = detect_text(s)

        if score > 85:
            label = "AI"
        elif score > 60:
            label = "Mixed"
        else:
            label = "Human"

        results.append({
            "sentence": s,
            "score": score,
            "label": label
        })

    return results


# -------- SUGGESTIONS --------
def generate_suggestions(text):
    suggestions = []

    if len(text.split()) > 50:
        suggestions.append("Shorten sentences for a more natural tone.")

    if any(word in text.lower() for word in ["moreover", "furthermore", "thus"]):
        suggestions.append("Avoid overly formal connectors.")

    if text.lower().count("the") > 10:
        suggestions.append("Reduce repetition of common words.")

    if len(set(text.split())) / max(len(text.split()),1) < 0.5:
        suggestions.append("Increase vocabulary diversity.")

    if not suggestions:
        suggestions.append("Text already appears natural 👍")

    return suggestions


# -------- HUMANIZER --------
def humanize_text(text):
    replacements = {
        "moreover": "also",
        "furthermore": "plus",
        "thus": "so",
        "in conclusion": "to sum up",
        "however": "but"
    }

    words = text.split()
    new_words = []

    for w in words:
        lw = w.lower()
        if lw in replacements:
            new_words.append(replacements[lw])
        else:
            new_words.append(w)

    # random variation
    if len(new_words) > 10:
        new_words.insert(random.randint(0, len(new_words)-1), "actually")

    return " ".join(new_words)


# -------- API --------
@app.route("/detect", methods=["POST"])
def detect():
    data = request.json
    text = data.get("text", "")

    return jsonify({
        "overall_score": detect_text(text),
        "sentences": analyze_sentences(text),
        "suggestions": generate_suggestions(text)
    })


@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files["file"]

    image = Image.open(file.stream).convert("RGB")
    img = np.array(image)

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh, lang='eng')

    return jsonify({
        "extracted_text": text,
        "overall_score": detect_text(text),
        "sentences": analyze_sentences(text),
        "suggestions": generate_suggestions(text)
    })


@app.route("/humanize", methods=["POST"])
def humanize():
    data = request.json
    text = data.get("text", "")

    return jsonify({
        "humanized_text": humanize_text(text)
    })


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)