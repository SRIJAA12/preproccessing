# -*- coding: utf-8 -*-
"""
Prepayment Control & Portfolio Retention
Idea Olympics -- Team: Portfolio Protectors
Theme: "வரும்முன் காப்போம்" / "Prevention is better than cure"
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prepayment Control & Portfolio Retention",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  PATHS & DATA DIRECTORY
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
CUSTOMERS_CSV_PATH = os.path.join(DATA_DIR, "customers.csv")
TEMPLATE_CSV_PATH = os.path.join(DATA_DIR, "customers_template.csv")
USERS_CSV_PATH = os.path.join(DATA_DIR, "users.csv")
RM_CSV_PATH = os.path.join(DATA_DIR, "rm_interactions.csv")

# ─────────────────────────────────────────────────────────────
#  COMPLETE LIGHT THEME CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* ══ GLOBAL RESET — full light mode ══ */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main,
.block-container,
[data-testid="stVerticalBlock"] {
    background-color: #f0f4f8 !important;
    font-family: 'Inter', sans-serif;
}

/* Kill Streamlit's own dark-mode overrides */
.stApp {
    background-color: #f0f4f8 !important;
    font-family: 'Inter', sans-serif;
}

/* All standard text elements */
p, li, label, td, th {
    color: #1e293b !important;
    font-family: 'Inter', sans-serif;
}

/* PROTECT MATERIAL ICONS / ARROW BUTTONS: Never override icon fonts with Inter! */
[class*="material-symbols"],
[class*="material-icons"],
[data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] span,
[data-testid="collapsedControl"] span {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
}

/* ══ SIDEBAR — clean light with navy accent ══ */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 2px solid #e2e8f0 !important;
    box-shadow: 2px 0 12px rgba(0,0,0,0.06) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 16px;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stMarkdown {
    color: #1e293b !important;
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] .stRadio label {
    color: #1e293b !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 6px 0 !important;
}
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: #1e293b !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

/* ══ Headings ══ */
h1 { color: #0f172a !important; font-size: 1.9rem !important; font-weight: 800 !important; letter-spacing: -0.5px !important; }
h2 { color: #0f172a !important; font-size: 1.4rem !important; font-weight: 700 !important; }
h3 { color: #0f172a !important; font-size: 1.1rem !important; font-weight: 600 !important; }

/* ══ KPI CARD ══ */
.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px 16px 16px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.06);
    border: 1px solid #e8edf3;
    min-height: 108px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s, box-shadow 0.15s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.10);
}
.kpi-label {
    font-size: 0.68rem !important;
    color: #64748b !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.9px !important;
    margin-bottom: 8px !important;
}
.kpi-value {
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    line-height: 1.1 !important;
}
.kpi-sub {
    font-size: 0.7rem !important;
    color: #94a3b8 !important;
    margin-top: 5px !important;
    font-weight: 400 !important;
}

/* KPI colour variants */
.kpi-red   { border-top: 3px solid #ef4444; }
.kpi-red   .kpi-value { color: #dc2626 !important; }
.kpi-navy  { border-top: 3px solid #1e3a8a; }
.kpi-navy  .kpi-value { color: #1e3a8a !important; }
.kpi-amber { border-top: 3px solid #f59e0b; }
.kpi-amber .kpi-value { color: #d97706 !important; }
.kpi-teal  { border-top: 3px solid #0d9488; }
.kpi-teal  .kpi-value { color: #0d9488 !important; }
.kpi-green { border-top: 3px solid #22c55e; }
.kpi-green .kpi-value { color: #16a34a !important; }
.kpi-purple { border-top: 3px solid #8b5cf6; }
.kpi-purple .kpi-value { color: #7c3aed !important; }

/* ══ SECTION HEADER ══ */
.section-head {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a !important;
    padding: 4px 0 12px;
    border-bottom: 2px solid #e2e8f0;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ══ TAGLINE BOX ══ */
.tagline-box {
    background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%);
    border-radius: 16px;
    padding: 24px 32px;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 4px 20px rgba(30,58,138,0.25);
}
.tagline-tamil   { color: #ffffff; font-size: 1.65rem; font-weight: 800 !important; letter-spacing: 1px; }
.tagline-english { color: rgba(255,255,255,0.75) !important; font-size: 0.95rem !important; margin-top: 6px; }

/* ══ ALERT BANNERS ══ */
.warn-banner {
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
    border-left: 4px solid #f97316;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 14px 0;
    color: #7c2d12 !important;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(249,115,22,0.12);
}
.info-banner {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border-left: 4px solid #3b82f6;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 14px 0;
    color: #1e3a8a !important;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(59,130,246,0.10);
}
.success-banner {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-left: 4px solid #22c55e;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 14px 0;
    color: #14532d !important;
    font-size: 0.9rem;
    box-shadow: 0 2px 8px rgba(34,197,94,0.12);
}

/* ══ WORKFLOW FLOW ══ */
.flow-container { display: flex; flex-direction: column; align-items: center; gap: 0; margin: 14px 0; }
.flow-step {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: #ffffff !important;
    border-radius: 10px;
    padding: 11px 28px;
    font-weight: 600;
    font-size: 0.86rem;
    width: 220px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(30,58,138,0.25);
}
.flow-step span { color: #ffffff !important; }
.flow-arrow { color: #2563eb !important; font-size: 1.4rem; line-height: 1; margin: 2px 0; font-weight: 800; }

/* ══ BEAUTIFUL HTML TABLE ══ */
.tbl-wrap {
    overflow-x: auto;
    border-radius: 14px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.09);
    background: #ffffff;
    margin: 8px 0 16px;
}
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Inter', sans-serif;
    font-size: 0.84rem;
    background: #ffffff;
}
.styled-table thead tr {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
}
.styled-table th {
    padding: 13px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #ffffff !important;
    white-space: nowrap;
}
.styled-table td {
    padding: 11px 16px;
    border-bottom: 1px solid #f1f5f9;
    color: #1e293b !important;
    vertical-align: middle;
}
.styled-table tbody tr:last-child td { border-bottom: none; }
.styled-table tbody tr:hover { background: #f8faff !important; }
.row-high   { background: #fff5f5 !important; }
.row-medium { background: #fffdf0 !important; }
.row-low    { background: #f6fef9 !important; }
.row-high:hover   { background: #ffe4e6 !important; }
.row-medium:hover { background: #fef9c3 !important; }
.row-low:hover    { background: #dcfce7 !important; }

/* ══ BADGES ══ */
.bdg {
    display: inline-block;
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.73rem;
    font-weight: 700;
    white-space: nowrap;
    line-height: 1.5;
}
.bdg-high        { background: #fee2e2; color: #991b1b !important; }
.bdg-medium      { background: #fef3c7; color: #92400e !important; }
.bdg-low         { background: #d1fae5; color: #065f46 !important; }
.bdg-contacted   { background: #dbeafe; color: #1d4ed8 !important; }
.bdg-notcontact  { background: #f1f5f9; color: #475569 !important; border: 1px solid #e2e8f0; }
.bdg-retained    { background: #d1fae5; color: #065f46 !important; }
.bdg-partial     { background: #fef3c7; color: #92400e !important; }
.bdg-closed      { background: #fee2e2; color: #991b1b !important; }
.bdg-followup    { background: #ede9fe; color: #5b21b6 !important; }

.chip {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8 !important;
    border-radius: 12px;
    padding: 2px 9px;
    font-size: 0.71rem;
    font-weight: 600;
    margin: 1px 2px;
    white-space: nowrap;
    border: 1px solid #bfdbfe;
}

/* ══ ACTION CARDS ══ */
.action-card {
    background: #f0fdf9;
    border: 1.5px solid #a7f3d0;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0;
    color: #134e4a !important;
}
.action-card li, .action-card p, .action-card b { color: #134e4a !important; }
.action-warn {
    background: #fff7ed;
    border: 1.5px solid #fed7aa;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0;
}
.action-warn li, .action-warn p, .action-warn b { color: #7c2d12 !important; }

.disclaimer {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.77rem !important;
    color: #64748b !important;
    font-style: italic;
    margin-top: 12px;
}

/* ══ SIMULATION BOX ══ */
.sim-box {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 2px solid #86efac;
    border-radius: 14px;
    padding: 22px 26px;
    margin: 14px 0;
}
.sim-box p, .sim-box span { color: #14532d !important; }
.sim-result {
    font-size: 1.1rem;
    font-weight: 800;
    color: #065f46 !important;
    background: #ffffff;
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 14px;
    border-left: 4px solid #22c55e;
    box-shadow: 0 2px 8px rgba(34,197,94,0.12);
}

/* ══ INSIGHT BOX ══ */
.insight-box {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-radius: 12px;
    padding: 14px 18px;
    border: 1.5px solid #86efac;
    margin-top: 14px;
}
.insight-box p, .insight-box span, .insight-box b { color: #065f46 !important; }

/* ══ CLOSING BANNER ══ */
.close-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #0d9488 100%);
    border-radius: 16px;
    padding: 28px 36px;
    text-align: center;
    box-shadow: 0 6px 30px rgba(15,23,42,0.20);
    margin-top: 16px;
}
.close-banner p { color: #e2e8f0 !important; }
.close-banner .tamil { color: #5eead4 !important; font-size: 1.5rem !important; font-weight: 800 !important; }
.close-banner .sub   { color: rgba(255,255,255,0.55) !important; font-size: 0.9rem !important; }

/* ══ STREAMLIT ELEMENTS ══ */
.stSelectbox label { color: #0f172a !important; font-weight: 600 !important; font-size: 0.88rem !important; }
.stTextArea  label { color: #0f172a !important; font-weight: 600 !important; font-size: 0.88rem !important; }
.stTextInput label { color: #0f172a !important; font-weight: 600 !important; font-size: 0.88rem !important; }
.stDateInput label { color: #0f172a !important; font-weight: 600 !important; font-size: 0.88rem !important; }

.stSelectbox > div > div {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
.stTextArea > div > div { background: #ffffff !important; border-radius: 10px !important; }
.stTextInput > div > div { background: #ffffff !important; border-radius: 10px !important; }
textarea, input { background: #ffffff !important; color: #0f172a !important; }

.stButton > button {
    background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    font-size: 0.88rem !important;
    box-shadow: 0 3px 12px rgba(37,99,235,0.25) !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(37,99,235,0.35) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #0d9488, #059669) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    font-size: 0.85rem !important;
    box-shadow: 0 3px 12px rgba(13,148,136,0.25) !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(13,148,136,0.35) !important;
}

.stTabs [data-baseweb="tab"] {
    font-weight: 600;
    color: #475569 !important;
    font-size: 0.88rem;
}
.stTabs [aria-selected="true"] { color: #1e3a8a !important; border-bottom-color: #1e3a8a !important; }

/* ══ Divider ══ */
.sdiv { border: none; border-top: 2px solid #e8edf3; margin: 22px 0; }

/* ══ HEADER — light background ══ */
[data-testid="stHeader"] {
    background: #f0f4f8 !important;
    border-bottom: 1px solid #e2e8f0 !important;
}
/* Ensure sidebar toggle arrow buttons are fully functional, visible and clickable */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    z-index: 1000 !important;
    visibility: visible !important;
}
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {
    cursor: pointer !important;
}
[data-testid="stDecoration"] { display: none !important; }

/* ══ DROPDOWN POPUP — light white panel ══ */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
[role="listbox"] {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.14) !important;
}

/* Each dropdown option */
[role="option"] {
    background: #ffffff !important;
    color: #1e293b !important;
    font-size: 0.88rem !important;
    padding: 10px 16px !important;
}
[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background: #eff6ff !important;
    color: #1d4ed8 !important;
    font-weight: 600 !important;
}

/* ══ AUTH CARD ══ */
.auth-box {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 18px;
    padding: 32px 36px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    max-width: 520px;
    margin: 30px auto;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  USER AUTHENTICATION LOGIC
# ─────────────────────────────────────────────────────────────
def load_users():
    if os.path.exists(USERS_CSV_PATH):
        try:
            return pd.read_csv(USERS_CSV_PATH)
        except Exception:
            pass
    # default fallback
    df = pd.DataFrame([
        {"Username": "anandhan", "Email": "anandhan@portfolio.in", "FullName": "R. Anandhan", "Role": "Relationship Manager", "Password": "password123"},
        {"Username": "admin", "Email": "admin@portfolio.in", "FullName": "Portfolio Admin", "Role": "Branch Manager", "Password": "admin123"},
        {"Username": "srijaa", "Email": "srijaa@portfolio.in", "FullName": "Srijaa M", "Role": "Portfolio Risk Head", "Password": "srijaa123"}
    ])
    df.to_csv(USERS_CSV_PATH, index=False)
    return df

def save_user(username, email, fullname, role, password):
    users_df = load_users()
    new_user = pd.DataFrame([{
        "Username": username.strip(),
        "Email": email.strip().lower(),
        "FullName": fullname.strip(),
        "Role": role.strip(),
        "Password": password.strip()
    }])
    updated = pd.concat([users_df, new_user], ignore_index=True)
    updated.to_csv(USERS_CSV_PATH, index=False)
    return updated

def verify_login(user_or_email, password):
    users_df = load_users()
    user_or_email = user_or_email.strip().lower()
    matches = users_df[
        (users_df["Username"].str.lower() == user_or_email) |
        (users_df["Email"].str.lower() == user_or_email)
    ]
    if not matches.empty:
        user_row = matches.iloc[0]
        if str(user_row["Password"]).strip() == password.strip():
            return user_row.to_dict()
    return None

# Initialize session state for auth
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ─────────────────────────────────────────────────────────────
#  DATA LOADING & RM LOGS
# ─────────────────────────────────────────────────────────────
def load_customers_data():
    if "customer_df" not in st.session_state or st.session_state.customer_df is None:
        df = pd.read_csv(CUSTOMERS_CSV_PATH)
        df.columns = df.columns.str.strip()
        df["Outstanding (L)"] = pd.to_numeric(df["Outstanding (L)"], errors="coerce").fillna(0)
        df["ROI"] = pd.to_numeric(df["ROI"], errors="coerce").fillna(10.0)
        df["Portfolio Retained (L)"] = pd.to_numeric(df["Portfolio Retained (L)"], errors="coerce").fillna(0)
        st.session_state.customer_df = df
    return st.session_state.customer_df

def load_rm_interactions():
    if "rm_interactions_df" not in st.session_state or st.session_state.rm_interactions_df is None:
        if os.path.exists(RM_CSV_PATH):
            try:
                df = pd.read_csv(RM_CSV_PATH)
            except Exception:
                df = pd.DataFrame()
        else:
            df = pd.DataFrame()
        st.session_state.rm_interactions_df = df
    return st.session_state.rm_interactions_df

def save_rm_interaction(log_entry):
    interactions_df = load_rm_interactions()
    new_entry_df = pd.DataFrame([log_entry])
    updated_df = pd.concat([new_entry_df, interactions_df], ignore_index=True)
    st.session_state.rm_interactions_df = updated_df
    try:
        updated_df.to_csv(RM_CSV_PATH, index=False)
    except Exception:
        pass
    return updated_df

if "customer_actions" not in st.session_state:
    st.session_state.customer_actions = {}

# ─────────────────────────────────────────────────────────────
#  AUTHENTICATION GATE (LOGIN & SIGN UP)
# ─────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <div style='text-align:center;padding:24px 0 12px;'>
      <div style='font-size:2.2rem;font-weight:800;color:#0f172a !important;letter-spacing:-0.5px;'>
        🏦 Portfolio Protectors
      </div>
      <div style='color:#64748b !important;font-size:1.05rem;margin-top:4px;'>
        Prepayment Control &amp; Proactive Portfolio Retention Platform
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tagline-box" style='max-width:540px;margin:10px auto 26px;'>
      <div class="tagline-tamil">&#2997;&#2992;&#3009;&#2990;&#3021;&#2990;&#3009;&#2985;&#3021; &#2965;&#3006;&#2986;&#3021;&#2986;&#3019;&#2990;&#3021;</div>
      <div class="tagline-english">"Prevention is better than cure" — Idea Olympics 2026</div>
    </div>
    """, unsafe_allow_html=True)

    auth_col1, auth_col2, auth_col3 = st.columns([1, 1.8, 1])
    with auth_col2:
        auth_tab_login, auth_tab_signup = st.tabs(["🔑  Sign In", "📝  Create New Account"])

        with auth_tab_login:
            st.markdown("<p style='font-weight:600;color:#0f172a;'>Access your Relationship Management Portal</p>", unsafe_allow_html=True)
            login_user = st.text_input("Username or Email Address", key="login_user_input", placeholder="e.g. anandhan or anandhan@portfolio.in")
            login_pass = st.text_input("Password", type="password", key="login_pass_input", placeholder="Enter your password")

            if st.button("🚀  Sign In to Dashboard", use_container_width=True):
                if not login_user or not login_pass:
                    st.error("Please enter both username/email and password.")
                else:
                    user_data = verify_login(login_user, login_pass)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user_data
                        st.success(f"Welcome back, {user_data.get('FullName')}!")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password. Try demo login below.")

            st.markdown("<div style='border-top:1px solid #e2e8f0;margin:18px 0 14px;'></div>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.8rem;color:#64748b;font-weight:600;margin-bottom:8px;'>⚡ ONE-CLICK DEMO ACCESS FOR EVALUATORS:</p>", unsafe_allow_html=True)
            if st.button("👤 One-Click Demo Login (RM Anandhan)", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.current_user = {
                    "Username": "anandhan",
                    "Email": "anandhan@portfolio.in",
                    "FullName": "R. Anandhan",
                    "Role": "Relationship Manager"
                }
                st.rerun()

        with auth_tab_signup:
            st.markdown("<p style='font-weight:600;color:#0f172a;'>Register as a Relationship Manager or Branch Officer</p>", unsafe_allow_html=True)
            su_fullname = st.text_input("Full Name", placeholder="e.g. Arun Ramanathan")
            su_email    = st.text_input("Official Email ID", placeholder="e.g. arun.r@portfolio.in")
            su_username = st.text_input("Choose Username", placeholder="e.g. arun_rm")
            su_role     = st.selectbox("Designation / Role", [
                "Relationship Manager (RM)",
                "Senior RM — High Networth Portfolio",
                "Branch Manager",
                "Credit & Portfolio Retention Officer",
                "Risk Analyst"
            ])
            su_pass1    = st.text_input("Password", type="password", key="su_pass1")
            su_pass2    = st.text_input("Confirm Password", type="password", key="su_pass2")

            if st.button("✨  Create Account & Sign In", use_container_width=True):
                if not su_fullname or not su_email or not su_username or not su_pass1:
                    st.error("Please fill in all mandatory fields.")
                elif su_pass1 != su_pass2:
                    st.error("Passwords do not match.")
                elif "@" not in su_email or "." not in su_email:
                    st.error("Please enter a valid email address.")
                else:
                    users_df = load_users()
                    if su_username.strip().lower() in users_df["Username"].str.lower().values:
                        st.error("Username already registered. Please choose another username.")
                    elif su_email.strip().lower() in users_df["Email"].str.lower().values:
                        st.error("Email ID already exists. Please sign in or use another email.")
                    else:
                        save_user(su_username, su_email, su_fullname, su_role, su_pass1)
                        st.session_state.authenticated = True
                        st.session_state.current_user = {
                            "Username": su_username.strip(),
                            "Email": su_email.strip().lower(),
                            "FullName": su_fullname.strip(),
                            "Role": su_role
                        }
                        st.success(f"Account created successfully! Welcome, {su_fullname}!")
                        st.rerun()

    st.stop()

# ─────────────────────────────────────────────────────────────
#  APP INITIALIZATION FOR LOGGED-IN USERS
# ─────────────────────────────────────────────────────────────
df_master = load_customers_data()
rm_interactions_df = load_rm_interactions()
current_user = st.session_state.current_user or {"FullName": "R. Anandhan", "Role": "Relationship Manager", "Username": "anandhan"}

# ─────────────────────────────────────────────────────────────
#  REUSABLE HELPERS
# ─────────────────────────────────────────────────────────────
def fmt_l(v):  return f"&#8377;{v:.1f} L"
def fmt_lp(v): return f"Rs.{v:.1f} L"

def kpi(label, value, sub="", style=""):
    cls = f"kpi-card kpi-{style}" if style else "kpi-card"
    return f"""<div class="{cls}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-sub'>"+sub+"</div>" if sub else ""}
    </div>"""

def bdg(text, kind):
    return f'<span class="bdg bdg-{kind}">{text}</span>'

def chip(text):
    return f'<span class="chip">{text}</span>'

def risk_bdg(risk):
    r = str(risk).strip().lower()
    k = {"high":"high","medium":"medium","low":"low"}.get(r,"low")
    return bdg(str(risk).strip(), k)

def contact_bdg(status):
    s = str(status).strip().lower()
    return bdg("&#10003; Contacted","contacted") if s=="contacted" else bdg("Not Contacted","notcontact")

def checkin_bdg(status):
    s = str(status).strip().lower()
    if "overdue" in s:
        return bdg("&#9888; Overdue", "high")
    elif "today" in s:
        return bdg("&#9200; Due Today", "medium")
    elif "soon" in s or "upcoming" in s:
        return bdg("&#128197; Due Soon", "contacted")
    return bdg("&#10003; Up to date", "retained")

def identify_cat(trigger):
    t = str(trigger).lower()
    if any(x in t for x in ["competitor","balance transfer","foreclosure"]):
        return "Balance Transfer / Foreclosure"
    if "own fund" in t:  return "Own Funds"
    if any(x in t for x in ["service","complaint"]): return "Service Issue"
    if any(x in t for x in ["top-up","top up"]):     return "Top-Up Requirement"
    if "rate reduction" in t:                         return "Rate Reduction Request"
    return "Outstanding Amount Check"

def html_customer_table(df):
    rows = ""
    for _, r in df.iterrows():
        rk   = str(r["Risk Level"]).strip().lower()
        rcls = {"high":"row-high","medium":"row-medium","low":"row-low"}.get(rk,"")
        chips = "".join(chip(t.strip()) for t in str(r.get("Trigger","")).split("|"))
        out  = f"<b style='color:#1e3a8a !important;'>&#8377;{r['Outstanding (L)']:.1f} L</b>"
        roi  = f"<span style='font-weight:700;color:#0f172a !important;'>{r['ROI']:.2f}%</span>"
        prod = f"<span style='background:#f1f5f9;border-radius:6px;padding:2px 8px;font-size:0.75rem;font-weight:600;color:#334155 !important;'>{r.get('Product','HL')}</span>"
        phone = r.get("Phone Number", "+91 98400 00000")
        email = r.get("Email ID", "customer@example.com")
        loan_acc = r.get("Loan Account No", "LN-001")
        
        contact_html = f"""<div style='font-size:0.8rem;font-weight:600;color:#1e3a8a !important;'>📞 {phone}</div>
        <div style='font-size:0.74rem;color:#64748b !important;'>✉️ {email}</div>"""

        rows += f"""<tr class="{rcls}">
            <td>
              <b style='color:#0f172a !important;font-size:0.9rem;'>{r['Customer Name']}</b><br>
              <span style='font-size:0.73rem;color:#64748b !important;font-family:monospace;'>{loan_acc}</span>
            </td>
            <td>{contact_html}</td>
            <td style='color:#475569 !important;font-weight:500;'>{r['Branch']}</td>
            <td>{prod}</td>
            <td>{out}</td>
            <td>{roi}</td>
            <td style='max-width:240px;'>{chips}</td>
            <td>{risk_bdg(r['Risk Level'])}</td>
            <td>{contact_bdg(r.get('RM Contact Status','Not Contacted'))}</td>
        </tr>"""
    return f"""<div class="tbl-wrap">
    <table class="styled-table">
      <thead><tr>
        <th>Customer &amp; Loan No</th><th>Contact Details</th><th>Branch</th><th>Product</th>
        <th>Outstanding</th><th>ROI</th><th>Signals</th>
        <th>Risk</th><th>RM Status</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>"""

def html_schedule_table(df):
    rows = ""
    for _, r in df.iterrows():
        phone = r.get("Phone Number", "+91 98400 00000")
        email = r.get("Email ID", "customer@example.com")
        loan_acc = r.get("Loan Account No", "LN-001")
        last_date = r.get("Last Contact Date", "—")
        next_date = r.get("Next Check-in Due", "—")
        status = r.get("Check-in Status", "Due Soon")
        rm_name = r.get("Assigned RM", "R. Anandhan")

        rows += f"""<tr>
            <td>
              <b style='color:#0f172a !important;'>{r['Customer Name']}</b><br>
              <span style='font-size:0.73rem;color:#64748b !important;font-family:monospace;'>{loan_acc}</span>
            </td>
            <td>
              <div style='font-size:0.8rem;font-weight:600;color:#1e3a8a !important;'>📞 {phone}</div>
              <div style='font-size:0.74rem;color:#64748b !important;'>✉️ {email}</div>
            </td>
            <td style='color:#334155 !important;font-weight:500;'>{r['Branch']}</td>
            <td><b style='color:#1e3a8a !important;'>&#8377;{r['Outstanding (L)']:.1f} L</b></td>
            <td style='color:#475569 !important;font-weight:600;'>{rm_name}</td>
            <td style='color:#334155 !important;'>{last_date}</td>
            <td><b style='color:#0f172a !important;'>{next_date}</b></td>
            <td>{checkin_bdg(status)}</td>
        </tr>"""
    return f"""<div class="tbl-wrap">
    <table class="styled-table">
      <thead><tr>
        <th>Customer / Loan No</th><th>Contact Information</th><th>Branch</th>
        <th>Outstanding</th><th>Assigned RM</th><th>Last Touchpoint</th>
        <th>Next Check-in Due</th><th>Status</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>"""

def html_mgmt_table(review_df):
    rows = ""
    for _, r in review_df.iterrows():
        hstyle = 'color:#dc2626 !important;font-weight:800;' if r["High Risk Cases"] >= 3 else 'font-weight:700;'
        rstyle = 'color:#0d9488 !important;font-weight:800;' if r["Retained"] > 0 else 'color:#64748b !important;'
        rows += f"""<tr>
            <td><b style='color:#0f172a !important;'>{r['Branch']}</b></td>
            <td style='{hstyle}'>{r['High Risk Cases']}</td>
            <td style='font-weight:600;color:#0f172a !important;'>{r['Contacted']}</td>
            <td style='{rstyle}'>{r['Retained']}</td>
            <td style='color:#d97706 !important;font-weight:700;'>{r['Part. Retained']}</td>
            <td style='color:#6d28d9 !important;font-weight:700;'>{r['Follow-up']}</td>
            <td style='color:#0d9488 !important;font-weight:800;'>{r['Portfolio Retained']}</td>
        </tr>"""
    return f"""<div class="tbl-wrap">
    <table class="styled-table">
      <thead><tr>
        <th>Branch</th><th>High Risk</th><th>Contacted</th>
        <th>Retained</th><th>Part. Retained</th><th>Follow-up</th><th>Portfolio Retained</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table></div>"""

# ─────────────────────────────────────────────────────────────
#  SIDEBAR NAVIGATION & CUSTOMER DATA TOOLS
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    # User Profile Badge
    user_initial = current_user.get("FullName", "U")[0].upper()
    st.markdown(f"""
    <div style='background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:12px;padding:10px 12px;margin-bottom:12px;'>
      <div style='display:flex;align-items:center;gap:10px;'>
        <div style='background:#1e3a8a;color:#ffffff;border-radius:50%;width:34px;height:34px;
                    display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.95rem;'>
          {user_initial}
        </div>
        <div style='overflow:hidden;'>
          <div style='font-weight:700;font-size:0.86rem;color:#0f172a;white-space:nowrap;text-overflow:ellipsis;'>
            {current_user.get("FullName")}
          </div>
          <div style='font-size:0.72rem;color:#0d9488;font-weight:600;'>
            {current_user.get("Role")}
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sign Out", key="sb_logout_btn", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.rerun()

    st.markdown("<div style='border-top:1.5px solid #e2e8f0;margin:12px 0 14px;'></div>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Home — Snapshot",
         "⚠️  Early Warning List",
         "🤝  Customer Retention",
         "📞  RM 90-Day Health Checks",
         "📊  Management Summary"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='border-top:1.5px solid #e2e8f0;margin:16px 0 14px;'></div>", unsafe_allow_html=True)

    # Data Upload & Template Section
    st.markdown("<div style='font-size:0.82rem;font-weight:700;color:#0f172a;margin-bottom:6px;'>📁 Customer Dataset Tools</div>", unsafe_allow_html=True)

    # 1. Download Template Button
    if os.path.exists(TEMPLATE_CSV_PATH):
        with open(TEMPLATE_CSV_PATH, "r", encoding="utf-8", errors="ignore") as f:
            template_content = f.read()
        st.download_button(
            label="📥 Download CSV Template",
            data=template_content,
            file_name="customers_template.csv",
            mime="text/csv",
            use_container_width=True,
            help="Download standard CSV structure with contact details and 90-day status columns."
        )

    # 2. File Uploader & Confirmation Button
    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"],
        help="Choose a CSV file, then click 'Upload & Confirm Dataset' to load it.",
        key="sb_customer_uploader"
    )
    if uploaded_file is not None:
        if st.button("📤 Upload & Confirm Dataset", key="btn_confirm_upload", use_container_width=True):
            try:
                up_df = pd.read_csv(uploaded_file)
                up_df.columns = up_df.columns.str.strip()
                # Validate core columns
                req = ["Customer Name", "Branch", "Product", "Outstanding (L)", "ROI", "Risk Level"]
                missing = [c for c in req if c not in up_df.columns]
                if not missing:
                    up_df["Outstanding (L)"] = pd.to_numeric(up_df["Outstanding (L)"], errors="coerce").fillna(0)
                    up_df["ROI"] = pd.to_numeric(up_df["ROI"], errors="coerce").fillna(10.0)
                    if "Portfolio Retained (L)" not in up_df.columns:
                        up_df["Portfolio Retained (L)"] = 0.0
                    else:
                        up_df["Portfolio Retained (L)"] = pd.to_numeric(up_df["Portfolio Retained (L)"], errors="coerce").fillna(0)

                    # Default fallback values for newly uploaded data
                    if "Phone Number" not in up_df.columns:
                        up_df["Phone Number"] = [f"+91 98400 {10000+i}" for i in range(len(up_df))]
                    if "Email ID" not in up_df.columns:
                        up_df["Email ID"] = up_df["Customer Name"].str.lower().str.replace(" ", ".") + "@example.com"
                    if "Loan Account No" not in up_df.columns:
                        up_df["Loan Account No"] = "LN-" + up_df["Branch"].astype(str) + "-2024-" + up_df.index.astype(str).str.zfill(3)
                    if "Assigned RM" not in up_df.columns:
                        up_df["Assigned RM"] = current_user.get("FullName", "R. Anandhan")
                    if "Last Contact Date" not in up_df.columns:
                        up_df["Last Contact Date"] = "2026-08-01"
                    if "Next Check-in Due" not in up_df.columns:
                        up_df["Next Check-in Due"] = "2026-11-01"
                    if "Check-in Status" not in up_df.columns:
                        up_df["Check-in Status"] = "Due Soon"

                    st.session_state.customer_df = up_df
                    st.session_state.customer_actions = {}
                    st.session_state.upload_success_message = f"✅ '{uploaded_file.name}' confirmed & loaded successfully ({len(up_df)} customer records active)!"
                    st.rerun()
                else:
                    st.sidebar.error(f"Missing required columns: {', '.join(missing)}")
            except Exception as e:
                st.sidebar.error(f"Upload error: {e}")

    if st.session_state.get("upload_success_message"):
        st.sidebar.success(st.session_state.upload_success_message)

    # 3. Reset Button
    if st.button("🔄 Reset to Default Data", use_container_width=True):
        st.session_state.customer_df = None
        st.session_state.customer_actions = {}
        st.session_state.upload_success_message = None
        st.rerun()

    st.markdown("<div style='border-top:1.5px solid #e2e8f0;margin:16px 0 14px;'></div>", unsafe_allow_html=True)

    # Tagline card
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#0d9488);
                border-radius:12px;padding:14px;text-align:center;'>
      <div style='font-size:1.05rem;font-weight:800;color:#ffffff !important;letter-spacing:1px;margin-bottom:3px;'>
        &#2997;&#2992;&#3009;&#2990;&#3021;&#2990;&#3009;&#2985;&#3021; &#2965;&#3006;&#2986;&#3021;&#2986;&#3019;&#2990;&#3021;
      </div>
      <div style='font-size:0.75rem;color:rgba(255,255,255,0.78) !important;font-style:italic;'>
        Prevention is better than cure
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SCREEN 1 — HOME SNAPSHOT
# ══════════════════════════════════════════════════════════════
if page == "🏠  Home — Snapshot":

    # Hero
    st.markdown("""
    <div style='text-align:center;padding:12px 0 6px;'>
      <div style='font-size:2rem;font-weight:800;color:#0f172a !important;letter-spacing:-0.5px;'>
        Prepayment Control &amp; Portfolio Retention
      </div>
      <div style='color:#64748b !important;font-size:1.0rem;margin-top:6px;font-weight:400;'>
        Detect early &nbsp;·&nbsp; Engage proactively &nbsp;·&nbsp; Retain relationships
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Tagline
    st.markdown("""
    <div class="tagline-box">
      <div class="tagline-tamil">&#2997;&#2992;&#3009;&#2990;&#3021;&#2990;&#3009;&#2985;&#3021; &#2965;&#3006;&#2986;&#3021;&#2986;&#3019;&#2990;&#3021;</div>
      <div class="tagline-english">"Prevention is better than cure"</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)

    # Section Head with Export Button
    head_c1, head_c2 = st.columns([3, 1])
    with head_c1:
        st.markdown("""<div class='section-head'>&#128204; YTD Prepayment Snapshot — Sep 2026</div>""", unsafe_allow_html=True)
    with head_c2:
        ytd_metrics_df = pd.DataFrame([
            {"Metric": "YTD Prepayment (Actual)", "Value (Cr)": 1727, "Period": "Sep 2026"},
            {"Metric": "YTD Budget (Planned)", "Value (Cr)": 1095, "Period": "Sep 2026"},
            {"Metric": "Above Planned (Excess)", "Value (Cr)": 632, "Period": "Sep 2026"},
            {"Metric": "Prepayment vs Budget", "Value (Cr)": "158%", "Period": "Sep 2026"},
            {"Metric": "LYTD Prepayment (Prior Year)", "Value (Cr)": 1369, "Period": "Sep 2025"},
            {"Metric": "Home Loan (HL) Prepayment", "Value (Cr)": 906, "Period": "Sep 2026"},
            {"Metric": "Non-Home Loan (NHL) Prepayment", "Value (Cr)": 821, "Period": "Sep 2026"}
        ])
        st.download_button(
            label="📥 Download YTD Summary (CSV)",
            data=ytd_metrics_df.to_csv(index=False),
            file_name="ytd_prepayment_snapshot.csv",
            mime="text/csv",
            use_container_width=True
        )

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("YTD Prepayment","&#8377;1,727 Cr","Actual — Sep 2026","red"),      unsafe_allow_html=True)
    with c2: st.markdown(kpi("YTD Budget","&#8377;1,095 Cr","Planned","navy"),                    unsafe_allow_html=True)
    with c3: st.markdown(kpi("Above Planned","&#8377;632 Cr","Excess over budget","amber"),       unsafe_allow_html=True)
    with c4: st.markdown(kpi("Prepayment vs Budget","158%","of YTD Budget","red"),                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c5,c6,c7 = st.columns(3)
    with c5: st.markdown(kpi("LYTD Prepayment","&#8377;1,369 Cr","Last year same period"),       unsafe_allow_html=True)
    with c6: st.markdown(kpi("Home Loan (HL)","&#8377;906 Cr","YTD prepayment","navy"),          unsafe_allow_html=True)
    with c7: st.markdown(kpi("Non-Home Loan (NHL)","&#8377;821 Cr","YTD prepayment","navy"),     unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-banner">
      &#9888;&nbsp; Prepayment is at <b>158% of YTD budget</b> &mdash;
      Prepayment is not an achievement. It requires <b>proactive control.</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)
    st.markdown("""<div class='section-head'>&#128260; Proactive Retention Workflow</div>""",
                unsafe_allow_html=True)

    col_fl, col_txt = st.columns([1,2], gap="large")
    with col_fl:
        steps = ["&#9889; Early Warning",
                 "&#128100; Customer Identification",
                 "&#128222; RM Engagement",
                 "&#128737; Retention Action",
                 "&#9989; Outcome",
                 "&#128203; Periodical Review"]
        html = '<div class="flow-container">'
        for i,s in enumerate(steps):
            html += f'<div class="flow-step"><span>{s}</span></div>'
            if i < len(steps)-1:
                html += '<div class="flow-arrow">&#8595;</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    with col_txt:
        st.markdown("""
        <div style='padding:8px 0;color:#334155 !important;line-height:1.9;font-size:0.92rem;'>
          <p><b style='color:#0f172a !important;'>&#128680; Current Situation</b><br>
          Prepayment intent is identified only when the customer walks in for foreclosure or closure.
          By then, it is often too late to retain the relationship.</p>
          <p><b style='color:#0d9488 !important;'>&#9989; Our Solution</b><br>
          Detect early warning signals &mdash; bureau alerts, foreclosure enquiries, competitor quotes,
          service complaints &mdash; and route them to the RM <b>before</b> the customer reaches closure intent.</p>
          <p><b style='color:#0f172a !important;'>Different Reasons. Different Responses.</b></p>
          <ul style='color:#334155 !important;'>
            <li>&#128260; <b>Balance Transfer</b> &mdash; Rate review &amp; competitor discussion</li>
            <li>&#128176; <b>Own Funds</b> &mdash; Partial prepayment &amp; liquidity discussion</li>
            <li>&#128295; <b>Service Issue</b> &mdash; Complaint resolution &amp; RM callback</li>
            <li>&#128200; <b>Top-Up Need</b> &mdash; Proactive eligibility assessment</li>
          </ul>
          <p style='color:#64748b !important;font-style:italic;font-size:0.86rem;'>
          Prepayment should not first be managed at the point of closure.
          It should be managed at the <b>first sign of intent.</b>
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="close-banner">
      <p style='font-size:0.95rem;margin-bottom:10px;'>
        "Prepayment should not first be managed at the point of closure.<br>
        It should be managed at the <b>first sign of intent.</b>"
      </p>
      <div class="tamil">&#2997;&#2992;&#3009;&#2990;&#3021;&#2990;&#3009;&#2985;&#3021; &#2965;&#3006;&#2986;&#3021;&#2986;&#3019;&#2990;&#3021;</div>
      <div class="sub">Prevention is better than cure.</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SCREEN 2 — EARLY WARNING LIST
# ══════════════════════════════════════════════════════════════
elif page == "⚠️  Early Warning List":

    st.markdown("""
    <div style='font-size:1.6rem;font-weight:800;color:#0f172a !important;margin-bottom:4px;'>
      &#9888;&#65039; Early Warning — Customer Watch List
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-banner">
      &#128204; Customers flagged through <b>bureau alerts, foreclosure enquiries, competitor quotes,
      rate requests and service signals</b>. Complete with verified contact numbers and direct outreach channels.
    </div>
    """, unsafe_allow_html=True)

    df = df_master.copy()

    all_branches = ["All"] + sorted(df["Branch"].unique())
    all_risks    = ["All","High","Medium","Low"]
    all_reasons  = ["All"] + sorted({identify_cat(t) for t in df["Trigger"]})

    f1,f2,f3 = st.columns(3)
    with f1: sel_branch = st.selectbox("Filter by Branch",    all_branches)
    with f2: sel_risk   = st.selectbox("Filter by Risk Level", all_risks)
    with f3: sel_reason = st.selectbox("Filter by Reason",    all_reasons)

    if sel_branch != "All": df = df[df["Branch"] == sel_branch]
    if sel_risk   != "All": df = df[df["Risk Level"].str.strip().str.lower() == sel_risk.lower()]
    if sel_reason != "All": df = df[df["Trigger"].apply(identify_cat) == sel_reason]

    hc = len(df[df["Risk Level"].str.strip().str.lower() == "high"])
    mc = len(df[df["Risk Level"].str.strip().str.lower() == "medium"])
    lc = len(df[df["Risk Level"].str.strip().str.lower() == "low"])

    k1,k2,k3,k4 = st.columns(4)
    with k1: st.markdown(kpi("Total Flagged", str(len(df)), "customers"),                    unsafe_allow_html=True)
    with k2: st.markdown(kpi("High Risk",  str(hc), "immediate contact","red"),              unsafe_allow_html=True)
    with k3: st.markdown(kpi("Medium Risk", str(mc), "contact within 2 days","amber"),       unsafe_allow_html=True)
    with k4: st.markdown(kpi("Low Risk",   str(lc), "watch list","green"),                   unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Action Toolbar: Download options & In-Screen Upload
    tool_c1, tool_c2, tool_c3 = st.columns([1.5, 1.2, 1.2])
    with tool_c1:
        st.download_button(
            label="📥 Download Filtered Watch List (CSV)",
            data=df.to_csv(index=False),
            file_name="early_warning_watchlist.csv",
            mime="text/csv",
            use_container_width=True
        )
    with tool_c2:
        if os.path.exists(TEMPLATE_CSV_PATH):
            with open(TEMPLATE_CSV_PATH, "r", encoding="utf-8", errors="ignore") as f:
                tmpl_bytes = f.read()
            st.download_button(
                label="📥 Download CSV Template",
                data=tmpl_bytes,
                file_name="customers_template.csv",
                mime="text/csv",
                use_container_width=True
            )
    with tool_c3:
        st.markdown(f"<div style='text-align:right;font-size:0.85rem;font-weight:600;color:#64748b;padding-top:8px;'>Showing <b>{len(df)}</b> borrowers</div>", unsafe_allow_html=True)

    if df.empty:
        st.info("No customers match the selected filters.")
    else:
        st.markdown(html_customer_table(df), unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style='display:flex;gap:18px;margin-top:10px;font-size:0.82rem;color:#475569 !important;flex-wrap:wrap;'>
      <span>&#128996; <span class='bdg bdg-high'>High</span> Immediate RM contact required</span>
      <span>&#128997; <span class='bdg bdg-medium'>Medium</span> Contact within 48 hours</span>
      <span>&#128994; <span class='bdg bdg-low'>Low</span> Quarterly health check watchlist</span>
    </div>
    <p style='color:#94a3b8 !important;font-size:0.8rem;margin-top:8px;font-style:italic;'>
      &#128073; To perform targeted interventions, open <b>Customer Retention</b> or log quarterly check-ins in <b>RM 90-Day Health Checks</b>.
    </p>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SCREEN 3 — CUSTOMER RETENTION ACTION
# ══════════════════════════════════════════════════════════════
elif page == "🤝  Customer Retention":

    st.markdown("""<div style='font-size:1.6rem;font-weight:800;color:#0f172a !important;margin-bottom:4px;'>
      &#129309; Customer Retention Action &amp; Targeted Playbook</div>""", unsafe_allow_html=True)

    df = df_master.copy()
    all_names = [str(n).strip() for n in df["Customer Name"].dropna().unique() if str(n).strip()]
    if not all_names:
        st.warning("No customer records found in active dataset.")
        st.stop()
    demo  = [n for n in ["Arun Kumar","Meena R","Suresh P"] if n in all_names]
    other = [n for n in all_names if n not in demo]
    cust_options = demo + other
    
    sel_c1, sel_c2 = st.columns([2.5, 1])
    with sel_c1:
        sel = st.selectbox("👤 Select Customer to Formulate Retention Strategy", cust_options)
    with sel_c2:
        st.download_button(
            label="📥 Download Retention Actions (CSV)",
            data=df.to_csv(index=False),
            file_name="retention_actions_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    matching = df[df["Customer Name"] == sel]
    if matching.empty:
        st.warning(f"Customer '{sel}' not found in active dataset.")
        st.stop()
    row   = matching.iloc[0]
    saved = st.session_state.customer_actions.get(sel, {})

    # Customer Profile Card with Contact Information
    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)
    st.markdown("""<div class='section-head'>&#128100; Borrower Profile &amp; Contact Details</div>""", unsafe_allow_html=True)

    p1,p2,p3,p4,p5 = st.columns(5)
    with p1: st.markdown(kpi("Borrower Name", row["Customer Name"], f"Acc: {row.get('Loan Account No','LN-001')}"), unsafe_allow_html=True)
    with p2: st.markdown(kpi("Product & Branch",  f"{row['Product']} | {row['Branch']}", f"RM: {row.get('Assigned RM','R. Anandhan')}"), unsafe_allow_html=True)
    with p3: st.markdown(kpi("Outstanding Balance", fmt_l(row["Outstanding (L)"]), "Current Loan Balance","navy"), unsafe_allow_html=True)
    with p4: st.markdown(kpi("Current ROI", f"{row['ROI']:.2f}%", "Interest rate"),    unsafe_allow_html=True)
    with p5:
        rk = str(row["Risk Level"]).strip().lower()
        rc = {"high":"red","medium":"amber","low":"green"}.get(rk,"")
        st.markdown(kpi("Prepayment Risk", row["Risk Level"], "Urgency: High", rc),       unsafe_allow_html=True)

    # Detailed Contact Card
    phone = row.get("Phone Number", "+91 98401 23456")
    email = row.get("Email ID", "customer@example.com")
    last_touch = row.get("Last Contact Date", "2026-09-01")
    next_check = row.get("Next Check-in Due", "2026-12-01")
    check_status = row.get("Check-in Status", "Up to date")

    st.markdown(f"""
    <div style='background:#ffffff;border:1px solid #e2e8f0;border-radius:12px;padding:12px 18px;margin:12px 0 16px;
                display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;'>
      <div>
        <span style='font-size:0.8rem;color:#64748b;font-weight:600;'>VERIFIED CONTACT:</span> &nbsp;
        <b style='color:#1e3a8a;'>📞 {phone}</b> &nbsp;&nbsp;|&nbsp;&nbsp;
        <b style='color:#475569;'>✉️ {email}</b>
      </div>
      <div>
        <span style='font-size:0.8rem;color:#64748b;font-weight:600;'>LAST TOUCHPOINT:</span> &nbsp;
        <b style='color:#0f172a;'>{last_touch}</b> &nbsp;&nbsp;|&nbsp;&nbsp;
        <span style='font-size:0.8rem;color:#64748b;font-weight:600;'>NEXT 90-DAY CHECK:</span> &nbsp;
        <b style='color:#0f172a;'>{next_check}</b> &nbsp;
        {checkin_bdg(check_status)}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Trigger chips
    triggers = [t.strip() for t in str(row["Trigger"]).split("|")]
    chips_html = "  ".join(chip(t) for t in triggers)
    st.markdown(f"""
    <div style='margin:10px 0 16px;'>
      <span style='font-weight:700;color:#0f172a !important;font-size:0.88rem;'>
        &#128268; Detected Signals:
      </span>  {chips_html}
    </div>
    """, unsafe_allow_html=True)

    # Why attention
    st.markdown("""<div class='section-head'>&#128269; Why Does This Customer Need Attention?</div>""",
                unsafe_allow_html=True)
    reasons = "<ul style='color:#134e4a !important;line-height:2.2;font-size:0.92rem;margin:0;'>"
    for t in triggers:
        tl = t.lower()
        if   "bureau"     in tl: reasons += "<li><b>Bureau alert</b> detected — competitor institution pulled credit history.</li>"
        elif "foreclosure" in tl: reasons += "<li>Customer has <b>enquired about foreclosure / payoff amount</b> at branch.</li>"
        elif "competitor"  in tl: reasons += "<li>A <b>competitor quote</b> is suspected — evaluating balance transfer terms.</li>"
        elif "own fund"    in tl: reasons += "<li>Customer <b>intends to prepay using own funds</b> — windfall or savings liquidation.</li>"
        elif "service" in tl or "complaint" in tl:
            reasons += "<li>A <b>service complaint or unresolved grievance</b> is on record — driving dissatisfaction.</li>"
        elif "rate reduction" in tl: reasons += "<li>Customer has <b>formally requested a rate reduction</b>.</li>"
        elif "top-up" in tl or "top up" in tl:
            reasons += "<li>Customer has an <b>unmet top-up requirement</b> and may approach another lender.</li>"
        else: reasons += "<li>Customer has been <b>actively checking outstanding balance</b> — possible closure planning.</li>"
    reasons += "</ul>"
    st.markdown(f'<div class="action-card">{reasons}</div>', unsafe_allow_html=True)

    # Category-specific actions
    st.markdown("""<div class='section-head'>&#128737;&#65039; Recommended Retention Actions</div>""",
                unsafe_allow_html=True)
    cat = identify_cat(row["Trigger"])

    # ── Balance Transfer ──
    if cat == "Balance Transfer / Foreclosure":
        comp_roi = round(row["ROI"] - 1.35, 2)
        if row["Customer Name"] == "Arun Kumar": comp_roi = 8.90
        diff = round(row["ROI"] - comp_roi, 2)

        t1, t2 = st.tabs(["&#128202; Rate Comparison", "&#9989; Action Checklist"])
        with t1:
            r1,r2,r3 = st.columns(3)
            with r1: st.markdown(kpi("Our Current ROI",    f"{row['ROI']:.2f}%", "What customer pays","red"),   unsafe_allow_html=True)
            with r2: st.markdown(kpi("Competitor ROI",     f"{comp_roi:.2f}%",   "Estimated offer","teal"),     unsafe_allow_html=True)
            with r3: st.markdown(kpi("Rate Differential",  f"{diff:.2f}%",       "Competitor advantage","amber"),unsafe_allow_html=True)
            st.markdown(f"""
            <div class="action-card" style='margin-top:14px;'>
              <b>Outstanding:</b> {fmt_l(row['Outstanding (L)'])} &nbsp;|&nbsp;
              <b>Trigger:</b> Foreclosure enquiry + bureau alert — serious closure intent.<br>
              <b style='color:#dc2626 !important;'>Urgency:</b> Contact customer within <b>24 hours</b> via RM hotline.
            </div>""", unsafe_allow_html=True)
        with t2:
            st.markdown("""
            <div class="action-card">
              <b>Steps for Balance Transfer / Foreclosure Case:</b>
              <ol style='line-height:2.3;margin-top:10px;color:#134e4a !important;'>
                <li>&#128222; <b>Contact customer immediately</b> — do not wait for closure application.</li>
                <li>&#128172; <b>Understand the competitor offer</b> — rate, tenure, processing fee, lock-in terms.</li>
                <li>&#128203; <b>Review ROI eligibility</b> — check if revision is permissible under credit policy.</li>
                <li>&#128176; <b>Check top-up requirement</b> — customer may have a fund need we can address.</li>
                <li>&#128295; <b>Resolve any service concerns</b> — pricing is not always the only reason.</li>
                <li>&#128680; <b>Escalate to retention team</b> if branch-level intervention is insufficient.</li>
              </ol>
              <div class="disclaimer">&#9888; Rate reduction must follow company credit policy. It is not automatic.</div>
            </div>""", unsafe_allow_html=True)

    # ── Own Funds ──
    elif cat == "Own Funds":
        outstanding = float(row["Outstanding (L)"])
        planned = round(outstanding * 0.8, 1)
        paid = round(outstanding * 0.2, 1)
        if row["Customer Name"] == "Meena R":
            outstanding, planned, paid = 25.0, 20.0, 5.0
        avoided = round(planned - paid, 1)

        t1, t2 = st.tabs(["&#128176; Prepayment Simulation", "&#9989; Action Checklist"])
        with t1:
            st.markdown("""
            <div class="info-banner">
              Customer intends to prepay using own funds. The goal is to <b>understand the reason</b>,
              explore partial prepayment, and discuss liquidity — while <b>respecting the customer's final decision</b>.
            </div>""", unsafe_allow_html=True)

            s1,s2,s3 = st.columns(3)
            with s1: st.markdown(kpi("Outstanding",          fmt_l(outstanding), "Current balance","navy"),      unsafe_allow_html=True)
            with s2: st.markdown(kpi("Planned Prepayment",   fmt_l(planned),     "Customer's original plan","red"),unsafe_allow_html=True)
            with s3: st.markdown(kpi("After RM Discussion",  fmt_l(paid),        "Actual prepayment","teal"),    unsafe_allow_html=True)

            st.markdown(f"""
            <div class="sim-box">
              <div style='font-size:0.9rem;font-weight:700;color:#14532d !important;margin-bottom:10px;'>
                &#128202; What Happened
              </div>
              <p style='font-size:0.95rem;line-height:1.8;'>
                Customer originally planned to prepay <b>{fmt_l(planned)}</b>.<br>
                After RM discussion on <b>liquidity needs</b> and <b>partial prepayment benefits</b>,
                customer chose to prepay only <b>{fmt_l(paid)}</b>.
              </p>
              <div class="sim-result">
                &#9989; Portfolio retained through intervention: <b>{fmt_l(avoided)}</b>
              </div>
              <div class="disclaimer">
                Investment options (FD / MF referral) are for workflow demonstration only.
                Actual recommendations must follow company policy, suitability requirements and applicable regulations.
              </div>
            </div>""", unsafe_allow_html=True)

        with t2:
            st.markdown("""
            <div class="action-card">
              <b>Discussion Points — Own Funds Case:</b>
              <ol style='line-height:2.3;margin-top:10px;color:#134e4a !important;'>
                <li>&#128172; <b>Understand why</b> the customer wants to close — inheritance, windfall, or debt-aversion?</li>
                <li>&#128269; <b>Is full closure necessary?</b> Partial prepayment may achieve the same goal.</li>
                <li>&#128176; <b>Explore partial prepayment</b> — reduces EMI without locking all surplus.</li>
                <li>&#128016; <b>Explain liquidity risk</b> — funds once locked in closure are not recoverable.</li>
                <li>&#128203; <b>Where permitted</b>, mention FD / Mutual Fund as an alternative for surplus.</li>
                <li>&#9989; <b>Respect the customer's final decision</b> — no pressure.</li>
              </ol>
            </div>""", unsafe_allow_html=True)

    # ── Service Issue ──
    elif cat == "Service Issue":
        st.markdown("""
        <div class="action-warn">
          <b>Issue Identified:</b>
          <p style='font-size:1.0rem;margin-top:6px;'>
            &#128295; Documentation delay / service complaint / unresolved issue on record.
          </p>
        </div>
        <div class="action-card">
          <b>Steps — Service Issue Case:</b>
          <ol style='line-height:2.3;margin-top:10px;color:#134e4a !important;'>
            <li>&#128228; <b>Escalate the complaint</b> through the defined process immediately.</li>
            <li>&#8987; <b>Resolve within TAT</b> — do not allow complaint to remain open.</li>
            <li>&#128222; <b>Branch callback</b> to acknowledge action taken.</li>
            <li>&#129309; <b>RM follow-up</b> after resolution to confirm satisfaction.</li>
          </ol>
          <div class="insight-box">
            <b>&#128161; Key Insight:</b>
            <p style='margin:4px 0 0;'>
              Retention does not always require pricing intervention.
              <b>Service resolution alone</b> may retain the customer.
            </p>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Top-Up ──
    elif cat == "Top-Up Requirement":
        st.markdown("""
        <div class="action-card">
          <b>Top-Up Opportunity:</b>
          <p style='margin-top:8px;'>Customer has a fund requirement. If not addressed, they may approach a competitor.</p>
          <p style='color:#0d9488 !important;font-size:1.0rem;font-weight:700;'>
            &#128200; Assess customer for eligible top-up <u>before</u> they approach another lender.
          </p>
          <div class="disclaimer">Subject to credit policy and eligibility.</div>
        </div>""", unsafe_allow_html=True)

    # ── Rate Reduction ──
    elif cat == "Rate Reduction Request":
        st.markdown("""
        <div class="action-card">
          <b>Rate Reduction Request:</b>
          <ol style='line-height:2.3;margin-top:10px;color:#134e4a !important;'>
            <li>&#128203; Review current ROI vs applicable rate band for customer profile.</li>
            <li>&#128172; Understand the basis — market reference or financial stress.</li>
            <li>&#128228; Submit for rate review per credit policy if eligible.</li>
            <li>&#128200; Explore top-up or service improvements as complementary actions.</li>
          </ol>
          <div class="disclaimer">Rate reduction requires credit policy approval and is not automatic.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="action-card">
          <ol style='line-height:2.3;color:#134e4a !important;'>
            <li>&#128222; Contact customer to understand intent.</li>
            <li>&#128269; Assess any service or pricing concern.</li>
            <li>&#128203; Log contact and outcome below.</li>
          </ol>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)
    st.markdown("""<div class='section-head'>&#128203; Record RM Action</div>""", unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    act_opts = ["Rate Review","Top-Up Discussion","Service Resolution","Own Fund Discussion",
                "FD / MF Referral","Competitor Quote Review","Follow-up Required"]
    out_opts = ["Retained","Partially Retained","Closed","Follow-up"]

    with a1:
        def_act = saved.get("Action Taken", act_opts[0])
        if def_act not in act_opts: def_act = act_opts[0]
        action_taken = st.selectbox("Action Taken", act_opts, index=act_opts.index(def_act))

        def_out = saved.get("Outcome", out_opts[0])
        if def_out not in out_opts: def_out = out_opts[0]
        cust_outcome = st.selectbox("Customer Outcome", out_opts, index=out_opts.index(def_out))

    with a2:
        def_cmt = saved.get("RM Comments", str(row.get("RM Comments","")))
        rm_cmt  = st.text_area("RM Comments", value=def_cmt, height=120,
                                placeholder="Notes on customer interaction…")

    if st.button("&#128190;  Save Action"):
        st.session_state.customer_actions[sel] = {
            "Action Taken": action_taken, "Outcome": cust_outcome, "RM Comments": rm_cmt,
            "RM Contact Status": "Contacted"
        }
        # Update master df as well
        st.session_state.customer_df.loc[st.session_state.customer_df["Customer Name"] == sel, "Action Taken"] = action_taken
        st.session_state.customer_df.loc[st.session_state.customer_df["Customer Name"] == sel, "Outcome"] = cust_outcome
        st.session_state.customer_df.loc[st.session_state.customer_df["Customer Name"] == sel, "RM Comments"] = rm_cmt
        st.session_state.customer_df.loc[st.session_state.customer_df["Customer Name"] == sel, "RM Contact Status"] = "Contacted"
        st.success(f"&#9989; Action recorded for **{sel}** — Outcome: **{cust_outcome}**")


# ══════════════════════════════════════════════════════════════
#  SCREEN 4 — RM 90-DAY HEALTH CHECKS & ENGAGEMENT
# ══════════════════════════════════════════════════════════════
elif page == "📞  RM 90-Day Health Checks":

    st.markdown("""<div style='font-size:1.6rem;font-weight:800;color:#0f172a !important;margin-bottom:4px;'>
      &#128222; Proactive RM Engagement &amp; 90-Day Health Checks</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-banner">
      <b>Periodic Touchpoints Matter:</b> Proactively contacting borrowers every 90 days surfaces grievances,
      identifies competitor quotes early, and prevents foreclosure enquiries before they happen.
    </div>""", unsafe_allow_html=True)

    df = df_master.copy()
    rm_df = load_rm_interactions()

    # Calculate metrics
    tot_borrowers = len(df)
    overdue_count = len(df[df["Check-in Status"].astype(str).str.lower().str.contains("overdue")])
    due_today     = len(df[df["Check-in Status"].astype(str).str.lower().str.contains("today")])
    due_soon      = len(df[df["Check-in Status"].astype(str).str.lower().str.contains("soon|upcoming")])
    up_to_date    = len(df[df["Check-in Status"].astype(str).str.lower().str.contains("date")])

    m1,m2,m3,m4,m5 = st.columns(5)
    with m1: st.markdown(kpi("Total Portfolio", str(tot_borrowers), "Borrowers assigned"), unsafe_allow_html=True)
    with m2: st.markdown(kpi("Overdue (>90d)", str(overdue_count), "Requires immediate call", "red"), unsafe_allow_html=True)
    with m3: st.markdown(kpi("Due Today", str(due_today), "Scheduled for today", "amber"), unsafe_allow_html=True)
    with m4: st.markdown(kpi("Due Soon", str(due_soon), "Upcoming in next 30d", "navy"), unsafe_allow_html=True)
    with m5: st.markdown(kpi("Up to Date", str(up_to_date), "Check completed", "teal"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_sched, tab_log, tab_history = st.tabs([
        "📋  90-Day Calling Schedule & Queue",
        "📞  Log RM Call & Record Remarks",
        "📜  RM Interaction History & Audit Trail"
    ])

    # ── TAB 1: 90-DAY CALLING SCHEDULE ──
    with tab_sched:
        sf1, sf2, sf3 = st.columns([1.5, 1.5, 1])
        with sf1:
            sched_status = st.selectbox("Filter by Check-in Urgency", ["All", "Overdue", "Due Today", "Due Soon", "Up to date"])
        with sf2:
            sched_branch = st.selectbox("Filter by Branch", ["All"] + sorted(df["Branch"].unique()), key="sched_br_sel")
        with sf3:
            sched_filtered = df.copy()
            if sched_status != "All":
                sched_filtered = sched_filtered[sched_filtered["Check-in Status"].str.lower().str.contains(sched_status.lower())]
            if sched_branch != "All":
                sched_filtered = sched_filtered[sched_filtered["Branch"] == sched_branch]

            st.download_button(
                label="📥 Download Schedule (CSV)",
                data=sched_filtered.to_csv(index=False),
                file_name="rm_90day_calling_schedule.csv",
                mime="text/csv",
                use_container_width=True
            )

        if sched_filtered.empty:
            st.info("No customers matching this criteria.")
        else:
            st.markdown(html_schedule_table(sched_filtered), unsafe_allow_html=True)

    # ── TAB 2: LOG RM CALL & FEEDBACK ──
    with tab_log:
        st.markdown("<div class='section-head'>&#128222; Log Customer Health Check &amp; Record RM Notes</div>", unsafe_allow_html=True)

        call_c1, call_c2 = st.columns([1.5, 2])
        with call_c1:
            cust_list = [str(n).strip() for n in df["Customer Name"].dropna().unique() if str(n).strip()]
            if not cust_list:
                st.info("No customers available in active dataset.")
                st.stop()
            log_cust_name = st.selectbox("Select Customer to Call", cust_list, key="log_call_cust_sel")
            matching_cust = df[df["Customer Name"] == log_cust_name]
            if matching_cust.empty:
                st.warning("Customer record not found.")
                st.stop()
            cust_row = matching_cust.iloc[0]

            st.markdown(f"""
            <div style='background:#f8fafc;border:1.5px solid #cbd5e1;border-radius:12px;padding:16px;margin:10px 0;'>
              <div style='font-size:0.75rem;font-weight:700;color:#64748b;'>CUSTOMER SUMMARY</div>
              <div style='font-size:1.1rem;font-weight:800;color:#0f172a;margin-top:2px;'>{cust_row["Customer Name"]}</div>
              <div style='font-size:0.8rem;color:#1e3a8a;font-weight:600;'>{cust_row.get("Loan Account No","LN-001")} &bull; {cust_row["Branch"]}</div>
              <hr style='border:none;border-top:1px solid #e2e8f0;margin:10px 0;'>
              <div style='font-size:0.84rem;line-height:1.8;color:#334155;'>
                📞 <b>Phone:</b> {cust_row.get("Phone Number","+91 98401 23456")}<br>
                ✉️ <b>Email:</b> {cust_row.get("Email ID","cust@example.com")}<br>
                💰 <b>Outstanding:</b> &#8377;{cust_row["Outstanding (L)"]:.1f} Lakh &bull; <b>ROI:</b> {cust_row["ROI"]:.2f}%<br>
                ⏱️ <b>Last Contact:</b> {cust_row.get("Last Contact Date","2026-08-01")} ({cust_row.get("Check-in Status","Due")})
              </div>
            </div>
            """, unsafe_allow_html=True)

        with call_c2:
            form_c1, form_c2 = st.columns(2)
            with form_c1:
                call_date = st.date_input("Contact Date", datetime.date.today())
                call_channel = st.selectbox("Contact Channel", ["Phone Call", "In-Person Branch Visit", "Field / Residence Visit", "Video Call", "Email / WhatsApp"])
            with form_c2:
                call_rm = st.text_input("RM Name", value=current_user.get("FullName", "R. Anandhan"))
                call_connected = st.selectbox("Call Status", ["Connected & Spoke with Borrower", "Customer Callback Requested", "Call Not Answered / Busy", "Phone Switched Off / Invalid"])

            # Customer Trouble & Grievance
            trouble_options = [
                "No Troubles — Customer Fully Satisfied & Happy",
                "Competitor Offered Lower Interest Rate (BT enquiry)",
                "Planning Prepayment with Own Funds / Bonus",
                "Delays in Receiving Statement / Interest Certificate / NOC",
                "Grievance with Branch Customer Service / Communication",
                "Borrower Needs Additional Top-Up / Business Capital",
                "Facing Financial Distress / Requested Tenure Extension",
                "Other Grievance / Unspecified"
            ]
            identified_trouble = st.selectbox("Customer Feedback / Trouble Identified", trouble_options)

            # Outcome & Actions
            outcome_options = [
                "Retained — Reassured & Continuing Smoothly",
                "ROI Review Proposed to Retain Account",
                "Top-Up Eligibility Evaluation Initiated",
                "Service Grievance Escalated to Branch Ops & Resolved",
                "Partial Prepayment Counseled (Liquidity Retained)",
                "Follow-up Required (Borrower evaluating options)",
                "Account at Immediate Risk — Escalated to Head Office"
            ]
            call_outcome = st.selectbox("Interaction Outcome", outcome_options)

            next_date = st.date_input("Next 90-Day Follow-up Scheduled Date", datetime.date.today() + datetime.timedelta(days=90))

            rm_notes = st.text_area(
                "RM Remarks, Observations & Commitments Given to Customer",
                placeholder="Enter conversation highlights, customer sentiment, competitor name if mentioned, specific grievances, and action promised…",
                height=110
            )

            if st.button("💾  Save RM Health Check Record", use_container_width=True):
                if not rm_notes.strip():
                    st.warning("Please type RM Remarks before saving.")
                else:
                    new_log = {
                        "Interaction ID": f"LOG-{len(rm_df)+101}",
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Customer Name": log_cust_name,
                        "Loan Account No": cust_row.get("Loan Account No", "LN-001"),
                        "Branch": cust_row["Branch"],
                        "RM Name": call_rm,
                        "Call Type": f"90-Day Health Check ({call_channel})",
                        "Customer Trouble / Feedback": identified_trouble,
                        "Call Outcome": call_outcome,
                        "Next Check-in Date": next_date.strftime("%Y-%m-%d"),
                        "RM Remarks": rm_notes.strip()
                    }
                    save_rm_interaction(new_log)

                    # Update customer record in session state
                    st.session_state.customer_df.loc[
                        st.session_state.customer_df["Customer Name"] == log_cust_name,
                        "Last Contact Date"
                    ] = call_date.strftime("%Y-%m-%d")

                    st.session_state.customer_df.loc[
                        st.session_state.customer_df["Customer Name"] == log_cust_name,
                        "Next Check-in Due"
                    ] = next_date.strftime("%Y-%m-%d")

                    st.session_state.customer_df.loc[
                        st.session_state.customer_df["Customer Name"] == log_cust_name,
                        "Check-in Status"
                    ] = "Up to date"

                    st.session_state.customer_df.loc[
                        st.session_state.customer_df["Customer Name"] == log_cust_name,
                        "RM Contact Status"
                    ] = "Contacted"

                    st.markdown(f"""
                    <div class="success-banner">
                      &#9989; <b>Health Check recorded successfully for {log_cust_name}!</b><br>
                      Outcome: <b>{call_outcome}</b> &nbsp;|&nbsp; Next scheduled check-in: <b>{next_date}</b>.
                    </div>
                    """, unsafe_allow_html=True)

    # ── TAB 3: RM INTERACTION HISTORY & AUDIT TRAIL ──
    with tab_history:
        st.markdown("<div class='section-head'>&#128220; Logged RM Interactions &amp; Feedback Audit Trail</div>", unsafe_allow_html=True)
        rm_hist = load_rm_interactions()

        if rm_hist.empty:
            st.info("No interaction history logged yet. Use the 'Log RM Call' tab to record customer check-ins.")
        else:
            hist_c1, hist_c2 = st.columns([3, 1])
            with hist_c1:
                st.markdown(f"<p style='color:#64748b;font-weight:600;font-size:0.88rem;'>Total Recorded Health Checks: <b>{len(rm_hist)}</b></p>", unsafe_allow_html=True)
            with hist_c2:
                st.download_button(
                    label="📥 Download Full RM Logs (CSV)",
                    data=rm_hist.to_csv(index=False),
                    file_name="rm_customer_interactions_log.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            # Styled Table for RM logs
            rows_html = ""
            for _, ir in rm_hist.iterrows():
                rows_html += f"""<tr>
                    <td><b>{ir.get('Interaction ID','')}</b><br><span style='font-size:0.75rem;color:#64748b;'>{ir.get('Timestamp','')}</span></td>
                    <td><b>{ir.get('Customer Name','')}</b><br><span style='font-size:0.75rem;color:#64748b;font-family:monospace;'>{ir.get('Loan Account No','')}</span></td>
                    <td>{ir.get('Branch','')}</td>
                    <td><b>{ir.get('RM Name','')}</b></td>
                    <td style='max-width:200px;font-size:0.8rem;color:#0f172a;'>{ir.get('Customer Trouble / Feedback','None')}</td>
                    <td><span class='bdg bdg-contacted'>{ir.get('Call Outcome','')}</span></td>
                    <td style='font-weight:700;color:#0d9488;'>{ir.get('Next Check-in Date','')}</td>
                    <td style='max-width:280px;font-size:0.82rem;color:#334155;line-height:1.4;'>{ir.get('RM Remarks','')}</td>
                </tr>"""

            st.markdown(f"""
            <div class="tbl-wrap">
              <table class="styled-table">
                <thead><tr>
                  <th>ID &amp; Time</th><th>Borrower</th><th>Branch</th>
                  <th>RM Name</th><th>Trouble / Feedback</th><th>Call Outcome</th>
                  <th>Next Date</th><th>RM Remarks</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
              </table>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SCREEN 5 — MANAGEMENT SUMMARY
# ══════════════════════════════════════════════════════════════
elif page == "📊  Management Summary":

    st.markdown("""<div style='font-size:1.6rem;font-weight:800;color:#0f172a !important;margin-bottom:4px;'>
      &#128202; Management Summary — Prepayment Control</div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="info-banner">
      <b>Branch-wise Periodical Review</b> &nbsp;|&nbsp; Portfolio Protectors &nbsp;|&nbsp; YTD Sep 2026
    </div>""", unsafe_allow_html=True)

    df = df_master.copy()
    for name, upd in st.session_state.customer_actions.items():
        for col, val in upd.items():
            df.loc[df["Customer Name"] == name, col] = val

    total   = len(df)
    highr   = len(df[df["Risk Level"].str.strip().str.lower() == "high"])
    contd   = len(df[df["RM Contact Status"].str.strip().str.lower() == "contacted"])
    retd    = len(df[df["Outcome"].str.strip().str.lower() == "retained"])
    partd   = len(df[df["Outcome"].str.strip().str.lower() == "partially retained"])
    closd   = len(df[df["Outcome"].str.strip().str.lower() == "closed"])
    fupd    = len(df[df["Outcome"].str.strip().str.lower() == "follow-up"])
    port_l  = df[df["Outcome"].str.strip().str.lower().isin(["retained","partially retained"])]["Portfolio Retained (L)"].sum()
    port_s  = f"Rs.{port_l:.1f} L" if port_l < 100 else f"Rs.{port_l/100:.2f} Cr"

    k1,k2,k3,k4 = st.columns(4)
    with k1: st.markdown(kpi("Total Monitored", str(total),  "customers flagged"),         unsafe_allow_html=True)
    with k2: st.markdown(kpi("High Risk",       str(highr),  "immediate action","red"),    unsafe_allow_html=True)
    with k3: st.markdown(kpi("RM Contacted",    str(contd),  "outreach done","navy"),      unsafe_allow_html=True)
    with k4: st.markdown(kpi("Retained",        str(retd),   "customers saved","teal"),    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    k5,k6,k7,k8 = st.columns(4)
    with k5: st.markdown(kpi("Partially Retained", str(partd), "partial save","amber"),    unsafe_allow_html=True)
    with k6: st.markdown(kpi("Closed / Lost",       str(closd), "prepayment done","red"),  unsafe_allow_html=True)
    with k7: st.markdown(kpi("Follow-up Pending",   str(fupd),  "action needed","purple"), unsafe_allow_html=True)
    with k8: st.markdown(kpi("Portfolio Retained",  port_s,     "through intervention","teal"), unsafe_allow_html=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)

    PLOT_CFG = dict(paper_bgcolor="#ffffff", plot_bgcolor="#f8fafc",
                    font=dict(family="Inter", color="#1e293b"),
                    margin=dict(t=48,b=36,l=16,r=16))

    cc1, cc2 = st.columns(2)
    with cc1:
        rc = df["Risk Level"].str.strip().value_counts().reset_index()
        rc.columns = ["Risk Level","Count"]
        fig1 = px.pie(rc, names="Risk Level", values="Count",
                      title="Risk Level Distribution",
                      color="Risk Level",
                      color_discrete_map={"High":"#ef4444","Medium":"#f59e0b","Low":"#22c55e"},
                      hole=0.48)
        fig1.update_traces(textposition="inside", textinfo="percent+label",
                           textfont=dict(size=12,family="Inter",color="#ffffff"))
        fig1.update_layout(**PLOT_CFG, title_font=dict(size=15,color="#0f172a"),
                           legend=dict(orientation="h",y=-0.08))
        st.plotly_chart(fig1, use_container_width=True)

    with cc2:
        df["Cat"] = df["Trigger"].apply(identify_cat)
        reas = df["Cat"].value_counts().reset_index()
        reas.columns = ["Reason","Count"]
        fig2 = px.bar(reas, x="Count", y="Reason", orientation="h",
                      title="Reason for Possible Prepayment",
                      color="Count", color_continuous_scale=["#bfdbfe","#1d4ed8"])
        fig2.update_layout(**PLOT_CFG, title_font=dict(size=15,color="#0f172a"),
                           showlegend=False, coloraxis_showscale=False,
                           yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)

    cc3, cc4 = st.columns(2)
    with cc3:
        oc = df["Outcome"].str.strip().value_counts().reset_index()
        oc.columns = ["Outcome","Count"]
        fig3 = px.bar(oc, x="Outcome", y="Count", title="Outcome Distribution",
                      color="Outcome",
                      color_discrete_map={"Retained":"#0d9488","Partially Retained":"#f59e0b",
                                          "Closed":"#ef4444","Follow-up":"#8b5cf6"})
        fig3.update_layout(**PLOT_CFG, title_font=dict(size=15,color="#0f172a"), showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with cc4:
        hdf = df[df["Risk Level"].str.strip().str.lower() == "high"]
        bh  = hdf.groupby("Branch").size().reset_index(name="High Risk")
        fig4 = px.bar(bh, x="Branch", y="High Risk", title="Branch-wise High Risk Cases",
                      color="High Risk", color_continuous_scale=["#fecaca","#ef4444"])
        fig4.update_layout(**PLOT_CFG, title_font=dict(size=15,color="#0f172a"),
                           showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""<div class='section-head'>&#128200; Branch-wise Portfolio Retained</div>""",
                unsafe_allow_html=True)
    rdf = df[df["Outcome"].str.strip().str.lower().isin(["retained","partially retained"])]
    br  = rdf.groupby(["Branch","Outcome"])["Portfolio Retained (L)"].sum().reset_index()
    br.columns = ["Branch","Outcome","Portfolio Retained (L)"]
    if not br.empty:
        fig5 = px.bar(br, x="Branch", y="Portfolio Retained (L)", color="Outcome",
                      barmode="stack", title="Branch-wise Portfolio Retained (Rs. Lakh)",
                      color_discrete_map={"Retained":"#0d9488","Partially Retained":"#f59e0b"})
        fig5.update_layout(**PLOT_CFG, title_font=dict(size=15,color="#0f172a"),
                           legend=dict(orientation="h",y=-0.12))
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)

    # Management Branch Review Table with Export Button
    mgmt_c1, mgmt_c2 = st.columns([3, 1])
    with mgmt_c1:
        st.markdown("""<div class='section-head'>&#128203; Branch-wise Periodical Review</div>""", unsafe_allow_html=True)

    rows_rev = []
    for branch in sorted(df["Branch"].unique()):
        bdf  = df[df["Branch"] == branch]
        hc   = len(bdf[bdf["Risk Level"].str.strip().str.lower() == "high"])
        cc   = len(bdf[bdf["RM Contact Status"].str.strip().str.lower() == "contacted"])
        rc   = len(bdf[bdf["Outcome"].str.strip().str.lower() == "retained"])
        pc   = len(bdf[bdf["Outcome"].str.strip().str.lower() == "partially retained"])
        fc   = len(bdf[bdf["Outcome"].str.strip().str.lower() == "follow-up"])
        ptot = bdf[bdf["Outcome"].str.strip().str.lower().isin(["retained","partially retained"])]["Portfolio Retained (L)"].sum()
        rows_rev.append({"Branch":branch,"High Risk Cases":hc,"Contacted":cc,
                         "Retained":rc,"Part. Retained":pc,"Follow-up":fc,
                         "Portfolio Retained": f"Rs.{ptot:.1f} L" if ptot>0 else "-"})

    rev_df = pd.DataFrame(rows_rev)
    with mgmt_c2:
        st.download_button(
            label="📥 Download Review Summary (CSV)",
            data=rev_df.to_csv(index=False),
            file_name="branch_retention_periodical_review.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown(html_mgmt_table(rev_df), unsafe_allow_html=True)

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="close-banner">
      <p style='font-size:0.95rem;margin-bottom:12px;line-height:1.8;'>
        "Prepayment should not first be managed at the point of closure.<br>
        It should be managed at the <b>first sign of intent.</b>"
      </p>
      <div class="tamil">&#2997;&#2992;&#3009;&#2990;&#3021;&#2990;&#3009;&#2985;&#3021; &#2965;&#3006;&#2986;&#3021;&#2986;&#3019;&#2990;&#3021;</div>
      <div class="sub" style='margin-top:6px;'>Prevention is better than cure.</div>
    </div>
    """, unsafe_allow_html=True)
