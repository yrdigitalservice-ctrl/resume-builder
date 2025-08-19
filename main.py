import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="YR Digital Resume Builder", page_icon="📄", layout="centered")
st.title("📄 YR Digital Resume Builder")
st.write("Create your professional resume in minutes 🚀")

# Styles for PDF
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Heading", fontSize=14, leading=16, spaceAfter=10, textColor=colors.HexColor("#2E86C1"), bold=True))
styles.add(ParagraphStyle(name="SubHeading", fontSize=12, leading=14, spaceAfter=6, textColor=colors.HexColor("#117A65"), bold=True))
styles.add(ParagraphStyle(name="Normal", fontSize=10, leading=12, spaceAfter=6))

# ---------------- FORM ----------------
st.title("📝 Resume Builder (Clients can skip sections)")

with st.form("resume_form"):
    st.subheader("👤 Basic Information")
    name = st.text_input("Full Name *")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address (Optional)")
    summary = st.text_area("Professional Summary (1–3 lines)")

    st.subheader("🧠 Skills")
    skills = st.text_area("List your skills (comma separated)")

    st.subheader("💼 Experience")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    exp_years = st.text_input("Years (e.g. 2021–2023)")
    exp_details = st.text_area("Work Details")

    st.subheader("🎓 Education")
    degree = st.text_input("Degree")
    school = st.text_input("School / University")
    edu_years = st.text_input("Years (e.g. 2018–2021)")

    st.subheader("📜 Certificates (Optional)")
    certificate = st.text_input("Certificate Name")
    cert_year = st.text_input("Year")

    submitted = st.form_submit_button("✅ Generate Resume")

# ---------------- PDF GENERATOR ----------------
if submitted:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    if name:
        elements.append(Paragraph(name, styles["Heading"]))
    if email or phone or address:
        contact_info = f"{email} | {phone} | {address}"
        elements.append(Paragraph(contact_info, styles["Normal"]))
    elements.append(Spacer(1, 12))

    if summary:
        elements.append(Paragraph("Professional Summary", styles["SubHeading"]))
        elements.append(Paragraph(summary, styles["Normal"]))
        elements.append(Spacer(1, 12))

    if skills:
        elements.append(Paragraph("Skills", styles["SubHeading"]))
        skill_list = ", ".join([s.strip() for s in skills.split(",")])
        elements.append(Paragraph(skill_list, styles["Normal"]))
        elements.append(Spacer(1, 12))

    if job_title and company:
        elements.append(Paragraph("Experience", styles["SubHeading"]))
        elements.append(Paragraph(f"{job_title} - {company} ({exp_years})", styles["Normal"]))
        if exp_details:
            elements.append(Paragraph(exp_details, styles["Normal"]))
        elements.append(Spacer(1, 12))

    if degree and school:
        elements.append(Paragraph("Education", styles["SubHeading"]))
        elements.append(Paragraph(f"{degree} - {school} ({edu_years})", styles["Normal"]))
        elements.append(Spacer(1, 12))

    if certificate:
        elements.append(Paragraph("Certificates", styles["SubHeading"]))
        elements.append(Paragraph(f"{certificate} ({cert_year})", styles["Normal"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    st.success("🎉 Resume Generated Successfully!")
    st.download_button("📥 Download PDF", data=pdf, file_name="resume.pdf", mime="application/pdf")
