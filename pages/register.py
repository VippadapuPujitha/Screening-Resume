import streamlit as st
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("Register")

name = st.text_input("Name")
job_role = st.text_input("Job Role")
company = st.text_input("Company")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Register"):
    if not (name and job_role and company and password and confirm_password):
        st.error("Please fill all fields")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        st.success("Registration successful! Please login.")
        st.switch_page("pages/login.py")

st.markdown("Already have an account?")
if st.button("Login"):
    st.switch_page("pages/login.py")
