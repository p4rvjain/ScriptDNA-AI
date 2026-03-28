# ScriptDNA AI

ScriptDNA AI is an intelligent web-based system that detects whether a given text is AI-generated or human-written. It combines machine learning, OCR, and heuristic analysis to provide probability scores, sentence-level insights, and improvement suggestions.

---

## Problem Statement

GhostWriter Detector: AI vs Student Authorship Engine  

Background: With widespread use of LLMs, educators struggle to determine whether submissions reflect genuine student understanding or AI-generated content.  

Challenge: Design a system that analyzes writing style evolution, keystroke dynamics, and contextual reasoning patterns to estimate authorship authenticity.

---

## Features

AI vs Human Detection  
Uses a pretrained NLP model to classify text  
Provides an overall AI probability score  

Sentence-Level Analysis  
Highlights sentences as AI-generated, mixed, or human-written  

OCR Support  
Upload images and extract text for analysis  

Smart Suggestions  
Provides feedback to make AI text more natural  

AI Humanizer  
Rewrites text to improve readability and human-like flow  

Login System  
Simple authentication for controlled access  

Modern UI  
Dark themed, tech-inspired interface with smooth layout  

---

## Project Structure

```
scriptdna-ai/
│
├── app.py
├── templates/
│ ├── login.html
│ └── index.html
├── static/
│ └── style.css
├── README.md
```


---

## Installation & Requirements

Ensure Python is installed on your system.

Install required dependencies:

pip install flask transformers torch pytesseract opencv-python nltk pillow

Install Tesseract OCR from:
https://github.com/tesseract-ocr/tesseract

Then set the path in app.py:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

---

## Running the Project

### 1. Clone the repository
Run:
git clone https://github.com/your-username/scriptdna-ai.git  
cd scriptdna-ai  

### 2. Create virtual environment
Run:
python -m venv venv  
venv\Scripts\activate  

### 3. Install dependencies
Run:
pip install flask transformers torch pytesseract opencv-python nltk pillow  

### 4. Start the application
Run:
python app.py  

Open in browser:
http://127.0.0.1:5000  

---

## Login Credentials

Username: dugtrio  
Password: anything  

---

## How It Works

User enters text or uploads image  
OCR extracts text if needed  
NLP model predicts AI probability  
Heuristic rules refine results  
Sentence-level classification is performed  
Suggestions and rewritten output are generated  

---

## Disclaimer

AI detection is probabilistic and not always fully accurate. Results may vary.

---

## Future Improvements

Fine-tuned custom detection model  
Real-time typing analysis  
Advanced paraphrasing system  
User dashboard and analytics  
API deployment  

---

## Authors

Parv Jain, Nikshit, Vriti Chaturvedi

Built for hackathon by Randomize();
