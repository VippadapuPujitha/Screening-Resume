import streamlit as st
st.set_page_config(page_title="Resume Screening System", layout="wide")

import pandas as pd
import pdfplumber
from docx import Document
import warnings
warnings.filterwarnings("ignore")
import streamlit.components.v1 as components

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- Hide Sidebar ----------------
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }

.donut-wrap {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}

.donut {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: conic-gradient(
        #7c4dff 0deg,
        #00e5ff calc(var(--percent) * 3.6deg),
        #e0e0e0 0deg
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    color: #333;
    position: relative;
}

.donut::before {
    content: "";
    width: 75px;
    height: 75px;
    background: white;
    border-radius: 50%;
    position: absolute;
}

.donut span {
    position: relative;
    z-index: 1;
}

.result-card {
    background: #f8f9fb;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Login Protection ----------------
if "logged_in" not in st.session_state:
    st.switch_page("welcome.py")

# ---------------- Logout Button (Top Right) ----------------
c1, c2, c3 = st.columns([6, 1, 1])
with c3:
    if st.button("Logout"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# ---------------- Title ----------------
st.markdown("<h1 style='text-align:center;'>Resume Screening System</h1>", unsafe_allow_html=True)

# ---------------- Skills Dictionary ----------------
COMMON_SKILLS = [
    "python", "java", "c", "c++", "sql", "excel", "html", "css", "javascript",
    "react", "git", "docker", "aws", "pandas", "tensorflow", "oop",
    "data structures", "dbms", "machine learning"
]

def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + " "
    elif file.name.endswith(".docx"):
        doc = Document(file)
        for p in doc.paragraphs:
            text += p.text + " "
    return text.lower()

def extract_skills(text):
    return list(set([s for s in COMMON_SKILLS if s in text]))

def ml_similarity(resume_skills, job_skills):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_skills, job_skills])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(score * 100, 1)

# ---------------- Load Job Data ----------------
job_df = pd.read_csv("data/job_descriptions.csv")

# ---------------- Inputs ----------------
l, c, r = st.columns([2, 5, 2])
with c:
    job_title = st.selectbox("Select Job Role", job_df["JobTitle"])
    resumes = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
    screen_clicked = st.button("Screen Resumes", use_container_width=True)

job_skill_text = job_df[job_df["JobTitle"] == job_title]["RequiredSkills"].values[0].lower()

# ---------------- Auto Scroll ----------------
if "scroll_to_results" not in st.session_state:
    st.session_state.scroll_to_results = False

if screen_clicked:
    st.session_state.scroll_to_results = True
    st.rerun()

# ---------------- Results ----------------
if st.session_state.scroll_to_results:

    st.markdown("<div id='results'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>Screening Results</h2>", unsafe_allow_html=True)

    if not resumes:
        st.warning("Please upload at least one resume")
    else:
        cols = st.columns(len(resumes))

        for col, resume in zip(cols, resumes):
            with col:
                text = extract_text(resume)
                resume_skills = " ".join(extract_skills(text))
                score = ml_similarity(resume_skills, job_skill_text)

                st.markdown(f"""
                <div class="result-card">
                    <h4>{resume.name}</h4>
                    <div class="donut-wrap">
                        <div class="donut" style="--percent:{score};">
                            <span>{score}%</span>
                        </div>
                    </div>
                    <p style="margin-top:10px;"><b>Match Score</b></p>
                    <p style="font-size:14px;">Skills: {resume_skills}</p>
                </div>
                """, unsafe_allow_html=True)

    components.html("""
    <script>
        setTimeout(() => {
            const el = window.parent.document.getElementById("results");
            if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
        }, 300);
    </script>
    """, height=0)

