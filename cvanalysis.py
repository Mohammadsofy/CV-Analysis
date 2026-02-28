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
print(extract_text_from_image("image.png"))

def extract_email(text):
  print(text)
  pattern=r'[a-z0-9.-\ٍs]+\s?@\s?[\s\w.-]+\s?\.\s?+\w+'
  return re.findall(pattern,text)

print(extract_email(extract_text_from_image("image.png")))


def extract_phone(text):
  pattern=r"\+?\d[\d\s\-]{7,}\d"
  return re.findall(pattern,text)
print(extract_phone(extract_text_from_image("image.png")))

def extract_name(text):
  doc=nlp(text)
  for ent in doc.ents:
    if ent.label_=="PERSON":
      return ent.text
print(extract_name(extract_text_from_image("image.png")))


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
(extract_skills(extract_text_from_image("image.png")))

def storage_data_in_json(image_path):
  text=extract_text_from_image(image_path)
  extract_data={
      "name":extract_name(text),
      "email":extract_email(text),
      "phone":extract_phone(text),
      "skills":extract_skills(text)
  }
  name_without_ext = os.path.splitext(os.path.basename(image_path))[0]
  output_path = os.path.join("/content/json", name_without_ext + ".json")
  with open(output_path, "w", encoding="utf-8") as f:
        json.dump(extract_data, f, indent=2, ensure_ascii=False)
storage_data_in_json("image.png")