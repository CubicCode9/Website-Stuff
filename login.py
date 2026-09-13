import streamlit as st

def login(session_state):
    st.set_page_config(page_title="Horizon XS - Login")
    if "names" not in session_state or not isinstance(session_state["names"], dict):
        session_state["names"] = {
            "setup123": ["Pa55w0rd", "Admin"],
            "CubicCode9": ["OptionalHomework", "Member"],
            "GuestUser": ["", "Guest"],
        }

    if "logged" not in session_state:
        session_state["logged"] = False

    if "userName" not in session_state:
        session_state["userName"] = ""

    if "userType" not in session_state:
        session_state["userType"] = ""

    if "selectedRole" not in session_state:
        session_state["selectedRole"] = ""

    st.title("Horizon XS")
    st.write("Please log in to access the application.")
    st.write("To view the application as a guest, use GuestUser as the username and leave the password blank.")

    with st.form("loginForm"):
        session_state["userName"] = st.text_input("Username", value="", max_chars=20, key="name")
        password = st.text_input("Password", value="", max_chars=20, type="password", key="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        userName = session_state["userName"]
        if userName in session_state["names"] and password == session_state["names"][userName][0]:
            session_state["logged"] = True
            session_state["userName"] = userName
            session_state["userType"] = session_state["names"][userName][1]
            session_state["selectedRole"] = session_state["names"][userName][1]
            st.rerun()
        else:
            session_state["logged"] = False
            st.warning("Invalid username or password. Please try again.")