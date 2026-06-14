import streamlit as st
from skills_db import ROLE_SKILLS

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("📄 Resume Analyzer & Skill Gap Finder")

uploaded_file = st.file_uploader(
    "Upload Resume (TXT File)",
    type=["txt"]
)

role = st.selectbox(
    "Select Target Role",
    list(ROLE_SKILLS.keys())
)

if uploaded_file:

    resume_text = uploaded_file.read().decode("utf-8")

    st.subheader("Resume Content")
    st.text_area("", resume_text, height=200)

    skills_found = []

    for skill in ROLE_SKILLS[role]:
        if skill.lower() in resume_text.lower():
            skills_found.append(skill)

    missing_skills = [
        skill for skill in ROLE_SKILLS[role]
        if skill not in skills_found
    ]

    score = int(
        (len(skills_found) / len(ROLE_SKILLS[role])) * 100
    )

    st.subheader("Match Score")
    st.progress(score)
    st.write(f"{score}% Match")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Skills Found")
        st.success(", ".join(skills_found) if skills_found else "None")

    with col2:
        st.subheader("Skill Gaps")
        st.error(", ".join(missing_skills) if missing_skills else "None")

    st.subheader("Recommendations")

    if missing_skills:
        for skill in missing_skills:
            st.write(f"• Learn {skill}")
    else:
        st.success("Excellent! Your resume matches the role strongly.")
