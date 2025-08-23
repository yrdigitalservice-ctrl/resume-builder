import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

st.set_page_config(page_title="Resume Builder", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>🚀 YR Digital Resume Builder</h1>
    <p style='text-align: center; color: #FAFAFA;'>Create a professional resume in minutes</p>
    """,
    unsafe_allow_html=True
)
st.write("---")

# -------- FORM ----------
with st.form("resume_form"):
    st.markdown("### 📌 Basic Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    st.markdown("### 🎯 Objective (optional)")
    objective = st.text_area("Write your career objective")

    st.markdown("### 📝 Professional Summary (optional)")
    summary = st.text_area("List key highlights (comma-separated)",
                           placeholder="e.g. 3+ years in IT recruitment, Skilled in stakeholder management")

    st.markdown("### 🧠 Skills (optional)")
    skills = st.text_area("Enter skills separated by commas", placeholder="Python, SQL, Communication")

    # ----- EXPERIENCE -----
    st.markdown("### 💼 Experience (optional)")
    exp_count = st.number_input("How many jobs do you want to add?", min_value=0, max_value=10, value=1)
    experience = []
    for i in range(exp_count):
        st.markdown(f"#### Job {i+1}")
        role = st.text_input(f"Role (Job {i+1})", key=f"role_{i}")
        company = st.text_input(f"Company (Job {i+1})", key=f"company_{i}")
        resp = st.text_area(f"Responsibilities (comma-separated) for Job {i+1}", key=f"resp_{i}")
        experience.append({
            "role": role,
            "company": company,
            "responsibilities": [r.strip() for r in resp.split(",")] if resp else []
        })

    # ----- EDUCATION -----
    st.markdown("### 🎓 Education (optional)")
    edu_count = st.number_input("How many education entries?", min_value=0, max_value=10, value=1)
    education = []
    for i in range(edu_count):
        st.markdown(f"#### Education {i+1}")
        degree = st.text_input(f"Degree (Education {i+1})", key=f"degree_{i}")
        inst = st.text_input(f"Institution (Education {i+1})", key=f"inst_{i}")
        year = st.text_input(f"Year (Education {i+1})", key=f"year_{i}")
        grade = st.text_input(f"Grade/Score (Education {i+1})", key=f"grade_{i}")
        if degree and inst:
            education.append([degree, inst, year, grade])

    # ----- CERTIFICATES -----
    st.markdown("### 📜 Certificates (optional)")
    cert_count = st.number_input("How many certificates do you want to add?", min_value=0, max_value=10, value=0)
    certificates = []
    for i in range(cert_count):
        cert = st.text_input(f"Certificate {i+1}", key=f"cert_{i}")
        if cert:
            certificates.append(cert)

    st.markdown("### 📎 Upload Certificate Images (optional)")
    uploaded_certs = st.file_uploader("Upload certificates (JPG/PNG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("Generate Resume")


# -------- PDF CREATION FUNCTION ----------
def create_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle("Title", fontSize=20, alignment=1, spaceAfter=8, textColor=colors.HexColor("#003366"), leading=22)
    section_style = ParagraphStyle("Section", fontSize=14, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#003366"))
    normal_style = ParagraphStyle("Normal", fontSize=11, leading=14)

    # ---- Header ----
    elements.append(Paragraph(f"<b>{data['name']}</b>", title_style))
    elements.append(Paragraph(f"{data['email']} | {data['phone']}", normal_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<hr width='100%'/>", normal_style))

    # ---- Objective ----
    if data.get("objective"):
        elements.append(Paragraph("Objective", section_style))
        elements.append(Paragraph(data["objective"], normal_style))
        elements.append(Spacer(1, 8))

    # ---- Professional Summary ----
    if data.get("summary"):
        elements.append(Paragraph("Professional Summary", section_style))
        for line in data["summary"]:
            elements.append(Paragraph(f"• {line}", normal_style))
        elements.append(Spacer(1, 8))

    # ---- Skills ----
    if data.get("skills"):
        elements.append(Paragraph("Skills", section_style))
        skills_text = " | ".join(data["skills"])
        elements.append(Paragraph(skills_text, normal_style))
        elements.append(Spacer(1, 8))

    # ---- Experience ----
    if data.get("experience"):
        elements.append(Paragraph("Experience", section_style))
        for job in data["experience"]:
            if job["role"] and job["company"]:
                elements.append(Paragraph(f"<b>{job['role']}</b> – {job['company']}", normal_style))
                for resp in job["responsibilities"]:
                    elements.append(Paragraph(f"• {resp}", normal_style))
                elements.append(Spacer(1, 6))
        elements.append(Spacer(1, 8))

    # ---- Education ----
    if data.get("education"):
        elements.append(Paragraph("Education", section_style))
        edu_data = [["Degree", "Institution", "Year", "Grade"]] + data["education"]
        table = Table(edu_data, hAlign="LEFT", colWidths=[120, 200, 60, 60])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#003366")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("FONTSIZE", (0,0), (-1,-1), 10),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 8))

    # ---- Certificates ----
    if data.get("certificates"):
        elements.append(Paragraph("Certificates", section_style))
        for cert in data["certificates"]:
            elements.append(Paragraph(f"• {cert}", normal_style))
        elements.append(Spacer(1, 8))

    # ---- Certificate Images ----
    if data.get("uploaded_certs"):
        elements.append(Paragraph("Certificate Images", section_style))
        for cert_file in data["uploaded_certs"]:
            try:
                img = Image(cert_file, width=350, height=250)
                elements.append(img)
                elements.append(Spacer(1, 10))
            except Exception as e:
                elements.append(Paragraph(f"(Could not load image: {e})", normal_style))

    doc.build(elements)


# -------- GENERATE PDF --------
if submitted:
    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "objective": objective,
        "summary": [s.strip() for s in summary.split(",")] if summary else [],
        "skills": [s.strip() for s in skills.split(",")] if skills else [],
        "experience": experience,
        "education": education,
        "certificates": certificates,
        "uploaded_certs": uploaded_certs
    }

    filename = f"{name.replace(' ', '_')}_Resume.pdf"
    create_pdf(resume_data, filename)

    with open(filename, "rb") as f:
        st.download_button("📥 Download Your Resume", f, file_name=filename)
