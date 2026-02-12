import streamlit as st

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("Login")

if "users" not in st.session_state:
    st.session_state.users = {}

email = st.text_input("Email ID")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not email or not password:
        st.error("Please fill all fields")
    elif email not in st.session_state.users:
        st.error("Email not registered. Please register.")
    elif st.session_state.users[email]["password"] != password:
        st.error("Incorrect password")
    else:
        st.success("Login successful!")
        st.session_state.logged_in = True
        st.session_state.current_user = email
        st.switch_page("pages/app.py")

