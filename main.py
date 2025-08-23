import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

st.set_page_config(page_title="Resume Builder", layout="centered")

# ---- HEADER ----
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>🚀 YR Digital Resume Builder</h1>
    <p style='text-align: center; color: #FAFAFA;'>Create a professional resume in minutes</p>
    """,
    unsafe_allow_html=True
)
st.write("---")

# ---- FORM ----
with st.form("resume_form"):
    st.markdown("### 📌 Basic Information")
    name = st.text_input("Full Name *", key="name")
    email = st.text_input("Email", key="email")
    phone = st.text_input("Phone", key="phone")
    address = st.text_input("Address (optional)", key="address")
    summary = st.text_area("Professional Headline / Summary (1–3 lines)", key="summary")

    st.write("---")
    st.markdown("### 🧠 Skills (optional)")
    skills = st.text_area("Add skills (comma separated)", key="skills")

    # ---- Education ----
    st.write("---")
    st.markdown("### 🎓 Education (optional)")
    edu_count = st.number_input("How many education entries?", min_value=0, max_value=10, value=1)
    education = []
    for i in range(edu_count):
        st.markdown(f"#### Education {i+1}")
        degree = st.text_input("Degree", key=f"degree_{i}")
        institution = st.text_input("Institution", key=f"inst_{i}")
        year = st.text_input("Year", key=f"year_{i}")
        grade = st.text_input("Grade/Score", key=f"grade_{i}")
        if degree and institution:
            education.append([degree, institution, year, grade])

    # ---- Experience ----
    st.write("---")
    st.markdown("### 💼 Experience (optional)")
    exp_count = st.number_input("How many job experiences?", min_value=0, max_value=10, value=1)
    experience = []
    for i in range(exp_count):
        st.markdown(f"#### Job {i+1}")
        job = st.text_input("Job Title", key=f"job_{i}")
        company = st.text_input("Company", key=f"company_{i}")
        years = st.text_input("Years", key=f"years_{i}")
        desc = st.text_area("Description", key=f"desc_{i}")
        if job and company:
            experience.append([job, company, years, desc])

    # ---- Certificates ----
    st.write("---")
    st.markdown("### 📜 Certificates (optional)")
    cert_count = st.number_input("How many certificates?", min_value=0, max_value=10, value=0)
    certificates = []
    for i in range(cert_count):
        cert = st.text_input(f"Certificate {i+1}", key=f"cert_{i}")
        if cert:
            certificates.append(cert)

    submitted = st.form_submit_button("📄 Generate Resume")

# ---- PDF CREATION ----
def create_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("Title", fontSize=20, alignment=1, spaceAfter=8, textColor=colors.HexColor("#003366"))
    section_style = ParagraphStyle("Section", fontSize=14, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#FF4B4B"))
    normal_style = ParagraphStyle("Normal", fontSize=11, leading=14)

    # Header
    story.append(Paragraph(f"<b>{data['name']}</b>", title_style))
    story.append(Paragraph(f"{data['email']} | {data['phone']} | {data['address']}", normal_style))
    story.append(Spacer(1, 8))

    if data.get("summary"):
        story.append(Paragraph("Summary", section_style))
        story.append(Paragraph(data["summary"], normal_style))
        story.append(Spacer(1, 8))

    if data.get("skills"):
        story.append(Paragraph("Skills", section_style))
        story.append(Paragraph(data["skills"], normal_style))
        story.append(Spacer(1, 8))

    if data.get("experience"):
        story.append(Paragraph("Experience", section_style))
        for job, company, years, desc in data["experience"]:
            story.append(Paragraph(f"<b>{job}</b> – {company} ({years})", normal_style))
            if desc:
                story.append(Paragraph(f"• {desc}", normal_style))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 8))

    if data.get("education"):
        story.append(Paragraph("Education", section_style))
        edu_data = [["Degree", "Institution", "Year", "Grade"]] + data["education"]
        table = Table(edu_data, hAlign="LEFT", colWidths=[120, 200, 60, 60])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#FF4B4B")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 10),
        ]))
        story.append(table)
        story.append(Spacer(1, 8))

    if data.get("certificates"):
        story.append(Paragraph("Certificates", section_style))
        for cert in data["certificates"]:
            story.append(Paragraph(f"• {cert}", normal_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---- DOWNLOAD BUTTON ----
if submitted:
    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "summary": summary,
        "skills": skills,
        "experience": experience,
        "education": education,
        "certificates": certificates
    }
    pdf_buffer = create_pdf(resume_data)
    st.download_button("⬇️ Download Your Resume", pdf_buffer, file_name=f"{name.replace(' ', '_')}_Resume.pdf", mime="application/pdf")
