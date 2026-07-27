import streamlit as st


st.set_page_config(page_title="Home", page_icon="💰", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp {
        background:
            radial-gradient(circle at 78% 12%, rgba(37, 99, 235, .17), transparent 29rem),
            radial-gradient(circle at 18% 70%, rgba(29, 78, 216, .10), transparent 26rem),
            #0F172A;
        color: #f8fafc;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { max-width: 1250px; padding: 3.25rem 2.25rem 2rem; }
    [data-testid="stSidebar"] {
        background: linear-gradient(165deg, #111b2d 0%, #0b1220 100%);
        border-right: 1px solid rgba(148, 163, 184, .18);
    }
    [data-testid="stSidebarNav"] a[href$="/"] span,
    [data-testid="stSidebarNav"] a[href$="/"] p { font-size: 0; }
    [data-testid="stSidebarNav"] a[href$="/"] span::after,
    [data-testid="stSidebarNav"] a[href$="/"] p::after {
        content: "Home"; font-size: 1rem; color: #ffffff; font-weight: 650;
    }
    [data-testid="stSidebarNav"] a[href$="/"] { background: rgba(37, 99, 235, .18); border-radius: 9px; }
    .hero-copy { padding: 4.2rem 0 2rem; }
    .eyebrow {
        display: inline-flex; align-items: center; gap: .45rem; color: #93c5fd;
        background: rgba(37, 99, 235, .13); border: 1px solid rgba(96, 165, 250, .28);
        padding: .42rem .75rem; border-radius: 999px; font-size: .82rem; font-weight: 700;
        letter-spacing: .04em; text-transform: uppercase;
    }
    .hero-copy h1 {
        font-size: clamp(3rem, 5.1vw, 5.35rem); line-height: .98; letter-spacing: -.065em;
        margin: 1.25rem 0 .9rem; color: #f8fafc;
    }
    .hero-copy h1 span { color: #4f7dff; }
    .hero-copy h2 { font-size: clamp(1.35rem, 2vw, 1.9rem); line-height: 1.25; margin: 0 0 1.15rem; color: #dbeafe; }
    .hero-copy p { max-width: 34rem; color: #aebbd0; font-size: 1.1rem; line-height: 1.75; margin: 0; }
    .st-key-home_actions { margin-top: 1.8rem; max-width: 27rem; }
    .st-key-home_actions .stPageLink a {
        min-height: 3.2rem; justify-content: center; border-radius: 10px; padding: .75rem 1rem;
        color: #f8fafc !important; border: 1px solid rgba(148, 163, 184, .42);
        background: rgba(15, 23, 42, .52); font-weight: 700; transition: all .2s ease;
    }
    .st-key-home_actions [data-testid="column"]:first-child .stPageLink a {
        background: linear-gradient(120deg, #2563eb, #3b82f6); border-color: #3b82f6;
        box-shadow: 0 11px 25px rgba(37, 99, 235, .30);
    }
    .st-key-home_actions .stPageLink a:hover { transform: translateY(-2px); border-color: #60a5fa; box-shadow: 0 12px 25px rgba(30, 64, 175, .26); }
    .st-key-home_hero_art { padding-top: .5rem; }
    .st-key-home_hero_art img {
        width: 100%; max-height: 31rem; object-fit: cover; object-position: 58% center;
        border-radius: 22px; border: 1px solid rgba(148, 163, 184, .25);
        box-shadow: 0 28px 58px rgba(0, 0, 0, .43), 0 0 0 1px rgba(37, 99, 235, .12);
    }
    .feature-heading { text-align: center; margin: 4.75rem 0 1.7rem; }
    .feature-heading h3 { font-size: clamp(1.65rem, 3vw, 2.35rem); letter-spacing: -.04em; margin: 0; color: #f8fafc; }
    .feature-heading p { color: #94a3b8; margin: .65rem 0 0; }
    .feature-grid {
        display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem;
    }
    .feature-card {
        min-height: 13rem; padding: 1.5rem; border-radius: 16px;
        background: linear-gradient(145deg, rgba(30, 41, 59, .83), rgba(15, 23, 42, .67));
        border: 1px solid rgba(148, 163, 184, .21); box-shadow: inset 0 1px 0 rgba(255, 255, 255, .045);
        backdrop-filter: blur(12px); transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px); border-color: rgba(96, 165, 250, .65);
        box-shadow: 0 17px 30px rgba(0, 0, 0, .25), inset 0 1px 0 rgba(255, 255, 255, .08);
    }
    .feature-icon {
        width: 3rem; height: 3rem; display: grid; place-items: center; border-radius: 12px;
        background: linear-gradient(135deg, rgba(37, 99, 235, .95), rgba(79, 70, 229, .8));
        box-shadow: 0 9px 18px rgba(37, 99, 235, .23); font-size: 1.45rem;
    }
    .feature-card h4 { margin: 1rem 0 .45rem; font-size: 1.1rem; color: #f8fafc; }
    .feature-card p { margin: 0; color: #a9b6c8; line-height: 1.55; }
    .home-footer {
        margin-top: 4rem; padding: 1.6rem 0 1rem; border-top: 1px solid rgba(148, 163, 184, .18);
        text-align: center; color: #94a3b8; line-height: 1.75; font-size: .9rem;
    }
    .home-footer strong { color: #dbeafe; }
    @media (max-width: 900px) {
        .block-container { padding: 1.6rem 1.15rem; }
        .hero-copy { padding: 1.25rem 0 .75rem; }
        .st-key-home_hero_art { padding-top: 1rem; }
        .feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 580px) {
        .feature-grid { grid-template-columns: 1fr; }
        .hero-copy h1 { font-size: 3rem; }
        .st-key-home_actions { max-width: none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.02, 1], gap="large")

with left:
    st.markdown(
        """
        <section class="hero-copy">
            <div class="eyebrow">✦ Your money, clearly managed</div>
            <h1>FinTrack <span>Pro</span></h1>
            <h2>Your Smart Personal Finance Dashboard</h2>
            <p>Track spending, grow savings, manage budgets and make smarter financial decisions.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="home_actions"):
        login_column, register_column = st.columns(2, gap="small")
        with login_column:
            st.page_link("pages/1_Login.py", label="Login", icon="🔐")
        with register_column:
            st.page_link("pages/2_Register.py", label="Create Account", icon="✨")

with right:
    with st.container(key="home_hero_art"):
        st.image("assets/images/auth-hero.png", use_container_width=True, output_format="PNG")

st.markdown(
    """
    <section class="feature-heading">
        <h3>Everything you need to manage your finances</h3>
        <p>Simple tools for clearer, more confident money decisions.</p>
    </section>
    <section class="feature-grid">
        <article class="feature-card"><div class="feature-icon">💰</div><h4>Track Expenses</h4><p>Record daily expenses easily.</p></article>
        <article class="feature-card"><div class="feature-icon">📊</div><h4>Analytics</h4><p>Visualize spending trends with interactive charts.</p></article>
        <article class="feature-card"><div class="feature-icon">🎯</div><h4>Budget Planner</h4><p>Create and monitor monthly budgets.</p></article>
        <article class="feature-card"><div class="feature-icon">📄</div><h4>Reports</h4><p>Generate monthly financial reports.</p></article>
        <article class="feature-card"><div class="feature-icon">🔔</div><h4>Smart Alerts</h4><p>Receive notifications for budgets and spending.</p></article>
        <article class="feature-card"><div class="feature-icon">💳</div><h4>Income Tracking</h4><p>Manage salary, freelance income and investments.</p></article>
    </section>
    <footer class="home-footer"><strong>FinTrack Pro v1.0</strong><br>Bachelor of Information Technology<br>Personal Finance Dashboard<br>2026</footer>
    """,
    unsafe_allow_html=True,
)
