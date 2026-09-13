import streamlit as st
import user_management


def sidebar(session_state):
    roles = ["Admin", "Member", "Guest"]
    roleRank = {"Guest": 0, "Member": 1, "Admin": 2}

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

    if "nav" not in session_state:
        session_state["nav"] = "Dashboard"

    if "navCheck" not in session_state:
        session_state["navCheck"] = ""

    if not session_state["logged"]:
        return

    userName = session_state["userName"]
    userType = session_state["userType"]
    if not userType:
        userType = session_state["names"][userName][1]
        session_state["userType"] = userType

    allowedRoles = [role for role in roles if roleRank[role] <= roleRank[userType]]
    selectedRole = session_state["selectedRole"]
    if selectedRole not in allowedRoles:
        selectedRole = userType
        session_state["selectedRole"] = selectedRole

    st.sidebar.title("Settings and Navigation")
    st.sidebar.write(f"Welcome, {userName}!")

    with st.sidebar.expander("User Info"):
        selectedRole = st.selectbox(
            "View As",
            allowedRoles,
            index=allowedRoles.index(selectedRole),
            key="selectedRole",
        )
        st.write(f"User role: {userType}")
        st.write(f"Viewing as: {selectedRole}")

    with st.sidebar.expander("Navigation"):
        if selectedRole == "Admin":
            st.segmented_control("Admin Navigation", ["Dashboard", "Profile", "Reports", "Options", "Help", "User Management", "Settings"], key="nav")
        elif selectedRole == "Member":
            st.segmented_control("Member Navigation", ["Dashboard", "Profile", "Settings", "Help", "Upgrade", "About"], key="nav")
        elif selectedRole == "Guest":
            st.segmented_control("Guest Navigation", ["Dashboard", "Help", "Upgrade", "About"], key="nav")

    if session_state["nav"] != session_state["navCheck"]:
        session_state["navCheck"] = session_state["nav"]
    if session_state["nav"] == "User Management": user_management.management(session_state)

    if st.sidebar.button("Logout"):
        st.session_state.pop("logged", None)
        session_state.pop("userName", None)
        session_state.pop("userType", None)
        session_state.pop("selectedRole", None)
        st.rerun()