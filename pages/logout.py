import streamlit as st
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Logout", layout="centered")

if "show_logout_dialog" not in st.session_state:
    st.session_state.show_logout_dialog = True

if st.session_state.get("show_logout_dialog", False):
    @st.dialog("Logout Confirmation")
    def logout_dialog():
        st.write("Are you sure you want to logout?")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Cancel"):
                st.switch_page("pages/app.py")

        with c2:
            if st.button("Logout"):
                st.session_state.clear()
                st.switch_page("welcome.py")

    logout_dialog()
