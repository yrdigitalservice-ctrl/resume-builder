import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="centered")

# ---------- Helpers ----------
def init_state():
    ss = st.session_state
    ss.setdefault("educations", [])   # list of dicts
    ss.setdefault("experiences", [])  # list of dicts
    ss.setdefault("certificates", []) # list of strings
    ss.setdefault("skills", [])       # list of strings

init_state()

def add_skill(skill):
    if skill and skill.strip():
        st.session_state.skills.append(skill.strip())

def add_certificate(cert):
    if cert and cert.strip():
        st.session_state.certificates.append(cert.strip())

def add_education(degree, school, board, year, grade):
    st.session_state.educations.append({
        "degree": degree.strip(),
        "school": school.strip(),
        "board": board.strip(),
        "year": year.strip(),
        "grade": grade.strip()
    })

def add_experience(company, client, role, domain, duration, team_size, responsibilities_text):
    # responsibilities as bullet list, split by newlines
    bullets = [x.strip("•- ").strip() for x in responsibilities_text.split("\n") if x.strip()]
    st.session_state.experiences.append({
        "company": company.strip(),
        "client": client.strip(),
        "role": role.strip(),
        "domain": domain.strip(),
        "duration": duration.strip(),
        "team_size": team_size.strip(),
        "responsibilities": bullets
    })

def build_pdf(fullname, email, phone, address, headline, include_sections):
    """
    include_sections is a dict like:
    {"summary": True, "education": True, "experience": True, "skills": True, "certs": True}
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=36, leftMargin=36, topMargin=42, bottomMargin=36)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Heading", fontSize=14, leading=16, spaceAfter=6, textColor=colors.HexColor("#1f4e79"), underlineWidth=0.4))
    styles.add(ParagraphStyle(name="Small", fontSize=9, leading=12))
    styles.add(ParagraphStyle(name="Label", fontSize=10, leading=12, textColor=colors.HexColor("#444444")))
    styles.add(ParagraphStyle(name="Body", fontSize=10, leading=14))

    story = []

    # Header
    story.append(Paragraph(f"<b>{fullname}</b>", styles["Title"]))
    contact_line = " • ".join([x for x in [email, phone, address] if x])
    if contact_line:
        story.append(Paragraph(contact_line, styles["Small"]))
    if headline:
        story.append(Paragraph(headline, styles["Body"]))
    story.append(Spacer(1, 12))

    # Summary (optional - we just print the headline again as a brief)
    if include_sections.get("summary") and headline:
        story.append(Paragraph("Professional Summary", styles["Heading"]))
        story.append(Paragraph(headline, styles["Body"]))
        story.append(Spacer(1, 8))

    # Skills
    if include_sections.get("skills") and st.session_state.skills:
        story.append(Paragraph("Skills", styles["Heading"]))
        skills_line = ", ".join(st.session_state.skills)
        story.append(Paragraph(skills_line, styles["Body"]))
        story.append(Spacer(1, 8))

    # Education Table
    if include_sections.get("education") and st.session_state.educations:
        story.append(Paragraph("Educational Qualifications", styles["Heading"]))
        data = [["Education", "College/School", "University/Board", "Year Passed", "Percentage/Grade"]]
        for e in st.session_state.educations:
            data.append([e["degree"], e["school"], e["board"], e["year"], e["grade"]])
        tbl = Table(data, colWidths=[110, 140, 140, 80, 100])
        tbl.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.4, colors.grey),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0f3f6")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.black),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("ALIGN", (3,1), (4,-1), "CENTER"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 8))

    # Experience (each as a mini-table + bullets)
    if include_sections.get("experience") and st.session_state.experiences:
        story.append(Paragraph("Professional Experience", styles["Heading"]))
        for exp in st.session_state.experiences:
            meta = [
                ["Company", exp["company"]],
                ["Client", exp["client"]],
                ["Role", exp["role"]],
                ["Domain", exp["domain"]],
                ["Duration", exp["duration"]],
                ["Team Size", exp["team_size"]],
            ]
            mt = Table(meta, colWidths=[80, 430])
            mt.setStyle(TableStyle([
                ("GRID", (0,0), (-1,-1), 0.25, colors.lightgrey),
                ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f7f7f7")),
                ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
                ("FONTSIZE", (0,0), (-1,-1), 9),
            ]))
            story.append(mt)
            if exp["responsibilities"]:
                story.append(Spacer(1, 4))
                story.append(Paragraph("<b>Responsibilities:</b>", styles["Label"]))
                items = [ListItem(Paragraph(r, styles["Body"]), leftIndent=8) for r in exp["responsibilities"]]
                story.append(ListFlowable(items, bulletType="bullet", start="•", bulletFontName="Helvetica", bulletFontSize=9))
            story.append(Spacer(1, 8))

    # Certificates
    if include_sections.get("certs") and st.session_state.certificates:
        story.append(Paragraph("Certificates", styles["Heading"]))
        items = [ListItem(Paragraph(c, styles["Body"]), leftIndent=8) for c in st.session_state.certificates]
        story.append(ListFlowable(items, bulletType="bullet", start="•", bulletFontName="Helvetica", bulletFontSize=9))
        story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------- UI ----------
st.title("📄 Resume Builder (Clients can skip sections)")

with st.expander("👤 Basic Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        fullname = st.text_input("Full Name *")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
    with col2:
        address = st.text_input("Address (optional)")
        headline = st.text_area("Professional Headline / Summary (1–3 lines)", height=80,
                                placeholder="Example: Technical Recruiter with 3+ years in IT hiring across Java, Cloud, and Data roles.")

with st.expander("🧠 Skills", expanded=True):
    skill = st.text_input("Add a skill")
    add = st.button("➕ Add Skill")
    if add:
        add_skill(skill)
        st.experimental_rerun()
    if st.session_state.skills:
        st.write("Current skills:")
        st.write(", ".join(st.session_state.skills))
        if st.button("Clear skills"):
            st.session_state.skills = []
            st.experimental_rerun()

with st.expander("🎓 Education"):
    with st.form("edu_form", clear_on_submit=True):
        deg = st.text_input("Education / Degree (e.g., MBA, BA, 12th Class)")
        sch = st.text_input("College/School")
        brd = st.text_input("University/Board")
        yr  = st.text_input("Year Passed")
        grd = st.text_input("Percentage/Grade")
        s = st.form_submit_button("➕ Add Education Row")
        if s:
            if deg and sch:
                add_education(deg, sch, brd, yr, grd)
                st.success("Added!")
            else:
                st.warning("Degree and College/School are required.")
    if st.session_state.educations:
        st.table([{ "Education": e["degree"], "College/School": e["school"], "University/Board": e["board"], "Year": e["year"], "Grade": e["grade"] } for e in st.session_state.educations])
        if st.button("Clear education"):
            st.session_state.educations = []
            st.experimental_rerun()

with st.expander("💼 Experience"):
    with st.form("exp_form", clear_on_submit=True):
        colA, colB = st.columns(2)
        with colA:
            company = st.text_input("Company")
            client  = st.text_input("Client")
            role    = st.text_input("Role / Designation")
        with colB:
            domain  = st.text_input("Domain")
            duration= st.text_input("Duration (e.g., Apr 2024 – Present)")
            team    = st.text_input("Team Size (e.g., Individual Contributor, 8)")
        resp = st.text_area("Responsibilities (one per line)\nExample:\n• End-to-end recruitment\n• Screening & scheduling\n• Offer negotiation")
        s2 = st.form_submit_button("➕ Add Experience")
        if s2:
            if company and role:
                add_experience(company, client, role, domain, duration, team, resp)
                st.success("Experience added!")
            else:
                st.warning("Company and Role are required.")
    if st.session_state.experiences:
        for i, exp in enumerate(st.session_state.experiences, 1):
            st.markdown(f"**{i}. {exp['company']} — {exp['role']} ({exp['duration']})**")
            st.caption(f"Client: {exp['client']} | Domain: {exp['domain']} | Team Size: {exp['team_size']}")
            for r in exp["responsibilities"]:
                st.write(f"- {r}")
        if st.button("Clear experience"):
            st.session_state.experiences = []
            st.experimental_rerun()

with st.expander("📜 Certificates (optional)"):
    cert = st.text_input("Certificate name")
    addc = st.button("➕ Add Certificate")
    if addc:
        add_certificate(cert)
        st.experimental_rerun()
    if st.session_state.certificates:
        st.write("Added certificates:")
        for c in st.session_state.certificates:
            st.write(f"- {c}")
        if st.button("Clear certificates"):
            st.session_state.certificates = []
            st.experimental_rerun()

st.markdown("---")
st.subheader("🧩 Include / Skip Sections")
cols = st.columns(5)
include = {
    "summary": cols[0].checkbox("Summary", value=True),
    "education": cols[1].checkbox("Education", value=True),
    "experience": cols[2].checkbox("Experience", value=True),
    "skills": cols[3].checkbox("Skills", value=True),
    "certs": cols[4].checkbox("Certificates", value=True),
}

ready = st.button("📥 Generate PDF Resume")

if ready:
    if not fullname:
        st.error("Full Name is required.")
    else:
        pdf_bytes = build_pdf(fullname, email, phone, address, headline, include)
        file_name = f"{fullname.replace(' ', '_')}_Resume.pdf"
        st.success("Resume generated!")
        st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=file_name, mime="application/pdf")