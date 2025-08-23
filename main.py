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
    summary = st.text_area("List key highlights (comma-separated)", placeholder="e.g. 3+ years in IT recruitment, Skilled in stakeholder management")

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
    certificates = st.text_area("Enter certificates (comma-separated)", placeholder="Google Data Analytics, AWS Certified Cloud Practitioner")

    st.markdown("### 📎 Upload Certificate Images (optional)")
    uploaded_certs = st.file_uploader("Upload certificates (JPG/PNG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("Generate Resume")


# -------- PDF CREATION FUNCTION ----------
def create_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Header
    header_style = ParagraphStyle("Header", fontSize=18, alignment=1, spaceAfter=12, textColor=colors.HexColor("#FF4B4B"))
    elements.append(Paragraph(f"<b>{data['name']}</b>", header_style))
    contact_style = ParagraphStyle("Contact", fontSize=10, alignment=1, spaceAfter=20)
    elements.append(Paragraph(f"{data['email']} | {data['phone']}", contact_style))

    # Objective
    if data.get("objective"):
        elements.append(Paragraph("<b>Objective</b>", styles["Heading3"]))
        elements.append(Paragraph(data["objective"], styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Professional Summary
    if data.get("summary"):
        elements.append(Paragraph("<b>Professional Summary</b>", styles["Heading3"]))
        for line in data["summary"]:
            elements.append(Paragraph(f"• {line}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Skills
    if data.get("skills"):
        elements.append(Paragraph("<b>Skills</b>", styles["Heading3"]))
        elements.append(Paragraph(", ".join(data["skills"]), styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Experience
    if data.get("experience"):
        elements.append(Paragraph("<b>Experience</b>", styles["Heading3"]))
        for job in data["experience"]:
            if job["role"] and job["company"]:
                elements.append(Paragraph(f"<b>{job['role']} – {job['company']}</b>", styles["Normal"]))
                for resp in job["responsibilities"]:
                    elements.append(Paragraph(f"• {resp}", styles["Normal"]))
                elements.append(Spacer(1, 8))
        elements.append(Spacer(1, 12))

    # Education
    if data.get("education"):
        elements.append(Paragraph("<b>Education</b>", styles["Heading3"]))
        edu_data = [["Degree", "Institution", "Year", "Grade"]] + data["education"]
        table = Table(edu_data, hAlign="LEFT", colWidths=[120, 200, 60, 60])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("GRID", (0,0), (-1,-1), 0.5, colors.black),
            ("ALIGN", (0,0), (-1,-1), "CENTER")
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Certificates (Text List)
    if data.get("certificates"):
        elements.append(Paragraph("<b>Certificates</b>", styles["Heading3"]))
        for cert in data["certificates"]:
            elements.append(Paragraph(f"• {cert}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Certificates (Images)
    if data.get("uploaded_certs"):
        elements.append(Paragraph("<b>Certificates (Images)</b>", styles["Heading3"]))
        for cert_file in data["uploaded_certs"]:
            try:
                img = Image(cert_file, width=400, height=300)
                elements.append(img)
                elements.append(Spacer(1, 12))
            except Exception as e:
                elements.append(Paragraph(f"(Could not load image: {e})", styles["Normal"]))

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
        "certificates": [c.strip() for c in certificates.split(",")] if certificates else [],
        "uploaded_certs": uploaded_certs
    }

    filename = f"{name.replace(' ', '_')}_Resume.pdf"
    create_pdf(resume_data, filename)

    with open(filename, "rb") as f:
        st.download_button("📥 Download Your Resume", f, file_name=filename)
