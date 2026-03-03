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
st.write("Upload a screenshot of your CV to extract information such as name, email, phone number, skills, education, experience, languages, and certifications.")

uploaded_file = st.file_uploader("Upload CV", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.image(uploaded_file, caption="الـ CV", width=300)

    with st.spinner("جاري التحليل..."):
        text = extract_text_from_image(tmp_path)
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

    st.subheader("👤 information")
    st.write("**name:** ", data["name"])
    st.write("**email:** ", data["email"])
    st.write("**phone:** ", data["phone"][0] if data["phone"] else "مو موجود")

    st.subheader("🛠️ skills")
    st.write("\n".join(data["skills"]) if data["skills"] else "مو موجود")

    st.subheader("🎓 education")
    for edu in data["education"]:
        st.markdown(f"• {edu}")
    st.subheader("💼 experience")
    for exp in data["experience"]:
        st.markdown(f"• {exp}")
    st.subheader("🌍 languages")
    for lang in data["languages"]:
        st.markdown(f"• {lang}")
    st.subheader("📜 certifications")
    for cert in data["certifications"]:
        st.markdown(f"• {cert}")
    os.unlink(tmp_path)