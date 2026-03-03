import streamlit as st
from PIL import Image
import json
import tempfile
import os
from cvanalysis import *
import subprocess
import sys
subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], 
               capture_output=True)

st.title("📄 CV Analyzer")
st.write("ارفع صورة الـ CV وبنحلل كل شي!")

uploaded_file = st.file_uploader("ارفع CV", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # حفظ الصورة مؤقتاً عشان نقدر نمررها للـ functions
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

    # عرض النتائج
    st.subheader("👤 المعلومات الأساسية")
    st.write("**الاسم:**", data["name"])
    st.write("**الإيميل:**", data["email"])
    st.write("**الرقم:**", data["phone"])

    st.subheader("🛠️ المهارات")
    st.write(", ".join(data["skills"]) if data["skills"] else "مو موجود")

    st.subheader("🎓 التعليم")
    st.write("\n".join(data["education"]) if data["education"] else "مو موجود")

    st.subheader("💼 الخبرات")
    st.write("\n".join(data["experience"]) if data["experience"] else "مو موجود")

    st.subheader("🌍 اللغات")
    st.write("\n".join(data["languages"]) if data["languages"] else "مو موجود")

    st.subheader("📜 الشهادات")
    st.write("\n".join(data["certifications"]) if data["certifications"] else "مو موجود")

    os.unlink(tmp_path)