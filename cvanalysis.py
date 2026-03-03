import pytesseract
import cv2
import json
import spacy
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re
nlp=spacy.load("en_core_web_sm")

def extract_text_from_image(path_image):
  text=""
  images=Image.open(path_image)
  img_np=np.array(images)
  gray =cv2.cvtColor(img_np,cv2.COLOR_BGR2GRAY)

  sizeimage=cv2.resize(gray,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)

  lessnoise=cv2.GaussianBlur(sizeimage,(3,3),0)

  thresholds=cv2.threshold(lessnoise,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

  replaceimagetopil=Image.fromarray(thresholds)
  text=pytesseract.image_to_string(replaceimagetopil,lang="eng")
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
def extract_skills(text):
    skills_list = [
        # Programming
        "python", "sql", "java", "javascript", "r", "c++",
        # Data Science
        "machine learning", "deep learning", "nlp", "computer vision",
        "data analysis", "data visualization", "statistics",
        # Libraries
        "pandas", "numpy", "sklearn", "tensorflow", "pytorch",
        "matplotlib", "seaborn", "plotly",
        # Tools
        "power bi", "tableau", "excel", "git", "github",
        "jupyter", "colab", "streamlit",
        # Other
        "communication", "teamwork", "problem solving"
    ]
    text_lower=text.lower()
    found_skills=[]
    for skill in skills_list:
      if skill in text_lower:
         found_skills.append(skill) 
    return found_skills     
def extract_education(text):
  keywords=['education','academic','degree','university','school','college','master']
  lines=text.split("\n")
  education=[]
  in_section = False
    
  for line in lines:
        line_lower = line.lower().strip()
        if line_lower in keywords:
            in_section = True
            continue
        if in_section and line_lower in ["work experience","experience", "projects", "skills", "languages"]:
            break
        if in_section and line.strip():
            education.append(line.strip())

    
  return education
def extract_experience(text):
    keywords = ['projects','work experience', 'experience', 'work', 'job','employment']
    lines = text.split('\n')
    experience = []
    in_section = False
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in keywords:
            in_section = True
            continue

        if in_section and line_lower in ['progect','skills','education','technical skills','languages','Training and Workshops','Training','Workshops']:
            break
        if in_section and line.strip():
            experience.append(line.strip())
    return experience
def extract_languages(text):
    keywords = ["languages", "language skills"]
    lines = text.split('\n')
    languages = []
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in keywords:
            in_section = True
            continue
        if in_section and line_lower in ["education", "experience", "projects", "certifications",'training and workshops','training','workshops']:
            break
        if in_section and line.strip():
            languages.append(line.strip())

    
    return languages
def extract_certifications(text):
    keywords = ["certifications", "certificates", "courses",'training and workshops','training','workshops']
    lines = text.split('\n')
    certifications = []
    in_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower in keywords:
            in_section = True
            continue
        if in_section and line_lower in ["education", "experience", "projects", "languages"]:
            break
        if in_section and line.strip():
            certifications.append(line.strip())
    return certifications
# def storage_data_in_json(image_path):
#   text=extract_text_from_image(image_path)
#   extract_data={
#       "name":extract_name(text),
#       "email":extract_email(text),
#       "phone":extract_phone(text),
#       "skills":extract_skills(text),
#       "education":extract_education(text),
#       "experience":extract_experience(text),
#       "languages":extract_languages(text),
#       "certifications":extract_certifications(text)
#   }
#   name_without_ext = os.path.splitext(os.path.basename(image_path))[0]
#   json_dir = "/content/json"
#   os.makedirs(json_dir, exist_ok=True)
#   output_path = os.path.join(json_dir, name_without_ext + ".json")
#   with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(extract_data, f, indent=2, ensure_ascii=False)
# storage_data_in_json("image.png")