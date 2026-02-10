import streamlit as st
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.title("Login")

name = st.text_input("Name")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if name and password:
        st.session_state.logged_in = True
        st.switch_page("pages/app.py")
    else:
        st.error("Please fill all fields")

st.markdown("Don't have an account?")
if st.button("Register"):
    st.switch_page("pages/register.py")
