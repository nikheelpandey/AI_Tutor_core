import streamlit as st
from authentication import authenticate_user, register_user

def login(session_state):
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if authenticate_user(username, password):
            session_state.logged_in = True
            session_state.username = username
            st.success("Logged in successfully!")
            st.experimental_rerun()  # Restart the app
        else:
            st.error("Credentials do not match!")


def signup(session_state):
    email = st.text_input("Email", key="signup_email")
    reg_username = st.text_input("Username", key="signup_username")
    reg_password = st.text_input("Password", type="password", key="signup_password")
    age = st.number_input("Age", min_value=0, max_value=150, value=18, key="signup_age")

    if st.button("Register"):
        success = register_user(email, reg_username, reg_password, age)
        if success:
            st.success("Registration successful!")
            st.experimental_rerun()  # Restart the app
        else:
            st.error("Could not create a user!")

        st.clear()




def main(session_state=None):
    if session_state is None:
        session_state = get_session_state()

    if not session_state.logged_in:
        if 'page' not in session_state:
            session_state['page'] = 'login'

        if st.experimental_get_query_params().get('page', [''])[0] == 'signup':
            session_state.page = 'signup'

        if session_state.page == 'login':
            login(session_state)
            st.markdown("New user? [Sign up](?page=signup)")

        elif session_state.page == 'signup':
            signup(session_state)
            st.markdown("Already a user? [Login](?page=login)")

    if session_state.logged_in:
        show_home_page(session_state)


def show_home_page(session_state):
    st.title("Home")
    pass


def get_session_state():
    session_state = st.session_state
    if 'logged_in' not in session_state:
        session_state['logged_in'] = False
    if 'username' not in session_state:
        session_state['username'] = ""
    if 'learning_history' not in session_state:
        session_state['learning_history'] = []
    if 'learning_started' not in session_state:
        session_state['learning_started'] = False
    return session_state


if __name__ == "__main__":
    main()
