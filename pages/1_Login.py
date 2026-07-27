import streamlit as st
from utils.auth import login_user
from utils.auth_ui import apply_auth_theme, render_auth_rail, render_hero

st.set_page_config(page_title="Login | FinTrack Pro", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")
apply_auth_theme()

rail, hero, form_column = st.columns([0.32, 0.98, 1.03], gap="medium")

with rail:
    render_auth_rail("login")

with hero:
    render_hero()

with form_column:
    st.markdown('<div class="form-spacer"></div>', unsafe_allow_html=True)
    with st.form("login_form"):
        st.markdown(
            '''<div class="form-intro"><div class="form-badge">🔐</div><h1>Welcome Back!</h1><p>Log in to continue to your account</p></div>''',
            unsafe_allow_html=True,
        )
        email = st.text_input("Email address", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        st.checkbox("Remember me", value=True, key="remember_me")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        st.markdown('<p class="auth-switch">Don’t have an account? <a href="/Register" target="_self">Register here</a></p>', unsafe_allow_html=True)

if submitted:
    if email.strip() == "" or password == "":
        st.warning("Please enter your email and password.")
    else:
        success, result = login_user(email.strip(), password)

        if success:
            st.session_state.logged_in = True
            st.session_state.user = result
            st.switch_page("pages/3_Dashboard.py")

        else:
            st.error(result)
