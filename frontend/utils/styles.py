import streamlit as st


APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root {
    --ink: #172b2b;
    --muted: #617070;
    --teal: #147d73;
    --teal-dark: #0d5f58;
    --coral: #e66a4e;
    --gold: #d7a33d;
    --canvas: #f4f7f5;
    --surface: #ffffff;
    --line: #dce5e1;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink); }
.stApp { background: var(--canvas); }
[data-testid="stAppViewContainer"] {
    background-color: var(--canvas);
    background-image: radial-gradient(#ccd8d3 0.7px, transparent 0.7px);
    background-size: 18px 18px;
}
[data-testid="stHeader"] { background: rgba(244, 247, 245, 0.88); backdrop-filter: blur(12px); }
[data-testid="stAppDeployButton"] { display: none; }
[data-testid="stMainBlockContainer"] { max-width: 1480px; padding: 2rem 2.5rem 4rem; }

h1, h2, h3 { font-family: 'Manrope', sans-serif; color: var(--ink); letter-spacing: 0; }
h1 { font-size: 2rem !important; font-weight: 800 !important; margin-bottom: 0.15rem !important; }
h2 { font-size: 1.3rem !important; }
h3 { font-size: 1.05rem !important; }
p, label { color: var(--muted); }

[data-testid="stSidebar"] { background: #122c2b; border-right: 0; min-width: 250px; }
[data-testid="stSidebar"] * { color: #eaf3ef; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #b9cbc5; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 0.25rem; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding: 0.66rem 0.8rem;
    border-radius: 6px;
    transition: background-color 120ms ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: #1c403d; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background: #20685f; }
[data-testid="stSidebar"] [data-testid="stRadio"] > label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stSidebar"] .stButton button { width: 100%; background: transparent; border-color: #53716c; color: #eaf3ef; }

.bt-brand { padding: 0.25rem 0 1.2rem; border-bottom: 1px solid #34514d; margin-bottom: 1rem; }
.bt-brand-mark { display: flex; align-items: center; gap: 0.7rem; }
.bt-brand-icon { width: 34px; height: 34px; display: grid; place-items: center; background: var(--coral); color: white; border-radius: 6px; font-family: 'Manrope'; font-weight: 800; }
.bt-brand-name { color: white; font-family: 'Manrope'; font-weight: 800; font-size: 1rem; }
.bt-brand-copy { color: #9fb4ae; font-size: 0.75rem; margin-top: 0.15rem; }
.bt-user { display: flex; align-items: center; gap: 0.65rem; padding: 0.7rem 0; }
.bt-avatar { width: 30px; height: 30px; border-radius: 50%; background: #d7a33d; color: #172b2b; display: grid; place-items: center; font-weight: 700; }
.bt-user strong { color: white; font-size: 0.82rem; }
.bt-user span { color: #9fb4ae; font-size: 0.7rem; display: block; }

.bt-page-head { display: flex; justify-content: space-between; align-items: end; gap: 1rem; margin-bottom: 1.4rem; }
.bt-eyebrow { color: var(--teal); text-transform: uppercase; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 0.35rem; }
.bt-page-title { font-family: 'Manrope'; color: var(--ink); font-size: 1.85rem; font-weight: 800; line-height: 1.15; }
.bt-page-copy { color: var(--muted); font-size: 0.86rem; margin-top: 0.3rem; }
.bt-date-chip { white-space: nowrap; color: #3e5452; border: 1px solid var(--line); background: rgba(255,255,255,.75); padding: 0.45rem 0.65rem; border-radius: 5px; font-size: 0.76rem; }

[data-testid="stMetric"] { background: var(--surface); border: 1px solid var(--line); border-top: 3px solid var(--teal); border-radius: 7px; padding: 0.95rem 1rem; min-height: 106px; box-shadow: 0 5px 18px rgba(27, 61, 57, 0.05); }
[data-testid="stMetric"] label { color: var(--muted); font-size: 0.75rem; font-weight: 600; }
[data-testid="stMetricValue"] { font-family: 'Manrope'; color: var(--ink); font-size: 1.75rem; font-weight: 800; }
[data-testid="column"]:nth-child(5n+4) [data-testid="stMetric"] { border-top-color: var(--gold); }
[data-testid="column"]:nth-child(5n+5) [data-testid="stMetric"] { border-top-color: var(--coral); }

[data-testid="stPlotlyChart"], [data-testid="stDataFrame"] { background: var(--surface); border: 1px solid var(--line); border-radius: 7px; padding: 0.35rem; box-shadow: 0 5px 18px rgba(27, 61, 57, 0.04); overflow: hidden; }
[data-testid="stDataFrame"] { padding: 0.55rem; }

.stTabs [data-baseweb="tab-list"] { gap: 0.2rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { height: 2.8rem; padding: 0 1rem; background: transparent; border-radius: 4px 4px 0 0; }
.stTabs [aria-selected="true"] { color: var(--teal) !important; font-weight: 700; border-bottom: 2px solid var(--teal); }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.25rem; }

[data-testid="stForm"] { background: var(--surface); border: 1px solid var(--line); border-radius: 7px; padding: 1.15rem 1.25rem 1.3rem; }
[data-baseweb="input"] > div, [data-baseweb="select"] > div, textarea { border-color: #cdd9d5 !important; background: #fbfcfb !important; border-radius: 5px !important; }
.stButton button, [data-testid="stFormSubmitButton"] button, [data-testid="stDownloadButton"] button {
    border-radius: 5px;
    border: 1px solid var(--teal);
    background: var(--teal);
    color: white;
    font-weight: 700;
    min-height: 2.45rem;
}
.stButton button:hover, [data-testid="stFormSubmitButton"] button:hover, [data-testid="stDownloadButton"] button:hover { background: var(--teal-dark); border-color: var(--teal-dark); color: white; }

[data-testid="stAlert"] { border-radius: 6px; border-width: 1px; }
hr { border-color: var(--line) !important; }

.bt-login-wrap { max-width: 450px; margin: 7vh auto 0; text-align: center; }
.bt-login-mark { width: 58px; height: 58px; margin: 0 auto 1.1rem; display: grid; place-items: center; border-radius: 10px; background: var(--teal); color: white; font-family: 'Manrope'; font-weight: 800; font-size: 1.25rem; box-shadow: 0 10px 24px rgba(20,125,115,.22); }
.bt-login-title { font-family: 'Manrope'; font-size: 1.8rem; font-weight: 800; color: var(--ink); }
.bt-login-copy { color: var(--muted); font-size: 0.88rem; margin: 0.4rem 0 1.3rem; }

@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"] { padding: 1.2rem 1rem 3rem; }
    .bt-page-head { align-items: start; flex-direction: column; }
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap; gap: 0.7rem; }
    [data-testid="column"] { min-width: 170px !important; flex: 1 1 45% !important; }
}
</style>
"""


def apply_theme():
    st.markdown(APP_CSS, unsafe_allow_html=True)


def page_header(title, copy, eyebrow='Operations', date_label='Dec 2023 - Oct 2024'):
    st.markdown(
        f'''<div class="bt-page-head"><div><div class="bt-eyebrow">{eyebrow}</div><div class="bt-page-title">{title}</div><div class="bt-page-copy">{copy}</div></div><div class="bt-date-chip">{date_label}</div></div>''',
        unsafe_allow_html=True,
    )


def sidebar_brand(username):
    initial = (username or 'U')[0].upper()
    st.markdown(
        f'''<div class="bt-brand"><div class="bt-brand-mark"><div class="bt-brand-icon">BT</div><div><div class="bt-brand-name">BrewTech</div><div class="bt-brand-copy">Operations Hub</div></div></div></div><div class="bt-user"><div class="bt-avatar">{initial}</div><div><strong>{username}</strong><span>Operations administrator</span></div></div>''',
        unsafe_allow_html=True,
    )


def login_header():
    st.markdown(
        '''<div class="bt-login-wrap"><div class="bt-login-mark">BT</div><div class="bt-login-title">BrewTech Operations Hub</div><div class="bt-login-copy">Sign in to manage machines, service operations, inventory, and client deployments.</div></div>''',
        unsafe_allow_html=True,
    )
