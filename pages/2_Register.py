import streamlit as st
from utils.auth import register_user
from utils.auth_ui import apply_auth_theme, render_auth_rail, render_hero

st.set_page_config(
    page_title="Register | FinTrack Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_auth_theme()

rail, hero, form_column = st.columns([0.32, 0.98, 1.03], gap="medium")

with rail:
    render_auth_rail("register")

with hero:
    render_hero()

with form_column:
    st.markdown('<div class="form-spacer"></div>', unsafe_allow_html=True)
    with st.form("register_form"):
        st.markdown(
            '''<div class="form-intro"><div class="form-badge">✨</div><h1>Create account</h1><p>Start tracking your money with confidence</p></div>''',
            unsafe_allow_html=True,
        )
        full_name = st.text_input("Full name", placeholder="Enter your full name")
        email = st.text_input("Email address", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm password", type="password", placeholder="Confirm your password")
        submit = st.form_submit_button("Create account", type="primary", use_container_width=True)
        st.markdown('<p class="auth-switch">Already have an account? <a href="/Login" target="_self">Log in here</a></p>', unsafe_allow_html=True)

if submit:

    if full_name.strip() == "":
        st.error("Full name is required.")

    elif email.strip() == "":
        st.error("Email is required.")

    elif password == "":
        st.error("Password is required.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    else:

        success, message = register_user(
            full_name,
            email,
            password
        )

        if success:
            st.success(message)

        else:
            st.error(message)
