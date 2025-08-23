import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

# ----- PAGE CONFIG -----
st.set_page_config(page_title="AI Resume Builder", page_icon="📝", layout="centered")

# ----- HEADER -----
st.title("📝 YR Digital Resume Builder")
st.markdown("Create your professional resume in minutes 🚀")

# ----- BASIC INFO -----
st.header("👤 Basic Information")
full_name = st.text_input("Full Name *")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address (optional)")
summary = st.text_area("Professional Summary (1-3 lines)")

# ----- SKILLS -----
st.header("🧠 Skills")
skills = st.text_area("Enter your skills (comma separated)")

# ----- EXPERIENCE -----
st.header("💼 Experience (optional)")
exp_count = st.number_input("How many job experiences?", min_value=0, max_value=10, value=0)

experience = []
for i in range(exp_count):
    st.subheader(f"Experience {i+1}")
    job_title = st.text_input(f"Job Title (Experience {i+1})", key=f"job_{i}")
    company = st.text_input(f"Company (Experience {i+1})", key=f"company_{i}")
    years = st.text_input(f"Years (Experience {i+1})", key=f"years_{i}")
    desc = st.text_area(f"Description (Experience {i+1})", key=f"desc_{i}")
    if job_title and company:
        experience.append([job_title, company, years, desc])

# ----- EDUCATION -----
st.header("🎓 Education (optional)")
edu_count = st.number_input("How many education entries?", min_value=0, max_value=10, value=0)

education = []
for i in range(edu_count):
    st.subheader(f"Education {i+1}")
    degree = st.text_input(f"Degree (Education {i+1})", key=f"degree_{i}")
    inst = st.text_input(f"Institution (Education {i+1})", key=f"inst_{i}")
    year = st.text_input(f"Year (Education {i+1})", key=f"year_{i}")
    grade = st.text_input(f"Grade/Score (Education {i+1})", key=f"grade_{i}")
    if degree and inst:
        education.append([degree, inst, year, grade])

# ----- CERTIFICATES -----
st.header("📜 Certificates (optional)")
cert_count = st.number_input("How many certificates?", min_value=0, max_value=10, value=0)

certificates = []
for i in range(cert_count):
    cert = st.text_input(f"Certificate {i+1}", key=f"cert_{i}")
    if cert:
        certificates.append(cert)

# ----- PDF GENERATION -----
if st.button("📄 Generate PDF Resume"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>{full_name}</b>", styles['Title']))
    story.append(Paragraph(email, styles['Normal']))
    story.append(Paragraph(phone, styles['Normal']))
    story.append(Paragraph(address, styles['Normal']))
    story.append(Spacer(1, 12))

    if summary:
        story.append(Paragraph("<b>Summary</b>", styles['Heading2']))
        story.append(Paragraph(summary, styles['Normal']))
        story.append(Spacer(1, 12))

    if skills:
        story.append(Paragraph("<b>Skills</b>", styles['Heading2']))
        story.append(Paragraph(skills, styles['Normal']))
        story.append(Spacer(1, 12))

    if experience:
        story.append(Paragraph("<b>Experience</b>", styles['Heading2']))
        for job_title, company, years, desc in experience:
            story.append(Paragraph(f"{job_title} - {company} ({years})", styles['Normal']))
            if desc:
                story.append(Paragraph(desc, styles['Normal']))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 12))

    if education:
        story.append(Paragraph("<b>Education</b>", styles['Heading2']))
        for degree, inst, year, grade in education:
            story.append(Paragraph(f"{degree} - {inst} ({year}) {grade}", styles['Normal']))
        story.append(Spacer(1, 12))

    if certificates:
        story.append(Paragraph("<b>Certificates</b>", styles['Heading2']))
        for cert in certificates:
            story.append(Paragraph(cert, styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    st.download_button("⬇️ Download Resume", buffer, file_name="resume.pdf", mime="application/pdf")
