import subprocess
import sys
subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], 
               capture_output=True)
import streamlit as st
from PIL import Image
import json
import tempfile
import os
from cvanalysis import *


st.title("📄 CV Analyzer")
st.write("Upload your CV image and choose your preferred extraction method:")
st.markdown("""
- 🔧 **using rule-based** — Fast extraction using NLP and pattern matching
- 🤖 **using LLM** — Accurate extraction using Large Language Model
""")
uploaded_file = st.file_uploader("Upload CV", type=["png", "jpg", "jpeg"])
method=st.radio("Choose extraction method",
                 ("🤖using LLM", "🧠using rule-based"))
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.image(uploaded_file, caption="الـ CV", width=300)

    with st.spinner("جاري التحليل..."):
        text = extract_text_from_image(tmp_path)
        if method =="🤖using LLM":
            data=parse_cv_with_llm(text)
            if not data:
                st.error("AI analysis failed, try a clearer image")
                st.stop()
        else:
            data = {
                "name": extract_name(text),
                "email": extract_email(text),
                "phone": extract_phone(text),
                "skills": extract_skills(text),
                "education": extract_education(text),
                "experience": extract_experience(text),
                "languages": extract_languages(text),
                "certifications": extract_certifications(text)
            }

    st.subheader("👤 Basic information")
    col1, col2,col3 = st.columns(3)
    with col1:
        st.markdown(f"**Name:**")
        st.markdown(f"<span style='color:#4CAF50; font-size:18px'>{data['name']}</span>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"**Email:** ")
        st.markdown(f"<span style='color:#4CAF50; font-size:18px'>{data['email']}</span>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"**Phone:** ")
    phone = data['phone'] if isinstance(data['phone'], str) else (data['phone'][0] if data['phone'] else 'Not found')
    st.markdown(f"<span style='color:#4CAF50; font-size:18px'>{phone}</span>", unsafe_allow_html=True)
    st.subheader("🛠️ Skills")
    if data["skills"]:
        skills_html = " ".join([
            f'<span style="background:#4CAF50; color:white; padding:4px 12px; border-radius:12px; margin:3px; display:inline-block">{s}</span>'
            for s in data["skills"]
        ])
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.write("Not found")

    # باقي الأقسام
    for section, emoji, title in [
        ("education", "🎓", "Education"),
        ("experience", "💼", "Experience"),
        ("languages", "🌍", "Languages"),
        ("certifications", "📜", "Certifications")
    ]:
        st.subheader(f"{emoji} {title}")
        if data[section]:
            for item in data[section]:
                st.markdown(f"• {item}")
        else:
            st.write("Not found")
    os.unlink(tmp_path)