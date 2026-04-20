import pdfplumber
from skills import extract_skills

def extract_text_from_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


if __name__ == "__main__":
    file_path = "resume.pdf"

    resume_text = extract_text_from_pdf(file_path)

    detected_skills = extract_skills(resume_text)

    print("\nExtracted Resume Text:\n")
    
    for skill in detected_skills:
        print("-", skill)