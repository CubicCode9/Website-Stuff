import streamlit as st
import sidebar, login, users

st.set_page_config(page_title="Horizon XS", page_icon="HorizonXS_ICON.png", layout="wide")

if "names" not in st.session_state or not isinstance(st.session_state["names"], dict):
    st.session_state["names"] = users.load()

if "logged" not in st.session_state:
    st.session_state["logged"] = False

if "creating" not in st.session_state:
    st.session_state["creating"] = False

if "userName" not in st.session_state:
    st.session_state["userName"] = ""

if "userType" not in st.session_state:
    st.session_state["userType"] = ""

if "selectedRole" not in st.session_state:
    st.session_state["selectedRole"] = ""

if st.session_state["logged"]:
    sidebar.sidebar(st.session_state)
elif st.session_state["creating"]:
    users.create(st.session_state)
else:
    login.login(st.session_state)