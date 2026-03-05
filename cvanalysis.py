import pytesseract
import cv2
import json
import spacy
import os
import numpy as np
from PIL import Image
import re
from groq import Groq
import streamlit as st
nlp=spacy.load("en_core_web_sm")

def extract_text_from_image(path_image):
  text=""
  images=Image.open(path_image)
  img_np=np.array(images)
  if len(img_np.shape)==3:
    gray =cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)
  else:
    gray=img_np

  sizeimage=cv2.resize(gray,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)

  denoised=cv2.fastNlMeansDenoising(sizeimage,h=10)
  clahe=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
  enhanced=clahe.apply(denoised)

  thresholds=cv2.threshold(enhanced,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
  config=r"--oem 3 --psm 6"
  replaceimagetopil=Image.fromarray(thresholds)
  text=pytesseract.image_to_string(replaceimagetopil,lang="eng", config=config)
  return text
def extract_email(text):
  print(text)
  pattern=r'[\w\s\.-]+@[\w\s\.-]+\.\w+'
  result= re.findall(pattern,text.lower())
  return result[0].replace(" ","").strip()


def extract_phone(text):
  pattern=r"\+?\d[\d\s\-]{7,}\d"
  return re.findall(pattern,text)
def extract_name(text):
  doc=nlp(text)
  for ent in doc.ents:
    if ent.label_=="PERSON":
      return ent.text.strip()
    

skills_keywords=["technical skills", "skills", "core competencies", "key skills", "skills and expertise", "skills summary", "skills set", "skills profile", "skills section", "skills overview", "skills highlights", "skills list", "skills and qualifications", "skills and experience"],
education_keywords=["education", "academic", "qualification","degree", "university", "school", "college", "master"],
experience_keywords=["experience", "employment", "work history", "professional experience", "career", "work experience","experience", "work", "job","employment"],
languages_keywords=["languages", "language skills", "language proficiency", "language abilities", "language knowledge", "language expertise", "language section", "language overview", "language highlights", "language list"],
certifications_keywords=["certifications", "certificates", "courses",'training and workshops','training','workshops'],
projects_keywords=["projects", "project experience", "relevant projects", "project work", "academic projects","wey projects","personal projects"]

def extract_skills(text):
    end_keywords=[wk for wk in experience_keywords + education_keywords + languages_keywords + certifications_keywords + projects_keywords]
    lines=text.split("\n")
    skills=[]
    in_section = False
        
    for line in lines:
            line_lower = line.lower().strip()
            if line_lower in skills_keywords:
                in_section = True
                continue
            if in_section and line_lower in end_keywords:
                break
            if in_section and line.strip():
                skills.append(line.strip())
    
        
    return skills 
def extract_education(text):
  end_keywords=[wk for wk in experience_keywords + education_keywords + languages_keywords + certifications_keywords + projects_keywords]
  lines=text.split("\n")
  education=[]
  in_section = False
    
  for line in lines:
        line_lower = line.lower().strip()
        if line_lower in education_keywords:
            in_section = True
            continue
        if in_section and line_lower in end_keywords:
            break
        if in_section and line.strip():
            education.append(line.strip())

    
  return education
def extract_experience(text):
    end_keywords = [wk for wk in skills_keywords + education_keywords + languages_keywords + certifications_keywords + projects_keywords]
    lines = text.split('\n')
    experience = []
    in_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in experience_keywords:
            in_section = True
            continue

        if in_section and line_lower in end_keywords:
            break
        if in_section and line.strip():
            experience.append(line.strip())
    return experience
def extract_projects(text):
    end_keywords = [wk for wk in skills_keywords + education_keywords + languages_keywords + certifications_keywords + experience_keywords]
    lines = text.split('\n')
    projects = []
    in_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in projects_keywords:
            in_section = True
            continue

        if in_section and line_lower in end_keywords:
            break
        if in_section and line.strip():
            projects.append(line.strip())
    return projects
def extract_languages(text):
    end_keywords = [wk for wk in skills_keywords + education_keywords + projects_keywords + certifications_keywords + experience_keywords]
    lines = text.split('\n')
    languages = []
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in languages_keywords:
            in_section = True
            continue
        if in_section and line_lower in end_keywords:
            break
        if in_section and line.strip():
            languages.append(line.strip())

    
    return languages
def extract_certifications(text):
    end_keywords = [wk for wk in skills_keywords + education_keywords + projects_keywords + languages_keywords + experience_keywords]
    lines = text.split('\n')
    certifications = []
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in certifications_keywords:
            in_section = True
            continue
        if in_section and line_lower in end_keywords:
            break
        if in_section and line.strip():
            certifications.append(line.strip())
    return certifications
def parse_cv_with_llm(text):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt=f"""
        Extract information from this CV text and return ONLY a JSON object with these exact fields:
        - name (string)
        - email (string)
        - phone (string, may contain numbers, spaces, +, -, ., commas)
        - skills (list of strings)
        - education (list of strings)
        - experience (list of strings)
        - projects (list of strings)
        - languages (list of strings)
        - certifications (list of strings)
        CV Text:
        {text}

        Return ONLY the JSON object, nothing else.
        """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )
    raw=response.choices[0].message.content.strip()
    raw=raw.replace("```json","").replace("```","").strip()
    try:
        return json.loads(raw)
    except Exception as e:
        st.error(f"Parse error: {e}")
        st.code(raw)  # عشان تشوف شو رجع الـ LLM
        return None