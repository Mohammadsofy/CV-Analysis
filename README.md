# CV Analyzer 📄

A tool that extracts and analyzes information from CV image using OCR and NLP.

## 🔗 Live Demo
[👉 Try it here]
[https://cv-analysis-9tadmigdeuopqnshrpe3uv.streamlit.app/]

## ✨ Features
- Extracts text from CV images using OCR
- Identifies name, email, phone, skills, education, experience,project, languages, and certifications
- Two extraction modes: Rule-based and AI-powered (LLM)
- Shows missing skills to improve your chances

## 🔄 How It Works
1. Upload a CV screenshot
2. Choose extraction method:
   - 🔧 **Rule-based** — NLP + regex pattern matching (fast)
   - 🤖 **AI-powered** — LLM (Groq / LLaMA 3.3) for accurate extraction
3. Optionally paste a job description to get your match score

## 🛠️ Built With
- Python
- Tesseract OCR — text extraction from images
- OpenCV + Pillow — image processing
- spaCy — NLP and name extraction
- scikit-learn — TF-IDF and cosine similarity
- Groq / LLaMA 3.3 — AI-powered extraction
- Streamlit — web interface


## 📌 Status
Work in progress — tested on a limited number of CVs.
Next step: expand dataset testing and improve extraction accuracy.

