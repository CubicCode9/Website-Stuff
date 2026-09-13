import streamlit as st
import users

def management(session_state):
    st.set_page_config(page_title="Horizon XS - User Management")

    if "names" not in session_state or not isinstance(session_state["names"], dict):
        session_state["names"] = users.load()

    st.title("User Management")
    st.write("Manage user accounts and roles.")

    with st.form("addUserForm"):
        new_username = st.text_input("New Username", value="", max_chars=20, key="new_username")
        new_password = st.text_input("New Password", value="", max_chars=20, type="password", key="new_password")
        new_role = st.selectbox("Role", ["Admin", "Member", "Guest"], key="new_role")
        add_user_submitted = st.form_submit_button("Add User")

    if add_user_submitted:
        if new_username and new_password:
            if new_username not in session_state["names"]:
                users.add(new_username, new_password, new_role)
                st.success(f"User '{new_username}' added successfully.")
            else:
                st.warning(f"Username '{new_username}' already exists.")
        else:
            st.warning("Please provide both username and password.")

    st.subheader("Existing Users")
    for username, (password, role) in session_state["names"].items():
        st.write(f"Username: {username}, Role: {role}")