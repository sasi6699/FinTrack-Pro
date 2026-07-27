import streamlit as st


def apply_theme():
    """Apply FinTrack Pro's always-on dark theme and readable KPI cards."""
    st.session_state.theme = "Dark"
    st.markdown(
        """<style>
        .stApp {
            background: radial-gradient(circle at top right, #172a4a 0%, #101827 42%, #0b1220 100%);
            color: #e5e7eb;
        }
        [data-testid='stHeader'] { background: transparent; }
        [data-testid='stSidebar'] { background: #111b2b; border-right: 1px solid rgba(96, 165, 250, .18); }
        [data-testid='stMetric'] {
            background: linear-gradient(145deg, rgba(35, 47, 68, .96), rgba(27, 35, 51, .96)) !important;
            border: 1px solid rgba(70, 130, 246, .45) !important;
            border-radius: 14px;
            padding: 1rem 1.05rem;
            box-shadow: 0 10px 26px rgba(3, 10, 24, .28), inset 0 1px 0 rgba(255, 255, 255, .04);
        }
        [data-testid='stMetricLabel'],
        [data-testid='stMetricLabel'] p {
            color: #c5cfdd !important;
        }
        [data-testid='stMetricValue'],
        [data-testid='stMetricValue'] > div,
        [data-testid='stMetricValue'] p {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        [data-testid='stMetricDelta'] { color: #7dd3fc !important; }
        [data-testid='stMetric']:hover {
            border-color: rgba(96, 165, 250, .72) !important;
            box-shadow: 0 13px 30px rgba(3, 10, 24, .34), 0 0 0 1px rgba(59, 130, 246, .10);
        }
        </style>""",
        unsafe_allow_html=True,
    )


def sidebar(user):
    with st.sidebar:
        st.header("FinTrack Pro")
        st.caption(f"Signed in as {user[1]}")
        st.caption("🌙 Dark mode enabled")
        st.divider()
        st.subheader("Notifications")
        st.checkbox("Budget alerts", value=True, key="budget_alerts")
        st.checkbox("Monthly summary", value=True, key="summary_alerts")
        if st.button("Log out", use_container_width=True):
            st.session_state.clear()
            st.switch_page("pages/1_Login.py")
