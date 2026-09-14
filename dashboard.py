import streamlit as st
import users, sidebar

def Admin(session_state):
    st.set_page_config(page_title="Horizon XS - Admin Dashboard")

    if "names" not in session_state or not isinstance(session_state["names"], dict):
        session_state["names"] = users.load()

    st.title("Admin Dashboard")

def Member(session_state):
    st.set_page_config(page_title="Horizon XS - Member Dashboard")

    if "names" not in session_state or not isinstance(session_state["names"], dict):
        session_state["names"] = users.load()

    st.title("Member Dashboard")
    st.write("Welcome to the Member Dashboard. Here you can view your profile and access member resources.")

def Guest(session_state):
    st.set_page_config(page_title="Horizon XS - Guest Dashboard")

    if "names" not in session_state or not isinstance(session_state["names"], dict):
        session_state["names"] = users.load()

    st.title("Guest Dashboard")
    st.write("Welcome to the Guest Dashboard. Here you can explore the application as a guest.")

def run(session_state):
    if "userType" not in session_state:
        st.warning("User type not found. Please log in.")
        return

    userType = session_state["userType"]

    if userType == "Admin":
        Admin(session_state)
    elif userType == "Member":
        Member(session_state)
    elif userType == "Guest":
        Guest(session_state)
    else:
        st.warning("Unknown user type. Please log in.")