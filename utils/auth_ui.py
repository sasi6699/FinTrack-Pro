"""Shared presentation helpers for FinTrack Pro's public authentication pages."""

from base64 import b64encode
from pathlib import Path

import streamlit as st


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "images"


def hero_data_uri() -> str:
    """Return the local authentication artwork as a CSS-safe data URI."""
    hero_path = ASSET_DIR / "auth-hero.png"
    encoded = b64encode(hero_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def apply_auth_theme() -> None:
    """Apply the focused, dark glass visual system used before sign-in."""
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        #MainMenu, header, footer, [data-testid="stSidebar"],
        [data-testid="collapsedControl"] { display: none !important; }
        .stApp {
            background: radial-gradient(circle at 72% 12%, #142646 0%, #0b1320 36%, #070d17 100%);
            color: #f8fafc;
        }
        [data-testid="stAppViewContainer"] > .main { background: transparent; }
        .block-container {
            max-width: none !important;
            padding: 0.8rem 1.25rem 1.4rem !important;
        }
        .st-key-auth_rail {
            min-height: calc(100vh - 2rem);
            display: flex;
            flex-direction: column;
            border: 1px solid rgba(148, 163, 184, .13);
            border-radius: 18px;
            padding: 1.3rem .75rem;
            background: linear-gradient(155deg, rgba(18, 30, 48, .98), rgba(7, 15, 26, .98));
            box-shadow: 12px 0 36px rgba(0, 0, 0, .18);
        }
        .auth-logo { font-size: 1.13rem; font-weight: 750; letter-spacing: -.02em; margin: .35rem .25rem 2rem; white-space: nowrap; }
        .auth-logo span { font-size: 1.65rem; margin-right: .5rem; vertical-align: middle; }
        .nav-heading { color: #98a6b9; font-size: .73rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin: .95rem .35rem .55rem; }
        .muted-nav { color: #c2cbd8; font-size: .95rem; padding: .65rem .6rem; border-radius: 9px; margin: .16rem 0; }
        .rail-spacer { flex: 1; min-height: 4.2rem; }
        .st-key-auth_rail small { color: #8794a7; line-height: 1.45; display: block; margin: 1.1rem .25rem 0; }
        .st-key-auth_rail .stPageLink { margin: .22rem 0; }
        .st-key-auth_rail .stPageLink a {
            color: #d6deea !important; border-radius: 9px; padding: .68rem .65rem;
            font-size: .95rem; transition: none;
        }
        .st-key-auth_rail .stPageLink a:hover { background: rgba(46, 103, 226, .22); }
        .active-nav { color: white; background: linear-gradient(100deg, #2458c5, #1b3e7e); border-radius: 9px; padding: .68rem .65rem; font-size: .95rem; margin: .22rem 0; }
        .hero-panel {
            min-height: calc(100vh - 2rem); border-radius: 18px; background-size: cover; background-position: center;
            box-shadow: 0 18px 52px rgba(0, 0, 0, .26); overflow: hidden;
        }
        [data-testid="stForm"] {
            width: min(100%, 33.25rem); margin: 0 auto; padding: 2.45rem 2.7rem 2.2rem;
            background: linear-gradient(145deg, rgba(22, 34, 51, .91), rgba(14, 24, 38, .83));
            border: 1px solid rgba(148, 163, 184, .23); border-radius: 18px;
            box-shadow: 0 18px 50px rgba(0, 0, 0, .20); backdrop-filter: blur(14px);
        }
        .form-intro { text-align: center; margin: .35rem 0 1.65rem; }
        .form-badge { width: 4rem; height: 4rem; margin: 0 auto .85rem; display: grid; place-items: center; border-radius: 18px; font-size: 1.85rem; background: linear-gradient(145deg, #3d7cff, #1e4db1); box-shadow: 0 10px 26px rgba(40, 99, 225, .32); }
        .form-intro h1 { margin: 0; color: #f8fafc; font-size: 1.8rem; letter-spacing: -.04em; }
        .form-intro p { color: #b8c3d3; margin: .5rem 0 0; font-size: .96rem; }
        [data-testid="stForm"] label { color: #edf2f7 !important; font-size: .9rem !important; }
        [data-testid="stForm"] input {
            background: rgba(10, 19, 32, .58) !important; color: #f8fafc !important;
            border: 1px solid #45556a !important; border-radius: 9px !important;
            min-height: 3.15rem !important;
        }
        [data-testid="stForm"] input::placeholder { color: #8794a7 !important; }
        [data-testid="stForm"] input:focus { border-color: #3777fa !important; box-shadow: 0 0 0 1px #3777fa !important; }
        [data-testid="stForm"] button[kind="primary"], [data-testid="stForm"] button[kind="secondary"] {
            width: 100%; min-height: 3.25rem; margin-top: .7rem; border: 0 !important; border-radius: 9px !important;
            color: white !important; font-weight: 700 !important; background: linear-gradient(100deg, #2f6df4, #2960da) !important;
            box-shadow: 0 9px 20px rgba(30, 91, 221, .28);
        }
        [data-testid="stForm"] [data-testid="stCheckbox"] { margin-top: .15rem; }
        .auth-switch { text-align: center; color: #b8c3d3; margin: 1.25rem 0 -.35rem; font-size: .94rem; }
        .auth-switch a { color: #4a83ff; text-decoration: none; font-weight: 600; }
        .form-spacer { height: 10vh; }
        @media (max-width: 900px) {
            .block-container { padding: .7rem !important; }
            .st-key-auth_rail { display: none; }
            .hero-panel { min-height: 21rem; background-position: center 38%; }
            [data-testid="stForm"] { margin-top: 1rem; padding: 2rem 1.35rem; }
            .form-spacer { height: .8rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_auth_rail(active_page: str) -> None:
    """Render the small reference-style rail and safe public navigation."""
    with st.container(border=True, key="auth_rail"):
        st.markdown('<div class="auth-logo"><span>💰</span>FinTrack Pro</div>', unsafe_allow_html=True)
        if active_page == "login":
            st.markdown('<div class="active-nav">🔐 &nbsp; Login</div>', unsafe_allow_html=True)
            st.page_link("pages/2_Register.py", label="📝  Register")
        else:
            st.page_link("pages/1_Login.py", label="🔐  Login")
            st.markdown('<div class="active-nav">📝 &nbsp; Register</div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-heading">Your workspace</div>', unsafe_allow_html=True)
        for item in ("▣  Dashboard", "☷  Transactions", "▤  Budget", "⌁  Analytics", "▧  Reports"):
            st.markdown(f'<div class="muted-nav">{item}</div>', unsafe_allow_html=True)
        st.markdown('<div class="rail-spacer"></div><small>© 2026 FinTrack Pro<br>All rights reserved.</small>', unsafe_allow_html=True)


def render_hero() -> None:
    st.markdown(
        f'<div class="hero-panel" style="background-image: url(\'{hero_data_uri()}\');"></div>',
        unsafe_allow_html=True,
    )
