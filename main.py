import streamlit as st
import os
from PIL import Image
import pdfplumber
import pytesseract
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() 
api_key = os.getenv('YOUR_API_KEY')
tess_path = os.getenv("Path")

pytesseract.pytesseract.tesseract_cmd = tess_path

def image_to_text(image_file):
    image = Image.open(image_file)
    text = pytesseract.image_to_string(image)
    return text

def pdf_to_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""  
    return text


def generate_quiz_from_text(text):
    st.write("Generating quiz from the extracted text...")

    genai.configure(api_key=api_key)
    
    prompt = f"Make a 10 MCQ type of quiz with options on new line. If two or more files, divide the number of questions accordingly. For a single text, generate 10 questions(do not show answer key): {text}"
    
    model = genai.GenerativeModel('gemini-pro')
    res = model.generate_content(prompt)
    
    return res.text

def main():
    st.title("Quiz Generation App")
    
    st.write("Upload images or PDFs, and a quiz will be generated based on the extracted text.")

    uploaded_files = st.file_uploader("Upload Images or PDFs", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    
    combined_text = ""

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type
            
            if file_type in ["image/png", "image/jpeg", "image/jpg"]:
                st.write(f"Processing image: {uploaded_file.name}...")
                image_text = image_to_text(uploaded_file)
                combined_text += image_text + "\n\n"
            
            elif file_type == "application/pdf":
                st.write(f"Processing PDF: {uploaded_file.name}...")
                pdf_text = pdf_to_text(uploaded_file)
                combined_text += pdf_text + "\n\n"
    
    if combined_text:
        if st.button("Generate Quiz"):
            quiz_content = generate_quiz_from_text(combined_text)
            st.write("Generated Quiz:")
            st.write(quiz_content)
    else:
        st.write("Please upload valid images or PDF files to extract text.")

if __name__ == '__main__':
    main()
