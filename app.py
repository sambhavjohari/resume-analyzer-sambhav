import streamlit as st
from skills_db import ROLE_SKILLS
import PyPDF2
from docx import Document

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("📄 Resume Analyzer & Skill Gap Finder")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["txt", "pdf", "docx"]
)

role = st.selectbox(
    "Select Target Role",
    list(ROLE_SKILLS.keys())
)

def extract_text(file):
    file_type = file.name.split(".")[-1].lower()

    if file_type == "txt":
        return file.read().decode("utf-8")

    elif file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""

        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return text

    elif file_type == "docx":
        doc = Document(file)

        text = "\n".join(
            para.text for para in doc.paragraphs
        )

        return text

    return ""

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Content")
    st.text_area(
        "Extracted Text",
        resume_text,
        height=250
    )

    skills_found = []

    for skill in ROLE_SKILLS[role]:
        if skill.lower() in resume_text.lower():
            skills_found.append(skill)

    missing_skills = [
        skill for skill in ROLE_SKILLS[role]
        if skill not in skills_found
    ]

    score = int(
        len(skills_found)
        / len(ROLE_SKILLS[role])
        * 100
    )

    st.subheader("Resume Match Score")
    st.progress(score)

    st.metric(
        "Match Percentage",
        f"{score}%"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills Found")

        if skills_found:
            for skill in skills_found:
                st.success(skill)
        else:
            st.warning("No matching skills found.")

    with col2:
        st.subheader("❌ Skill Gaps")

        if missing_skills:
            for skill in missing_skills:
                st.error(skill)
        else:
            st.success("No skill gaps detected.")

    st.subheader("📚 Learning Recommendations")

    if missing_skills:
        for skill in missing_skills:
            st.write(f"• Learn {skill}")
    else:
        st.success(
            "Excellent! Your resume strongly matches this role."
            )
