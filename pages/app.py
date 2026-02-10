import streamlit as st
st.set_page_config(page_title="Resume Screening System", layout="wide")

import pandas as pd
import pdfplumber
from docx import Document
import warnings
warnings.filterwarnings("ignore")

# -------- Hide Sidebar + Styling --------
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }

.center-box {
    max-width: 420px;
    margin: auto;
}

.top-right {
    position: fixed;
    top: 15px;
    right: 25px;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# -------- Login Protection --------
if "logged_in" not in st.session_state:
    st.switch_page("welcome.py")

# -------- Logout Button (Top Right) --------
st.markdown('<div class="top-right">', unsafe_allow_html=True)
if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("welcome.py")
st.markdown('</div>', unsafe_allow_html=True)

# -------- Title --------
st.markdown("<h1 style='text-align:center;'>Resume Screening System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Welcome! You are logged in.</p>", unsafe_allow_html=True)

# -------- Data --------
COMMON_SKILLS = [
    "python", "java", "c", "c++", "sql", "excel",
    "html", "css", "javascript", "react",
    "git", "docker", "aws", "pandas", "tensorflow"
]

def extract_text(file):
    text = ""
    try:
        if file.name.endswith(".pdf"):
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + " "
        elif file.name.endswith(".docx"):
            doc = Document(file)
            for p in doc.paragraphs:
                text += p.text + " "
    except:
        pass
    return text.lower()

def extract_skills(text):
    return [s for s in COMMON_SKILLS if s in text]

def calculate_match(resume_skills, job_skills):
    job_set = set(j.strip().lower() for j in job_skills.split(","))
    if not job_set:
        return 0
    return round((len(set(resume_skills) & job_set) / len(job_set)) * 100, 2)

# -------- Load Job Data --------
job_df = pd.read_csv("data/job_descriptions.csv")

# -------- Center Inputs (Reduced Width) --------
st.markdown("<div class='center-box'>", unsafe_allow_html=True)
job_title = st.selectbox("Select Job Role", job_df["JobTitle"])
resumes = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
screen_clicked = st.button("Screen Resumes")
st.markdown("</div>", unsafe_allow_html=True)

job_skills = job_df[job_df["JobTitle"] == job_title]["RequiredSkills"].values[0]

# -------- Results --------
if screen_clicked:
    st.markdown("<h3 style='text-align:center;'>Screening Results</h3>", unsafe_allow_html=True)

    if not resumes:
        st.warning("Please upload at least one resume")
    else:
        cols = st.columns(3)
        for i, resume in enumerate(resumes):
            text = extract_text(resume)
            skills = extract_skills(text)
            score = calculate_match(skills, job_skills)

            with cols[i % 3]:
                st.markdown(f"### {resume.name}")
                st.metric("Match Percentage", f"{score}%")

                pie_data = pd.DataFrame({
                    "Match": [score, 100 - score]
                }, index=["Matched", "Not Matched"])

                st.pyplot(pie_data.plot.pie(
                    y="Match",
                    autopct="%1.1f%%",
                    legend=False,
                    figsize=(3,3)
                ).figure)

                st.write("Skills Found:", ", ".join(skills))
