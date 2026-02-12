import streamlit as st
import re

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("Register")

# Initialize users storage
if "users" not in st.session_state:
    st.session_state.users = {}

email = st.text_input("Email ID")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

def is_valid_email(mail):
    return re.match(r"[^@]+@[^@]+\.[^@]+", mail)

if st.button("Register"):
    if not email or not password or not confirm_password:
        st.error("Please fill all fields")
    elif not is_valid_email(email):
        st.error("Enter a valid email address")
    elif email in st.session_state.users:
        st.error("This email is already registered")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        st.session_state.users[email] = {
            "password": password
        }
        st.success("Registration successful! Please login.")
        st.switch_page("pages/login.py")

