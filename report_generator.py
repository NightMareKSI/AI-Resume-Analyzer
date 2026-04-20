from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(semantic_score, skill_score, overall_score, resume_skills, missing_skills, recommendations):
    file_name = "resume_analysis_report.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)

    y = 750

    c.drawString(50, y, "Resume Analysis Report")
    y -= 40
    c.drawString(50, y, f"Semantic Match Score: {semantic_score}%")
    y -= 20
    c.drawString(50, y, f"Skill Match Score: {skill_score}%")
    y -= 20
    c.drawString(50, y, f"Overall ATS Score: {overall_score}%")
    y -= 40
    c.drawString(50, y, "Your Skills:")
    y -= 20

    for skill in resume_skills:
        c.drawString(70, y, f"- {skill}")
        y -= 15
    y -= 20
    c.drawString(50, y, "Missing Skills:")
    y -= 20

    for skill in missing_skills:
        c.drawString(70, y, f"- {skill}")
        y -= 15
    y -= 20
    c.drawString(50, y, "Recommended Skills:")
    y -= 20

    for skill, desc in recommendations.items():
        c.drawString(70, y, f"{skill} - {desc}")
        y -= 15
    c.save()

    return file_name
    