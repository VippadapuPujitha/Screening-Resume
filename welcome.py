import streamlit as st

st.set_page_config(page_title="Welcome", layout="centered")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.big-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    margin-top: 150px;
}
.sub-title {
    text-align: center;
    font-size: 20px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>Resume Screening System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Smart resume analysis for better hiring</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Login", use_container_width=True):
            st.switch_page("pages/login.py")
    with b2:
        if st.button("Register", use_container_width=True):
            st.switch_page("pages/register.py")

