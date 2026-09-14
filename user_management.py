import streamlit as st
import users

def management(session_state):
    st.set_page_config(page_title="Horizon XS - User Management")

    if "names" not in session_state or not isinstance(session_state["names"], dict):
        session_state["names"] = users.load()
    if "showPasswords" not in session_state or not isinstance(session_state["showPasswords"], dict):
        session_state["showPasswords"] = {}
    if "pendingDeleteUser" not in session_state:
        session_state["pendingDeleteUser"] = None

    st.title("User Management")
    st.write("Manage user accounts and roles.")

    with st.form("addUserForm"):
        new_username = st.text_input("New Username", value="", max_chars=20, key="adminNewUserNameInput")
        new_password = st.text_input("New Password", value="", max_chars=20, type="password", key="adminNewUserPasswordInput")
        new_role = st.selectbox("Role", ["Admin", "Member", "Guest"], key="adminNewUserRoleSelect")
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
    if not session_state["names"]:
        st.info("No users found.")
    else:
        roleOrder = {"Admin": 0, "Member": 1, "Guest": 2}
        orderedUsers = dict(sorted(session_state["names"].items(), key=lambda item: roleOrder.get(item[1][1], 99)))

        headers = st.columns([2, 2, 2, 1, 1])
        with headers[0]:
            st.caption("Username")
        with headers[1]:
            st.caption("Role")
        with headers[2]:
            st.caption("Password")
        with headers[3]:
            st.caption("Show")
        with headers[4]:
            st.caption("Delete")

        for username, (password, role) in orderedUsers.items():
            cols = st.columns([2, 2, 2, 1, 1])
            showPassword = session_state["showPasswords"].get(username, False)

            with cols[0]:
                st.write(username)
            with cols[1]:
                st.write(role)
            with cols[2]:
                if role != "Admin":
                    if showPassword:
                        st.code(password)
                    else:
                        st.code("*" * len(password) if password else "")
            with cols[3]:
                if role != "Admin":
                    buttonLabel = "Hide" if session_state["showPasswords"].get(username, False) else "Show"
                    if st.button(buttonLabel, key=f"togglePassword{username}"):
                        session_state["showPasswords"][username] = not session_state["showPasswords"].get(username, False)
                        st.rerun()
            with cols[4]:
                if role != "Admin":
                    if not username in users.get_default_accounts():
                        if st.button("Delete", key=f"delete{username}"):
                            session_state["pendingDeleteUser"] = username

        if session_state["pendingDeleteUser"]:
            username = session_state["pendingDeleteUser"]
            st.warning(f"Are you sure you want to delete '{username}'?")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Confirm Delete", key="confirmDeleteUser"):
                    if users.delete(username):
                        session_state["names"] = users.load()
                        session_state["showPasswords"].pop(username, None)
                        session_state["pendingDeleteUser"] = None
                        st.success(f"User '{username}' deleted successfully.")
                        st.rerun()
                    else:
                        session_state["pendingDeleteUser"] = None
                        st.warning(f"Could not delete '{username}'.")

            with col2:
                if st.button("Cancel", key="cancelDeleteUser"):
                    session_state["pendingDeleteUser"] = None
                    st.rerun()