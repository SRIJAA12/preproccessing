# -*- coding: utf-8 -*-
"""
Prepayment Control & Portfolio Retention
Idea Olympics -- Team: Portfolio Protectors
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

/* Sidebar text (careful not to override icon spans) */
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
.stSelectbox > div > div {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
.stTextArea > div > div { background: #ffffff !important; border-radius: 10px !important; }
textarea { background: #ffffff !important; color: #0f172a !important; }
.stButton > button {
    background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 28px !important;
    font-size: 0.9rem !important;
    box-shadow: 0 3px 12px rgba(37,99,235,0.25) !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(37,99,235,0.35) !important;
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

/* Text area */
textarea {
    background: #ffffff !important;
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "customers.csv")

@st.cache_data
def load_customers():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    df["Outstanding (L)"]    = pd.to_numeric(df["Outstanding (L)"],    errors="coerce")
    df["ROI"]                 = pd.to_numeric(df["ROI"],                 errors="coerce")
    df["Portfolio Retained (L)"] = pd.to_numeric(df["Portfolio Retained (L)"], errors="coerce").fillna(0)
    return df

df_master = load_customers()

if "customer_actions" not in st.session_state:
    st.session_state.customer_actions = {}

# ─────────────────────────────────────────────────────────────
#  HELPERS
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
    r = risk.strip().lower()
    k = {"high":"high","medium":"medium","low":"low"}.get(r,"low")
    return bdg(risk.strip(), k)

def contact_bdg(status):
    s = str(status).strip().lower()
    return bdg("&#10003; Contacted","contacted") if s=="contacted" else bdg("Not Contacted","notcontact")

def identify_cat(trigger):
    t = trigger.lower()
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
        chips = "".join(chip(t.strip()) for t in str(r["Trigger"]).split("|"))
        out  = f"<b style='color:#1e3a8a !important;'>&#8377;{r['Outstanding (L)']:.1f} L</b>"
        roi  = f"<span style='font-weight:700;color:#0f172a !important;'>{r['ROI']:.2f}%</span>"
        prod = f"<span style='background:#f1f5f9;border-radius:6px;padding:2px 9px;font-size:0.78rem;font-weight:600;color:#334155 !important;'>{r['Product']}</span>"
        rows += f"""<tr class="{rcls}">
            <td><b style='color:#0f172a !important;'>{r['Customer Name']}</b></td>
            <td style='color:#475569 !important;'>{r['Branch']}</td>
            <td>{prod}</td>
            <td>{out}</td>
            <td>{roi}</td>
            <td style='max-width:260px;'>{chips}</td>
            <td>{risk_bdg(r['Risk Level'])}</td>
            <td>{contact_bdg(r['RM Contact Status'])}</td>
        </tr>"""
    return f"""<div class="tbl-wrap">
    <table class="styled-table">
      <thead><tr>
        <th>Customer Name</th><th>Branch</th><th>Product</th>
        <th>Outstanding</th><th>ROI</th><th>Signals</th>
        <th>Risk</th><th>RM Status</th>
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
#  SIDEBAR — pure light theme, fully readable
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 4px 16px;'>
      <div style='font-size:1.15rem;font-weight:800;color:#0f172a !important;letter-spacing:-0.3px;'>
        🏦 Portfolio Protectors
      </div>
      <div style='font-size:0.78rem;color:#64748b !important;margin-top:3px;'>
        Idea Olympics 2026
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='border-top:2px solid #e2e8f0;margin-bottom:14px;'></div>",
                unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Home — Snapshot",
         "⚠️  Early Warning List",
         "🤝  Customer Retention",
         "📊  Management Summary"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='border-top:2px solid #e2e8f0;margin-top:16px;margin-bottom:16px;'></div>",
                unsafe_allow_html=True)

    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#0d9488);
                border-radius:12px;padding:16px;text-align:center;'>
      <div style='font-size:1.1rem;font-weight:800;color:#ffffff !important;
                  letter-spacing:1px;margin-bottom:4px;'>
        &#2997;&#2992;&#3009;&#2990;&#3021;&#2990;&#3009;&#2985;&#3021; &#2965;&#3006;&#2986;&#3021;&#2986;&#3019;&#2990;&#3021;
      </div>
      <div style='font-size:0.75rem;color:rgba(255,255,255,0.75) !important;font-style:italic;'>
        Prevention is better than cure
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:14px;font-size:0.75rem;color:#94a3b8 !important;line-height:1.7;text-align:center;'>
      Use the menu above<br>to navigate screens
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SCREEN 1 — HOME
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
    st.markdown("""<div class='section-head'>&#128204; YTD Prepayment Snapshot — Sep 2026</div>""",
                unsafe_allow_html=True)

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
      rate requests and service signals</b>. Engage before the customer reaches closure intent.
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

    if df.empty:
        st.info("No customers match the selected filters.")
    else:
        st.markdown(html_customer_table(df), unsafe_allow_html=True)

    # Legend
    st.markdown("""
    <div style='display:flex;gap:18px;margin-top:10px;font-size:0.82rem;color:#475569 !important;flex-wrap:wrap;'>
      <span>&#128996; <span class='bdg bdg-high'>High</span> Immediate RM contact</span>
      <span>&#128997; <span class='bdg bdg-medium'>Medium</span> Contact within 2 days</span>
      <span>&#128994; <span class='bdg bdg-low'>Low</span> Monitor</span>
    </div>
    <p style='color:#94a3b8 !important;font-size:0.8rem;margin-top:8px;font-style:italic;'>
      &#128073; Select a customer in <b>Customer Retention</b> screen to view recommended steps.
    </p>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SCREEN 3 — CUSTOMER RETENTION
# ══════════════════════════════════════════════════════════════
elif page == "🤝  Customer Retention":

    st.markdown("""<div style='font-size:1.6rem;font-weight:800;color:#0f172a !important;margin-bottom:4px;'>
      &#129309; Customer Retention Action</div>""", unsafe_allow_html=True)

    df = df_master.copy()
    demo  = ["Arun Kumar","Meena R","Suresh P"]
    other = [n for n in df["Customer Name"].tolist() if n not in demo]
    sel   = st.selectbox("&#128100; Select Customer", demo + other)

    row   = df[df["Customer Name"] == sel].iloc[0]
    saved = st.session_state.customer_actions.get(sel, {})

    st.markdown("<hr class='sdiv'>", unsafe_allow_html=True)
    st.markdown("""<div class='section-head'>&#128100; Customer Profile</div>""", unsafe_allow_html=True)

    p1,p2,p3,p4,p5 = st.columns(5)
    with p1: st.markdown(kpi("Customer", row["Customer Name"], row["Branch"]),          unsafe_allow_html=True)
    with p2: st.markdown(kpi("Product",  row["Product"], "Loan type"),                 unsafe_allow_html=True)
    with p3: st.markdown(kpi("Outstanding", fmt_l(row["Outstanding (L)"]), "Balance","navy"), unsafe_allow_html=True)
    with p4: st.markdown(kpi("Current ROI", f"{row['ROI']:.2f}%", "Interest rate"),    unsafe_allow_html=True)
    with p5:
        rk = str(row["Risk Level"]).strip().lower()
        rc = {"high":"red","medium":"amber","low":"green"}.get(rk,"")
        st.markdown(kpi("Risk Level", row["Risk Level"], "Prepayment risk", rc),       unsafe_allow_html=True)

    # Trigger chips
    triggers = [t.strip() for t in str(row["Trigger"]).split("|")]
    chips_html = "  ".join(chip(t) for t in triggers)
    st.markdown(f"""
    <div style='margin:14px 0 18px;'>
      <span style='font-weight:700;color:#0f172a !important;font-size:0.88rem;'>
        &#128268; Active Signals:
      </span>  {chips_html}
    </div>
    """, unsafe_allow_html=True)

    # Why attention
    st.markdown("""<div class='section-head'>&#128269; Why Does This Customer Need Attention?</div>""",
                unsafe_allow_html=True)
    reasons = "<ul style='color:#134e4a !important;line-height:2.2;font-size:0.92rem;margin:0;'>"
    for t in triggers:
        tl = t.lower()
        if   "bureau"     in tl: reasons += "<li><b>Bureau alert</b> detected — another lender has pulled the customer's credit profile.</li>"
        elif "foreclosure" in tl: reasons += "<li>Customer has <b>enquired about foreclosure / payoff amount</b> at the branch.</li>"
        elif "competitor"  in tl: reasons += "<li>A <b>competitor quote</b> is suspected — customer is comparing offers.</li>"
        elif "own fund"    in tl: reasons += "<li>Customer <b>intends to prepay using own funds</b> — savings windfall or asset liquidation.</li>"
        elif "service" in tl or "complaint" in tl:
            reasons += "<li>A <b>service complaint or unresolved issue</b> is on record — may drive closure.</li>"
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
              <b style='color:#dc2626 !important;'>Urgency:</b> Contact customer within <b>24 hours</b>.
            </div>""", unsafe_allow_html=True)
        with t2:
            st.markdown("""
            <div class="action-card">
              <b>Steps for Balance Transfer / Foreclosure Case:</b>
              <ol style='line-height:2.3;margin-top:10px;color:#134e4a !important;'>
                <li>&#128222; <b>Contact customer immediately</b> — do not wait for further signals.</li>
                <li>&#128172; <b>Understand the competitor offer</b> — rate, tenure, processing fee, terms.</li>
                <li>&#128203; <b>Review ROI eligibility</b> — check if revision is permissible under credit policy.</li>
                <li>&#128176; <b>Check top-up requirement</b> — customer may have a fund need we can address.</li>
                <li>&#128295; <b>Resolve any service concerns</b> — pricing is not always the only reason.</li>
                <li>&#128680; <b>Escalate to retention team</b> if branch-level intervention is insufficient.</li>
              </ol>
              <div class="disclaimer">&#9888; Rate reduction must follow company credit policy. It is not automatic.</div>
            </div>""", unsafe_allow_html=True)

    # ── Own Funds ──
    elif cat == "Own Funds":
        outstanding   = 25.0 if row["Customer Name"] == "Meena R" else row["Outstanding (L)"]
        planned, paid = 20.0, 5.0
        avoided = planned - paid

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
            "Action Taken": action_taken, "Outcome": cust_outcome, "RM Comments": rm_cmt
        }
        st.success(f"&#9989; Action recorded for **{sel}** — Outcome: **{cust_outcome}**")


# ══════════════════════════════════════════════════════════════
#  SCREEN 4 — MANAGEMENT SUMMARY
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
    st.markdown("""<div class='section-head'>&#128203; Branch-wise Periodical Review</div>""",
                unsafe_allow_html=True)

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

    st.markdown(html_mgmt_table(pd.DataFrame(rows_rev)), unsafe_allow_html=True)

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
