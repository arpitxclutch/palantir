"""
╔══════════════════════════════════════════════════════════════════════════════╗
║      PALANTIR TECHNOLOGIES (PLTR) — RESEARCH TERMINAL  (Damodaran Framework)║
║  Forecasting · Valuation · Marketing Strategy · Live Data · Live News       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  HOW TO RUN IN VS CODE:                                                     ║
║  1. Open a terminal  (Ctrl + `)                                             ║
║  2. pip install streamlit yfinance plotly pandas numpy requests feedparser  ║
║  3. streamlit run palantir_terminal.py                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import feedparser
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Palantir Research Terminal · KB",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BRAND COLOURS — Vivid Light Theme ─────────────────────────────────────────
NAVY        = "#1D3557"          # deep ink blue (text, anchors)
NAVY_LIGHT  = "#EAF0FB"         # soft sky wash
ORANGE      = "#E63946"         # Palantir signal red-orange
ORANGE_LIGHT= "#FFF0F1"
TEAL        = "#2A9D8F"         # emerald teal
TEAL_LIGHT  = "#E0F5F2"
GOLD        = "#F4A261"         # warm amber
GOLD_LIGHT  = "#FEF3E6"
RED         = "#C1121F"
RED_LIGHT   = "#FFECEE"
GREEN       = "#2D6A4F"
GREEN_LIGHT = "#E8F5EE"
PURPLE      = "#7B2D8B"
PURPLE_LIGHT= "#F5EAF9"
BG          = "#F7F9FF"         # cool white canvas
BORDER      = "#D0DAF0"
ACCENT1     = "#264653"         # dark teal accent
ACCENT2     = "#E9C46A"         # saffron

# ── THEME CSS — Vibrant Light Overhaul ────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

  body, [data-testid="stApp"] {{
    background: {BG};
    color: {NAVY};
    font-family: 'Inter', 'Segoe UI', sans-serif;
  }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {NAVY} 0%, #0f2340 100%) !important;
    border-right: 2px solid {ORANGE};
  }}
  [data-testid="stSidebar"] * {{ color: #CBD5E1 !important; font-family: 'Inter', sans-serif !important; }}
  [data-testid="stSidebar"] .stRadio > label {{
    color: #94A3B8 !important; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 1.2px;
  }}
  [data-testid="stSidebar"] .stRadio label {{ color: #E2E8F0 !important; font-size: 0.88rem; }}
  h1, h2, h3 {{ color: {NAVY} !important; font-family: 'Space Grotesk', 'Inter', sans-serif !important; }}

  /* ── Cards ── */
  .q-card {{
    background: #fff; border: 1px solid {BORDER};
    border-radius: 14px; padding: 1.1rem 1.3rem; margin-bottom: 0.9rem;
    box-shadow: 0 2px 12px rgba(29,53,87,0.07);
    transition: box-shadow 0.2s;
  }}
  .q-card:hover {{ box-shadow: 0 4px 20px rgba(29,53,87,0.12); }}
  .q-card-navy {{
    background: linear-gradient(135deg, {NAVY_LIGHT} 0%, #f0f4ff 100%);
    border-left: 4px solid {NAVY};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}
  .q-card-orange {{
    background: linear-gradient(135deg, {ORANGE_LIGHT} 0%, #fff8f9 100%);
    border-left: 4px solid {ORANGE};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}
  .q-card-teal {{
    background: linear-gradient(135deg, {TEAL_LIGHT} 0%, #f0faf9 100%);
    border-left: 4px solid {TEAL};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}
  .q-card-gold {{
    background: linear-gradient(135deg, {GOLD_LIGHT} 0%, #fffdf5 100%);
    border-left: 4px solid {GOLD};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}
  .q-card-red {{
    background: linear-gradient(135deg, {RED_LIGHT} 0%, #fff8f9 100%);
    border-left: 4px solid {RED};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}
  .q-card-green {{
    background: linear-gradient(135deg, {GREEN_LIGHT} 0%, #f2faf5 100%);
    border-left: 4px solid {GREEN};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}
  .q-card-purple {{
    background: linear-gradient(135deg, {PURPLE_LIGHT} 0%, #fdf5ff 100%);
    border-left: 4px solid {PURPLE};
    border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
  }}

  /* ── Section Heading ── */
  .sec-head {{
    font-size: 1rem; font-weight: 800; color: {NAVY} !important;
    font-family: 'Space Grotesk', sans-serif;
    border-left: 5px solid {ORANGE}; padding-left: 12px;
    margin: 1.6rem 0 0.9rem; letter-spacing: 0.1px;
    background: linear-gradient(90deg, rgba(230,57,70,0.04) 0%, transparent 60%);
    padding-top: 4px; padding-bottom: 4px; border-radius: 0 6px 6px 0;
  }}

  /* ── Narrative ── */
  .narrative {{
    background: linear-gradient(135deg, {NAVY_LIGHT} 0%, #f5f8ff 100%);
    border-left: 3px solid {NAVY};
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.2rem;
    font-style: italic; font-size: 0.9rem; line-height: 1.85;
    color: #2c4a6e; margin-bottom: 1.1rem;
    box-shadow: 0 1px 6px rgba(29,53,87,0.06);
  }}

  /* ── Pull-quote ── */
  .pullquote {{
    background: linear-gradient(135deg, {ORANGE_LIGHT} 0%, {NAVY_LIGHT} 100%);
    border-left: 5px solid {ORANGE}; border-right: 5px solid {NAVY};
    border-radius: 6px; padding: 1rem 1.6rem; margin: 1.2rem 1rem;
    font-style: italic; font-size: 0.97rem; font-weight: 600;
    color: {ORANGE}; text-align: center;
    box-shadow: 0 2px 10px rgba(230,57,70,0.1);
  }}

  /* ── KPI Card ── */
  .kpi-card {{
    background: #fff; border: 1px solid {BORDER};
    border-top: 4px solid {ORANGE}; border-radius: 12px;
    padding: 0.9rem 1rem; text-align: center; height: 100%;
    box-shadow: 0 3px 12px rgba(230,57,70,0.08);
    transition: transform 0.18s, box-shadow 0.18s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(230,57,70,0.14); }}
  .kpi-label {{ font-size: 0.67rem; color: #6B7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; font-weight: 700; }}
  .kpi-value {{ font-size: 1.45rem; font-weight: 900; color: {NAVY}; font-family: 'Space Grotesk', sans-serif; }}
  .kpi-sub   {{ font-size: 0.7rem; color: #6B7280; margin-top: 4px; }}
  .kpi-up    {{ color: {GREEN}; font-size: 0.78rem; font-weight: 600; }}
  .kpi-dn    {{ color: {RED};   font-size: 0.78rem; font-weight: 600; }}

  /* ── Tags ── */
  .tag-navy   {{ background:{NAVY_LIGHT};   color:{NAVY};   padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}
  .tag-orange {{ background:{ORANGE_LIGHT}; color:{ORANGE}; padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}
  .tag-teal   {{ background:{TEAL_LIGHT};   color:{TEAL};   padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}
  .tag-gold   {{ background:{GOLD_LIGHT};   color:#b05a00; padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}
  .tag-red    {{ background:{RED_LIGHT};    color:{RED};    padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}
  .tag-green  {{ background:{GREEN_LIGHT};  color:{GREEN};  padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}
  .tag-purple {{ background:{PURPLE_LIGHT}; color:{PURPLE}; padding:3px 12px; border-radius:99px; font-size:0.71rem; font-weight:800; }}

  /* ── News ── */
  .news-pos   {{ background:linear-gradient(90deg,#f0fbf4,#fafffe); border-left:4px solid {TEAL};  padding:0.7rem 1.1rem; border-radius:0 10px 10px 0; margin-bottom:0.6rem; }}
  .news-neg   {{ background:linear-gradient(90deg,{RED_LIGHT},#fffcfc); border-left:4px solid {RED};   padding:0.7rem 1.1rem; border-radius:0 10px 10px 0; margin-bottom:0.6rem; }}
  .news-neu   {{ background:linear-gradient(90deg,{NAVY_LIGHT},#fafbff); border-left:4px solid {NAVY};  padding:0.7rem 1.1rem; border-radius:0 10px 10px 0; margin-bottom:0.6rem; }}
  .news-title {{ font-size:0.88rem; font-weight:700; color:{NAVY}; line-height:1.5; }}
  .news-meta  {{ font-size:0.7rem;  color:#6B7280; margin-top:5px; }}

  /* ── Ansoff card ── */
  .ansoff-card {{
    background: linear-gradient(135deg, #fff 0%, {NAVY_LIGHT} 100%);
    border-radius: 12px; padding: 1rem 1.2rem;
    margin-bottom: 0.8rem; border: 1px solid {BORDER};
    box-shadow: 0 2px 8px rgba(29,53,87,0.06);
  }}
  .ansoff-title {{ font-size: 0.94rem; font-weight: 800; color: {NAVY}; font-family:'Space Grotesk',sans-serif; }}
  .ansoff-sub   {{ font-size: 0.73rem; color: #6B7280; margin-bottom: 8px; }}
  .ansoff-item  {{ font-size: 0.84rem; color: #374151; margin-bottom: 5px; line-height:1.5; }}

  /* ── Fingerprint ── */
  .fp-card {{
    background: linear-gradient(135deg, #fff 0%, {ORANGE_LIGHT} 100%);
    border-left: 4px solid {ORANGE};
    border-radius: 0 10px 10px 0; padding: 0.7rem 1rem; margin-bottom: 0.65rem;
    box-shadow: 0 2px 8px rgba(230,57,70,0.07);
    transition: transform 0.15s;
  }}
  .fp-card:hover {{ transform: translateX(2px); }}
  .fp-label  {{ font-size:0.67rem; color:#6B7280; text-transform:uppercase; letter-spacing:0.6px; font-weight:700; }}
  .fp-value  {{ font-size:1.08rem; font-weight:800; color:{NAVY}; font-family:'Space Grotesk',sans-serif; }}
  .fp-signal {{ font-size:0.72rem; color:#374151; margin-top:2px; }}

  /* ── Dataframe overrides ── */
  .stDataFrame td, .stDataFrame th {{ color:{NAVY} !important; font-size:0.82rem !important; font-family:'Inter',sans-serif !important; }}
  .stDataFrame th {{ background: linear-gradient(90deg, {NAVY} 0%, #264a7a 100%) !important; color:white !important; font-weight:700 !important; letter-spacing:0.3px; }}
  .stDataFrame tr:nth-child(even) td {{ background-color:#f5f8ff !important; }}
  .stDataFrame tr:hover td {{ background-color:{NAVY_LIGHT} !important; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab"] {{ color:#374151 !important; font-weight:600; font-family:'Inter',sans-serif; }}
  .stTabs [aria-selected="true"] {{ color:{ORANGE} !important; border-bottom-color:{ORANGE} !important; font-weight:800; }}

  /* ── Slider ── */
  .stSlider label {{ color:{NAVY} !important; font-weight:600; }}
  [data-testid="stSlider"] > div > div > div > div {{ background:{ORANGE} !important; }}

  /* ── Metrics ── */
  [data-testid="stMetric"] label {{ color:#6B7280 !important; font-size:0.78rem !important; font-weight:700 !important; }}
  [data-testid="stMetricValue"]  {{ color:{NAVY}  !important; font-weight:900 !important; font-family:'Space Grotesk',sans-serif !important; }}

  /* ── Palantir Logo Block ── */
  .pltr-logo-block {{
    display: flex; align-items: center; gap: 14px; margin-bottom: 0.8rem;
  }}
  .pltr-logo-svg {{ flex-shrink: 0; }}
  .pltr-logo-text {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: white; letter-spacing: 2px;
    text-transform: uppercase;
  }}
  .pltr-logo-sub {{
    font-size: 0.65rem; color: rgba(255,255,255,0.55);
    letter-spacing: 1.5px; text-transform: uppercase; margin-top: 2px;
  }}

  /* ── Author Badge ── */
  .author-badge {{
    background: linear-gradient(135deg, rgba(230,57,70,0.15) 0%, rgba(42,157,143,0.1) 100%);
    border: 1px solid rgba(230,57,70,0.3);
    border-radius: 8px; padding: 8px 12px; margin-top: 8px;
    font-size: 0.72rem; color: #CBD5E1;
    font-family: 'Inter', sans-serif;
  }}
  .author-name {{
    color: {GOLD}; font-weight: 800; font-size: 0.78rem;
    font-family: 'Space Grotesk', sans-serif;
  }}

  /* ── Mission Strip ── */
  .mission-strip {{
    background: linear-gradient(90deg, {NAVY} 0%, #1a3060 40%, {ORANGE} 100%);
    border-radius: 10px; padding: 0.7rem 1.2rem; margin-bottom: 1rem;
    font-size: 0.78rem; color: rgba(255,255,255,0.85);
    font-style: italic; text-align: center; letter-spacing: 0.3px;
  }}

  /* ── Stat Pill ── */
  .stat-pill {{
    display: inline-block;
    background: {NAVY}; color: white;
    padding: 2px 10px; border-radius: 99px;
    font-size: 0.7rem; font-weight: 700;
    margin: 2px 3px;
  }}

  /* ── Footer ── */
  .footer {{
    font-size:0.7rem; color:#9CA3AF; text-align:center;
    margin-top:3rem; border-top: 2px solid {BORDER}; padding-top:1.2rem;
    background: linear-gradient(90deg, {NAVY_LIGHT} 0%, #fff 50%, {ORANGE_LIGHT} 100%);
    border-radius: 8px; padding: 1rem;
  }}
  .footer-author {{ color: {ORANGE}; font-weight: 800; font-size: 0.76rem; }}

  /* ── Buttons ── */
  [data-testid="baseButton-secondary"] {{
    background: linear-gradient(135deg, {ORANGE} 0%, #c1121f 100%) !important;
    color:#fff !important;
    border:none !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-weight:700 !important;
    box-shadow: 0 2px 8px rgba(230,57,70,0.3) !important;
  }}
  [data-testid="baseButton-secondary"]:hover {{
    box-shadow: 0 4px 16px rgba(230,57,70,0.45) !important;
    transform: translateY(-1px) !important;
  }}
</style>
""", unsafe_allow_html=True)


# ── HISTORICAL DATA (FY2021–FY2024 + TTM 2025, from 10-K & Earnings Releases) ─
HIST = pd.DataFrame([
    {"Year":"FY21","Revenue":1542, "NI":-520,  "EPS":-0.24,"EBIT_M":-33.4,"DPS":0.0,"FCFF":119,  "EBIT":-515, "DA":108, "Capex":68,  "CFO":187},
    {"Year":"FY22","Revenue":1906, "NI":-374,  "EPS":-0.17,"EBIT_M":-15.2,"DPS":0.0,"FCFF":261,  "EBIT":-290, "DA":113, "Capex":54,  "CFO":315},
    {"Year":"FY23","Revenue":2229, "NI":210,   "EPS":0.09, "EBIT_M":6.8,  "DPS":0.0,"FCFF":730,  "EBIT":152,  "DA":120, "Capex":43,  "CFO":773},
    {"Year":"FY24","Revenue":2865, "NI":462,   "EPS":0.19, "EBIT_M":12.5, "DPS":0.0,"FCFF":1154, "EBIT":358,  "DA":133, "Capex":42,  "CFO":1196},
    {"Year":"FY25E","Revenue":3754,"NI":852,   "EPS":0.34, "EBIT_M":19.5, "DPS":0.0,"FCFF":1630, "EBIT":731,  "DA":145, "Capex":50,  "CFO":1675},
])

SEGMENTS = pd.DataFrame([
    {"Segment":"U.S. Commercial",  "Rev_FY25":902,  "EBIT_FY25":315, "Margin_FY25":35.0,"Rev_FY24":668,  "EBIT_FY24":220},
    {"Segment":"U.S. Government",  "Rev_FY25":1199, "EBIT_FY25":384, "Margin_FY25":32.0,"Rev_FY24":1048, "EBIT_FY24":325},
    {"Segment":"International Comm","Rev_FY25":639, "EBIT_FY25":128, "Margin_FY25":20.0,"Rev_FY24":526,  "EBIT_FY24":95},
    {"Segment":"International Gov", "Rev_FY25":1014,"EBIT_FY25":203, "Margin_FY25":20.0,"Rev_FY24":623,  "EBIT_FY24":105},
])

PEERS = pd.DataFrame([
    {"Company":"Palantir",  "PE":280, "EBIT_M":19.5,"Rev_CAGR":27,"ROE":15, "FwdPE":170},
    {"Company":"Snowflake", "PE":None,"EBIT_M":-5.0, "Rev_CAGR":30,"ROE":-8, "FwdPE":95},
    {"Company":"C3.ai",     "PE":None,"EBIT_M":-20.0,"Rev_CAGR":18,"ROE":-22,"FwdPE":None},
    {"Company":"Datadog",   "PE":210, "EBIT_M":18.0, "Rev_CAGR":26,"ROE":12, "FwdPE":80},
    {"Company":"UiPath",    "PE":70,  "EBIT_M":12.0, "Rev_CAGR":14,"ROE":8,  "FwdPE":55},
    {"Company":"Veeva",     "PE":60,  "EBIT_M":30.0, "Rev_CAGR":16,"ROE":22, "FwdPE":48},
])

BASE = {
    "fcff":1630,"net_cash":5210,"total_debt":0,"shares":2.15,
    "revenue":3754,"ebitda":876,"ebit":731,"ni":852,"ni_nongaap":1100,
    "eps_gaap":0.34,"eps_nongaap":0.44,"dps":0.0,"equity":5900,
    "roe":15.0,"roce":16.0,"da":145,"capex":50,
}


# ── LIVE DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def get_live_price():
    try:
        t    = yf.Ticker("PLTR")
        info = t.info
        price = float(info.get("currentPrice") or info.get("regularMarketPrice") or 85.00)
        prev  = float(info.get("previousClose") or 84.00)
        chg   = round(price - prev, 2)
        chgp  = round((chg / prev) * 100, 2) if prev else 0.0
        mktcap= info.get("marketCap", 0)
        return {
            "price":    round(price, 2),
            "change":   chg,
            "change_pct": chgp,
            "volume":   f"{info.get('volume',0)/1e6:.1f}M",
            "market_cap": f"${mktcap/1e9:.1f}B",
            "52w_high": info.get("fiftyTwoWeekHigh", 125),
            "52w_low":  info.get("fiftyTwoWeekLow",  21),
            "pe":       round(float(info.get("trailingPE") or 280.0), 1),
            "fwd_pe":   round(float(info.get("forwardPE")  or 170.0), 1),
            "pb":       round(float(info.get("priceToBook")or 30.0), 1),
            "div_yield":round(float(info.get("dividendYield") or 0)*100, 2),
            "beta":     round(float(info.get("beta") or 2.80), 2),
            "shares":   round(float(info.get("sharesOutstanding",2.15e9))/1e9, 3),
        }
    except Exception:
        return {"price":85.00,"change":1.20,"change_pct":1.43,
                "volume":"72.3M","market_cap":"$183.1B",
                "52w_high":125,"52w_low":21,"pe":280.0,"fwd_pe":170.0,
                "pb":30.5,"div_yield":0.0,"beta":2.80,"shares":2.15}


@st.cache_data(ttl=300)
def get_price_history(period="6mo"):
    try:
        return yf.Ticker("PLTR").history(period=period)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=600)
def get_live_news():
    items = []
    feeds = [
        "https://news.google.com/rss/search?q=Palantir+Technologies+PLTR+AI&hl=en-US&gl=US&ceid=US:en",
        "https://news.google.com/rss/search?q=Palantir+AIP+government+contract&hl=en-US&gl=US&ceid=US:en",
    ]
    pos_kw = ["profit","growth","gains","contract","launch","record","beat","upgrade","buy",
              "rise","rally","partnership","win","award","expands","government","ai","aip","defense"]
    neg_kw = ["fall","loss","decline","regulatory","ban","downgrade","miss","concern",
              "risk","drop","slump","lawsuit","fine","overvalued","tariff","dilution"]
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:8]:
                title = e.get("title","")
                link  = e.get("link","#")
                dp    = e.get("published_parsed")
                date  = datetime(*dp[:6]).strftime("%d %b %Y") if dp else "—"
                tl    = title.lower()
                sent  = "neutral"
                if any(k in tl for k in pos_kw): sent = "positive"
                if any(k in tl for k in neg_kw): sent = "negative"
                if title and title not in [x["title"] for x in items]:
                    items.append({"title":title,"link":link,"date":date,"sentiment":sent})
            if len(items) >= 14: break
        except Exception:
            continue
    if not items:
        items = [
            {"title":"Palantir Q4 FY2024: Revenue $828M +36% YoY; U.S. Commercial +52%","link":"#","date":"Feb 2025","sentiment":"positive"},
            {"title":"AIP (Artificial Intelligence Platform) now deployed at 100+ commercial clients","link":"#","date":"Jan 2025","sentiment":"positive"},
            {"title":"Palantir secures $480M U.S. Army AI software contract extension","link":"#","date":"Dec 2024","sentiment":"positive"},
            {"title":"Stock valuation concerns: P/E exceeds 250x amid high retail investor expectations","link":"#","date":"Feb 2025","sentiment":"negative"},
            {"title":"Palantir added to S&P 500 index; institutional inflows surge","link":"#","date":"Sep 2024","sentiment":"positive"},
            {"title":"FY2025 guidance raised: Revenue $3.74–$3.76B; Adj. income from ops $1.55B+","link":"#","date":"Feb 2025","sentiment":"positive"},
            {"title":"International government revenue growth slows as European defence spending shifts","link":"#","date":"Nov 2024","sentiment":"negative"},
            {"title":"Palantir CEO Alex Karp sells $1.2B in stock under pre-arranged trading plan","link":"#","date":"Jan 2025","sentiment":"negative"},
        ]
    return items[:14]


# ── DCF ENGINE ────────────────────────────────────────────────────────────────
def run_dcf(wacc, g_term, rev_cagr, ebit_margin, live_price):
    """5-year DCF for Palantir — debt-free, high-growth SaaS/AI platform."""
    base_rev  = BASE["revenue"]
    tax_rate  = 0.21
    debt      = BASE["total_debt"]   # $0 — Palantir is debt-free
    shares    = BASE["shares"]

    rows, pv_total = [], 0.0
    stc = 3.5          # Sales-to-Capital (lower than hardware; software scale)
    rev_prev = base_rev

    for i in range(1, 6):
        rev_i   = base_rev * (1 + rev_cagr/100) ** i
        ebit_i  = rev_i * ebit_margin / 100
        nopat_i = ebit_i * (1 - tax_rate)
        drv     = rev_i - rev_prev
        reinv_i = drv / stc
        fcff_i  = nopat_i - reinv_i
        rev_prev = rev_i
        df_     = (1 + wacc/100) ** i
        pv_i    = fcff_i / df_
        pv_total += pv_i
        ni_i    = ebit_i * (1 - tax_rate)
        eps_i   = ni_i / (shares * 1000)
        rows.append({
            "Year": f"FY{25+i}E",
            "Revenue ($M)": int(rev_i),
            "EBIT ($M)":    int(ebit_i),
            "EBIT Margin":  f"{ebit_margin:.1f}%",
            "NOPAT ($M)":   int(nopat_i),
            "FCFF ($M)":    int(fcff_i),
            "Disc. Factor": round(1/df_, 4),
            "PV FCFF ($M)": int(pv_i),
        })

    tv_fcff  = rows[-1]["FCFF ($M)"] * (1 + g_term/100)
    if wacc <= g_term:
        return None
    tv       = tv_fcff / ((wacc - g_term) / 100)
    pv_tv    = tv / (1 + wacc/100) ** 5
    ev       = pv_total + pv_tv
    eq_val   = ev + BASE["net_cash"]   # add back net cash (no debt)
    ivps     = eq_val / (shares * 1000)
    upside   = round(((ivps / live_price) - 1) * 100, 1)

    return {
        "rows": rows, "pv_explicit": int(pv_total), "pv_tv": int(pv_tv),
        "ev": int(ev), "eq_val": int(eq_val), "ivps": round(ivps, 2),
        "upside": upside, "tv_pct": round(pv_tv / ev * 100, 1),
    }


def sensitivity_table(rev_cagr, ebit_margin, live_price):
    wacc_vals = [9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0]
    g_vals    = [3.0, 3.5, 4.0, 4.5, 5.0]
    data = {}
    for w in wacc_vals:
        row = []
        for g in g_vals:
            r = run_dcf(w, g, rev_cagr, ebit_margin, live_price)
            row.append(r["ivps"] if r else "—")
        data[f"WACC {w}%"] = row
    return pd.DataFrame(data, index=[f"g = {g}%" for g in g_vals])


# ── CHART HELPERS ─────────────────────────────────────────────────────────────
_L = dict(
    plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
    font=dict(color=NAVY, family="Inter, Space Grotesk, Segoe UI"),
    margin=dict(l=20, r=20, t=36, b=20),
    legend=dict(orientation="h", y=1.1, font=dict(color="#374151", size=11)),
)

def rev_ni_chart():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=HIST["Year"], y=HIST["Revenue"], name="Revenue",
                         marker_color=NAVY, opacity=0.85), secondary_y=False)
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["EBIT"], name="EBIT",
                             line=dict(color=ORANGE, width=2.5),
                             mode="lines+markers", marker=dict(size=7, color=ORANGE)), secondary_y=True)
    fig.add_trace(go.Scatter(x=HIST["Year"], y=HIST["CFO"], name="CFO",
                             line=dict(color=TEAL, width=2, dash="dot"),
                             mode="lines+markers", marker=dict(size=6, color=TEAL)), secondary_y=True)
    fig.update_layout(height=320, **_L,
                      yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      yaxis2=dict(tickprefix="$", ticksuffix="M", gridcolor="#F0F0F0", tickfont=dict(color="#374151")))
    fig.update_xaxes(tickfont=dict(color="#374151"))
    return fig


def candlestick_chart(df):
    if df is None or df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No live data available — check internet connection",
                           xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                           font=dict(size=14, color="#6B7280"))
        fig.update_layout(height=380, **_L)
        return fig
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.04, row_heights=[0.75, 0.25])
    fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                  low=df["Low"], close=df["Close"], name="PLTR",
                                  increasing_line_color=GREEN, decreasing_line_color=RED), row=1, col=1)
    ma20 = df["Close"].rolling(20).mean()
    ma50 = df["Close"].rolling(50).mean()
    fig.add_trace(go.Scatter(x=df.index, y=ma20, name="20D MA",
                             line=dict(color=ORANGE, width=1.5, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=ma50, name="50D MA",
                             line=dict(color=TEAL, width=1.5, dash="dash")), row=1, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume",
                         marker_color=NAVY, opacity=0.45), row=2, col=1)
    fig.update_layout(height=420, **_L, xaxis_rangeslider_visible=False,
                      yaxis=dict(tickprefix="$", tickfont=dict(color="#374151"), gridcolor="#F0F0F0"),
                      yaxis2=dict(tickfont=dict(color="#374151"), gridcolor="#F0F0F0"))
    fig.update_xaxes(tickfont=dict(color="#374151"))
    return fig


def segment_margin_chart():
    colors = [NAVY, ORANGE, TEAL, GOLD]
    fig = go.Figure(go.Bar(
        x=SEGMENTS["Segment"], y=SEGMENTS["Margin_FY25"],
        marker_color=colors,
        text=[f"{m:.1f}%" for m in SEGMENTS["Margin_FY25"]],
        textposition="outside", textfont=dict(color="#1A1A2E", size=11)
    ))
    fig.update_layout(height=300, **_L,
                      title=dict(text="EBIT Margin by Segment — FY2025E",
                                 font=dict(color="#1A1A2E", size=13)),
                      yaxis=dict(ticksuffix="%", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")), showlegend=False)
    return fig


def segment_rev_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Revenue FY25E", x=SEGMENTS["Segment"],
                         y=SEGMENTS["Rev_FY25"], marker_color=NAVY, opacity=0.9))
    fig.add_trace(go.Bar(name="Revenue FY24",  x=SEGMENTS["Segment"],
                         y=SEGMENTS["Rev_FY24"], marker_color=NAVY, opacity=0.4))
    fig.add_trace(go.Bar(name="EBIT FY25E",    x=SEGMENTS["Segment"],
                         y=SEGMENTS["EBIT_FY25"], marker_color=ORANGE, opacity=0.9))
    fig.add_trace(go.Bar(name="EBIT FY24",     x=SEGMENTS["Segment"],
                         y=SEGMENTS["EBIT_FY24"], marker_color=ORANGE, opacity=0.4))
    fig.update_layout(barmode="group", height=320, **_L,
                      yaxis=dict(tickprefix="$", ticksuffix="M",
                                 gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


def dcf_bar_chart(result):
    yrs  = [r["Year"] for r in result["rows"]]
    fcff = [r["FCFF ($M)"] for r in result["rows"]]
    pvs  = [r["PV FCFF ($M)"] for r in result["rows"]]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=yrs, y=fcff, name="FCFF", marker_color=NAVY, opacity=0.85,
                         text=[f"${v:,}" for v in fcff], textposition="outside",
                         textfont=dict(color="#1A1A2E", size=10)))
    fig.add_trace(go.Bar(x=yrs, y=pvs, name="PV of FCFF", marker_color=ORANGE, opacity=0.85))
    fig.update_layout(barmode="group", height=290, **_L,
                      yaxis=dict(tickprefix="$", ticksuffix="M",
                                 gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


def forecast_chart(rows, historical):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    hy  = list(historical["Year"])
    hr  = list(historical["Revenue"])
    py  = [r["Year"] for r in rows]
    pr  = [r["Revenue ($M)"] for r in rows]
    pni = [r["NI ($M)"] for r in rows]
    fig.add_trace(go.Scatter(x=hy, y=hr, name="Revenue (Hist.)",
                             line=dict(color=NAVY, width=2.5), mode="lines+markers",
                             marker=dict(size=6, color=NAVY)), secondary_y=False)
    fig.add_trace(go.Scatter(x=py, y=pr, name="Revenue (Proj.)",
                             line=dict(color=NAVY, width=2.5, dash="dash"), mode="lines+markers",
                             marker=dict(size=7, color=NAVY, symbol="diamond")), secondary_y=False)
    fig.add_trace(go.Scatter(x=py, y=pni, name="NI (Proj.)",
                             line=dict(color=ORANGE, width=2, dash="dash"), mode="lines+markers",
                             marker=dict(size=6, color=ORANGE)), secondary_y=True)
    fig.add_vline(x=2.5, line_dash="dot", line_color=GOLD,
                  annotation_text="← Actual  |  Projected →",
                  annotation_font=dict(color=GOLD, size=11),
                  annotation_position="top")
    fig.update_layout(height=360, **_L,
                      yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#F0F0F0",
                                 tickfont=dict(color="#374151"),
                                 title=dict(text="Revenue $M", font=dict(color="#374151"))),
                      yaxis2=dict(tickprefix="$", ticksuffix="M", gridcolor="#F0F0F0",
                                  tickfont=dict(color="#374151"),
                                  title=dict(text="Net Income $M", font=dict(color="#374151"))))
    fig.update_xaxes(tickfont=dict(color="#374151"))
    return fig


def scenario_bar_chart():
    cfgs = {"Bull": (35.0, 30.0, GREEN), "Base": (27.0, 22.0, NAVY), "Bear": (15.0, 14.0, RED)}
    metrics = ["Revenue ($B)", "Net Income ($B)", "FCFF ($B)"]
    fig = go.Figure()
    for name, (rg, em, col) in cfgs.items():
        r = BASE["revenue"]
        for _ in range(5): r *= (1 + rg/100)
        ni_   = r * em/100 * 0.79
        fcff_ = ni_ * 0.92
        vals  = [round(r/1000, 1), round(ni_/1000, 1), round(fcff_/1000, 1)]
        fig.add_trace(go.Bar(name=name, x=metrics, y=vals, marker_color=col, opacity=0.85,
                             text=[f"${v}B" for v in vals], textposition="outside",
                             textfont=dict(color="#1A1A2E", size=11)))
    fig.update_layout(barmode="group", height=300, **_L,
                      title=dict(text="Scenario Comparison — FY2030E",
                                 font=dict(color="#1A1A2E", size=13)),
                      yaxis=dict(tickprefix="$", ticksuffix="B",
                                 gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                      xaxis=dict(tickfont=dict(color="#374151")))
    return fig


def radar_chart():
    cats = ["Valuation<br>(inv. P/E)", "EBIT Margin", "Rev. Growth", "AI Moat", "Gov. Revenue"]
    cos  = [
        ("Palantir", [5, 39, 72, 95, 88], ORANGE),
        ("Snowflake",[10, 0, 75, 70, 5],  NAVY),
        ("Datadog",  [12, 36, 65, 68, 10], TEAL),
        ("C3.ai",    [8, 0, 45, 55, 60],  GOLD),
    ]
    fig = go.Figure()
    for name, vals, col in cos:
        fig.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]],
            fill="toself", name=name,
            line=dict(color=col, width=2),
            fillcolor=col, opacity=0.18 if name != "Palantir" else 0.28,
        ))
    fig.update_layout(height=340, paper_bgcolor="#FFFFFF",
                      polar=dict(
                          radialaxis=dict(visible=True, range=[0, 110],
                                          tickfont=dict(color="#9CA3AF"),
                                          gridcolor="#E5E7EB"),
                          angularaxis=dict(tickfont=dict(color="#374151", size=11))
                      ),
                      legend=dict(orientation="h", y=-0.08, font=dict(color="#374151", size=11)),
                      margin=dict(l=30, r=30, t=30, b=50),
                      font=dict(color="#1A1A2E", family="Inter"))
    return fig


def mc_simulation(rev_cagr, ebit_m, wacc, g_term, live_price, n=1500):
    np.random.seed(42)
    intrinsics = []
    for _ in range(n):
        g_s = np.random.triangular(rev_cagr-5, rev_cagr, rev_cagr+5)
        m_s = np.random.triangular(ebit_m-5,   ebit_m,  ebit_m+5)
        w_s = np.random.triangular(wacc-1.5,   wacc,    wacc+1.5)
        r   = run_dcf(w_s, g_term, g_s, m_s, live_price)
        if r: intrinsics.append(r["ivps"])
    return np.array(intrinsics)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style="background:linear-gradient(160deg,#0f2040 0%,#1D3557 60%,#0f2040 100%);
            padding:18px 16px 14px;border-radius:12px;margin-bottom:1.2rem;
            border:1px solid rgba(230,57,70,0.35);
            box-shadow:0 4px 20px rgba(0,0,0,0.3);">

  <!-- Palantir SVG Logo -->
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
    <svg width="38" height="38" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer ring -->
      <circle cx="50" cy="50" r="46" fill="none" stroke="{ORANGE}" stroke-width="5" opacity="0.9"/>
      <!-- Inner filled circle -->
      <circle cx="50" cy="50" r="28" fill="{ORANGE}" opacity="0.95"/>
      <!-- Center dot -->
      <circle cx="50" cy="50" r="10" fill="white"/>
      <!-- Scan lines -->
      <line x1="4" y1="50" x2="22" y2="50" stroke="{ORANGE}" stroke-width="3" opacity="0.6"/>
      <line x1="78" y1="50" x2="96" y2="50" stroke="{ORANGE}" stroke-width="3" opacity="0.6"/>
      <line x1="50" y1="4" x2="50" y2="22" stroke="{ORANGE}" stroke-width="3" opacity="0.6"/>
      <line x1="50" y1="78" x2="50" y2="96" stroke="{ORANGE}" stroke-width="3" opacity="0.6"/>
    </svg>
    <div>
      <div style="font-size:1.05rem;font-weight:900;color:#fff;letter-spacing:2px;
                  font-family:'Space Grotesk','Inter',sans-serif;text-transform:uppercase;">
        PALANTIR
      </div>
      <div style="font-size:0.58rem;color:rgba(255,255,255,0.45);letter-spacing:2.5px;
                  text-transform:uppercase;margin-top:1px;">Technologies · NYSE: PLTR</div>
    </div>
  </div>

  <!-- Terminal label -->
  <div style="background:rgba(230,57,70,0.15);border:1px solid rgba(230,57,70,0.3);
              border-radius:6px;padding:6px 10px;margin-bottom:10px;">
    <div style="font-size:0.73rem;font-weight:800;color:{ORANGE};letter-spacing:1.5px;
                text-transform:uppercase;font-family:'Inter',sans-serif;">
      ⬡ Research Terminal
    </div>
    <div style="font-size:0.62rem;color:rgba(255,255,255,0.5);margin-top:2px;">
      Damodaran Framework · Live Data · AI Analysis
    </div>
  </div>

  <!-- Mission -->
  <div style="font-size:0.65rem;color:rgba(255,255,255,0.55);font-style:italic;
              line-height:1.6;border-top:1px solid rgba(255,255,255,0.1);padding-top:8px;">
    "We exist to help the world's most important institutions use data to solve their hardest problems."
  </div>
</div>
""", unsafe_allow_html=True)

PAGE = st.sidebar.radio("Navigate", [
    "🔵  Live Market",
    "🏭  Industry Analysis",
    "💰  Valuation (DCF)",
    "📈  Forecasting",
    "⚔️   Competition",
    "🔄  Life Cycle",
    "🎯  Marketing Strategy",
    "🧠  AIP Deep Dive",
    "⚠️  Risk Matrix",
    "📰  Live News",
])

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="font-size:0.78rem;color:#94A3B8;line-height:1.9;">
  <b style="color:#CBD5E1;">Data Sources</b><br>
  · Live price: Yahoo Finance<br>
  · Fundamentals: PLTR 10-K FY21–FY25E<br>
  · News: Google News RSS<br>
  · Framework: Damodaran (NYU Stern)<br>
  <br>
</div>
<div style="background:linear-gradient(135deg,rgba(230,57,70,0.18) 0%,rgba(42,157,143,0.12) 100%);
            border:1px solid rgba(230,57,70,0.35);border-radius:10px;
            padding:10px 12px;margin-bottom:10px;">
  <div style="font-size:0.62rem;color:rgba(255,255,255,0.45);text-transform:uppercase;
              letter-spacing:1.2px;margin-bottom:4px;">Prepared by</div>
  <div style="font-size:0.9rem;font-weight:900;color:{GOLD};
              font-family:'Space Grotesk','Inter',sans-serif;letter-spacing:0.3px;">
    Krrish Bahuguna
  </div>
  <div style="font-size:0.7rem;color:#94A3B8;margin-top:2px;">
    IPM2 · MBA Corporate Finance
  </div>
  <div style="font-size:0.62rem;color:rgba(255,255,255,0.35);margin-top:6px;font-style:italic;">
    Academic use only — not investment advice
  </div>
</div>
<div style="font-size:0.68rem;color:#64748B;">
  <b style="color:#94A3B8;">Refreshed:</b><br>
  {datetime.now().strftime("%d %b %Y  %H:%M")}
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🔄  Refresh Live Data"):
    st.cache_data.clear()
    st.rerun()


# ── LIVE DATA ─────────────────────────────────────────────────────────────────
live      = get_live_price()
chg_sign  = "+" if live["change"] >= 0 else ""
chg_arrow = "▲" if live["change"] >= 0 else "▼"
chg_color = "#16A34A" if live["change"] >= 0 else "#DC2626"

# ── MASTER HEADER ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{NAVY} 0%,#0f2040 35%,#1a3a6a 65%,{ORANGE} 100%);
            padding:1.6rem 2rem;border-radius:16px;margin-bottom:0.6rem;
            box-shadow:0 8px 32px rgba(29,53,87,0.32);">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:14px;">
    <div>
      <!-- Logo row -->
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:8px;">
        <svg width="48" height="48" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
          <circle cx="50" cy="50" r="46" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="4"/>
          <circle cx="50" cy="50" r="46" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="80 210" stroke-linecap="round"/>
          <circle cx="50" cy="50" r="30" fill="{ORANGE}" opacity="0.9"/>
          <circle cx="50" cy="50" r="12" fill="white" opacity="0.95"/>
          <line x1="4" y1="50" x2="20" y2="50" stroke="rgba(255,255,255,0.5)" stroke-width="3"/>
          <line x1="80" y1="50" x2="96" y2="50" stroke="rgba(255,255,255,0.5)" stroke-width="3"/>
          <line x1="50" y1="4" x2="50" y2="20" stroke="rgba(255,255,255,0.5)" stroke-width="3"/>
          <line x1="50" y1="80" x2="50" y2="96" stroke="rgba(255,255,255,0.5)" stroke-width="3"/>
        </svg>
        <div>
          <div style="font-size:0.62rem;color:rgba(255,255,255,0.45);letter-spacing:3px;
                      text-transform:uppercase;font-family:'Inter',sans-serif;">NYSE: PLTR</div>
          <div style="font-size:1.6rem;font-weight:900;color:#fff;letter-spacing:1px;
                      font-family:'Space Grotesk','Inter',sans-serif;line-height:1.1;">
            PALANTIR TECHNOLOGIES
          </div>
          <div style="font-size:0.75rem;color:rgba(255,255,255,0.55);margin-top:2px;
                      font-family:'Inter',sans-serif;letter-spacing:0.5px;">
            Research Terminal · Damodaran Framework · Forecasting · Valuation · Marketing Strategy
          </div>
        </div>
      </div>
      <!-- Price row -->
      <div style="display:flex;align-items:baseline;gap:1.4rem;flex-wrap:wrap;margin-top:6px;">
        <span style="font-size:2.8rem;font-weight:900;color:#fff;
                     font-family:'Space Grotesk','Inter',sans-serif;line-height:1;">${live['price']}</span>
        <span style="font-size:1rem;color:{chg_color};font-weight:800;
                     background:rgba(255,255,255,0.14);padding:5px 14px;
                     border-radius:99px;font-family:'Inter',sans-serif;
                     border:1px solid rgba(255,255,255,0.1);">
          {chg_arrow} {chg_sign}{live['change']} ({chg_sign}{live['change_pct']}%)
        </span>
        <span style="font-size:0.75rem;color:rgba(255,255,255,0.45);font-family:'Inter',sans-serif;">
          Live via Yahoo Finance &nbsp;·&nbsp; {datetime.now().strftime("%d %B %Y")}
        </span>
      </div>
    </div>
    <div style="text-align:right;font-family:'Inter',sans-serif;">
      <div style="font-size:0.72rem;color:rgba(255,255,255,0.6);">Mkt Cap: <b style="color:#fff;">{live['market_cap']}</b></div>
      <div style="font-size:0.72rem;margin-top:4px;color:rgba(255,255,255,0.6);">Volume: <b style="color:#fff;">{live['volume']}</b></div>
      <div style="font-size:0.72rem;margin-top:4px;color:rgba(255,255,255,0.6);">52W: <b style="color:#fff;">${live['52w_low']} – ${live['52w_high']}</b></div>
      <div style="font-size:0.72rem;margin-top:4px;color:rgba(255,255,255,0.6);">Beta: <b style="color:#fff;">{live['beta']}</b>
        &nbsp;·&nbsp; Fwd P/E: <b style="color:#fff;">{live['fwd_pe']}×</b></div>
      <div style="margin-top:10px;background:rgba(230,57,70,0.2);border:1px solid rgba(230,57,70,0.4);
                  border-radius:8px;padding:5px 10px;font-size:0.68rem;color:{GOLD};font-weight:800;">
        ✦ Krrish Bahuguna · IPM2
      </div>
    </div>
  </div>
</div>
<div class="mission-strip">
  "We exist to help the world's most important institutions use data to solve their hardest problems." — Palantir Mission
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — LIVE MARKET
# ═════════════════════════════════════════════════════════════════════════════
if PAGE == "🔵  Live Market":
    st.markdown('<div class="narrative">Every analysis begins with the present — what the market believes right now. Palantir\'s market price reflects extraordinary expectations: a stock priced for near-perfection in the AI era. The analyst who ignores this premium pays for it; the one who only sees it misses the underlying platform power.</div>', unsafe_allow_html=True)

    kpis = [
        ("Current Price",    f"${live['price']}",       f"{chg_sign}{live['change_pct']}% today"),
        ("Market Cap",       live["market_cap"],          "NYSE listed"),
        ("P/E Ratio (TTM)",  f"{live['pe']}×",           "vs Software ~60×"),
        ("Fwd P/E",          f"{live['fwd_pe']}×",       "NTM consensus"),
        ("Dividend Yield",   f"{live['div_yield']}%",    "No dividend (growth reinvestment)"),
        ("Beta (β)",         f"{live['beta']}",           "vs S&P 500"),
    ]
    cols = st.columns(6)
    for col, (lbl, val, sub) in zip(cols, kpis):
        col.markdown(
            f'<div class="kpi-card"><div class="kpi-label">{lbl}</div>'
            f'<div class="kpi-value">{val}</div>'
            f'<div class="kpi-sub">{sub}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="sec-head">Live Price Chart — 6-Month Candlestick with Moving Averages</div>', unsafe_allow_html=True)
    period_sel = st.selectbox("Chart Period", ["1mo","3mo","6mo","1y","2y"], index=2)
    hist_df = get_price_history(period_sel)
    st.plotly_chart(candlestick_chart(hist_df), use_container_width=True)

    st.markdown('<div class="sec-head">Financial Fingerprint — FY2025E vs FY2024</div>', unsafe_allow_html=True)
    fp_items = [
        ("Revenue (FY25E)", "$3,754M", "+31.0% vs FY24"),
        ("U.S. Commercial Growth", "+52% YoY", "Fastest-growing segment"),
        ("Adj. EBIT Margin", "19.5%", "Expanding from 12.5% FY24"),
        ("FCFF (FY25E)", "$1,630M", "+41% vs FY24 FCFF"),
        ("Net Cash", "$5.2B", "Debt-free balance sheet"),
        ("Customer Count", "700+", "AIP-driven acceleration"),
    ]
    c1, c2, c3 = st.columns(3)
    for i, (lbl, val, sig) in enumerate(fp_items):
        col = [c1, c2, c3][i % 3]
        col.markdown(f"""
        <div class="fp-card">
          <div class="fp-label">{lbl}</div>
          <div class="fp-value">{val}</div>
          <div class="fp-signal">{sig}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Revenue & EBIT Trend — FY2021 to FY2025E</div>', unsafe_allow_html=True)
    st.plotly_chart(rev_ni_chart(), use_container_width=True)

    st.markdown('<div class="sec-head">Segment Breakdown — Revenue & EBIT</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(segment_rev_chart(), use_container_width=True)
    with c2: st.plotly_chart(segment_margin_chart(), use_container_width=True)

    st.markdown('<div class="sec-head">Investment Thesis at a Glance</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="q-card-navy">
      <b style="color:{NAVY};">The Palantir Thesis in One Paragraph</b><br>
      <span style="font-size:0.87rem;color:#1e3a5f;">
        Palantir is the only enterprise AI company with simultaneous deep roots in both the U.S. 
        government intelligence apparatus and commercial Fortune 500 AI deployment. 
        Its Artificial Intelligence Platform (AIP) is converting proof-of-concept contracts into 
        recurring production revenue at an accelerating rate. The moat is not the software — 
        it is the ontology, the classified data integrations, and the switching cost of mission-critical 
        operational workflows. The risk is the valuation: the market is pricing in execution perfection 
        for the next decade. Any deceleration in U.S. commercial growth or government budget cuts would 
        compress the multiple violently.
      </span>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — INDUSTRY ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🏭  Industry Analysis":
    st.markdown('<div class="narrative">Palantir operates at the intersection of three of the fastest-growing technology markets: enterprise AI software, defence and intelligence platforms, and big data analytics. Understanding the industry structure explains both the extraordinary growth runway and the competitive risks that could erode it.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Porter\'s Five Forces — AI Platform & Government Data Analytics</div>', unsafe_allow_html=True)
    forces = [
        ("🏭 Competitive Rivalry", "MEDIUM-HIGH",
         "Snowflake, Databricks, and C3.ai in commercial; Booz Allen Hamilton, Leidos, SAIC in government. However, no single rival matches Palantir's classified cross-domain integration breadth.",
         "q-card-orange"),
        ("🚪 Threat of New Entrants", "LOW-MEDIUM",
         "FedRAMP authorization, classified system accreditations (IL4/IL5/IL6), and deep FISA/SIGINT integration are multi-year barriers. For commercial AI, Microsoft, Google, and AWS are formidable incumbents.",
         "q-card-navy"),
        ("🔄 Supplier Power", "LOW",
         "Palantir is cloud-agnostic (AWS, Azure, GCP, on-prem). Data infrastructure commoditization reduces dependency. Human capital (cleared personnel) is the most constrained supplier input.",
         "q-card-teal"),
        ("🛒 Buyer Power", "MEDIUM",
         "Government clients negotiate multi-year IDIQ contracts — predictable but price-sensitive. Commercial clients face lock-in once AIP is embedded in workflows; early-stage buyers have leverage during boot camps.",
         "q-card-gold"),
        ("⚡ Threat of Substitutes", "MEDIUM",
         "Open-source LLM frameworks (LangChain, Hugging Face) + cloud-native analytics (BigQuery, Redshift) could substitute for non-classified use cases. Government classified remains highly defensible.",
         "q-card-red"),
    ]
    for title, rating, desc, card_cls in forces:
        st.markdown(f"""
        <div class="{card_cls}">
          <b>{title}</b> &nbsp; <span class="tag-orange">{rating}</span><br>
          <span style="font-size:0.85rem;color:#374151;">{desc}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Total Addressable Market (TAM) Sizing — FY2025–FY2030</div>', unsafe_allow_html=True)
    tam = pd.DataFrame([
        {"Segment":"U.S. Federal AI/Analytics","TAM FY25 ($B)":18,"TAM FY30E ($B)":52,"CAGR":24,"PLTR Share FY25":"~6%","Notes":"NDAA AI mandates driving spend"},
        {"Segment":"Allied Government (NATO+)","TAM FY25 ($B)":12,"TAM FY30E ($B)":35,"CAGR":24,"PLTR Share FY25":"~5%","Notes":"Ukraine war accelerating EU defence AI"},
        {"Segment":"U.S. Enterprise AI Platforms","TAM FY25 ($B)":38,"TAM FY30E ($B)":160,"CAGR":33,"PLTR Share FY25":"~2%","Notes":"AIP bootcamp driving rapid conversion"},
        {"Segment":"Healthcare & Life Sciences AI","TAM FY25 ($B)":15,"TAM FY30E ($B)":55,"CAGR":30,"PLTR Share FY25":"~1%","Notes":"NHS, Cleveland Clinic deployments"},
        {"Segment":"Industrial/Supply Chain AI","TAM FY25 ($B)":22,"TAM FY30E ($B)":75,"CAGR":28,"PLTR Share FY25":"<1%","Notes":"Emerging via AIP commercial expansion"},
    ])
    st.dataframe(tam, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Industry Megatrends Driving Palantir\'s Addressable Market</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="q-card-navy">
          <b style="color:{NAVY};">Tailwinds (Multi-Year)</b><br>
          <span style="font-size:0.84rem;color:#1e3a5f;">
            · AI mandates in U.S. National Security strategy (NSCAI, EO 14110)<br>
            · NATO Allied nations AI capability gap — EU increasing defence budgets to 2%+ GDP<br>
            · Enterprise AI adoption moving from PoC to production at scale (AIP Boot Camps)<br>
            · U.S. government data modernization: cloud migration of legacy DoD/IC systems<br>
            · Geopolitical tensions elevating demand for battlefield AI and decision platforms<br>
            · Rising U.S. commercial AI spend: $150B+ by 2027 (IDC estimates)
          </span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="q-card-red">
          <b style="color:{RED};">Headwinds & Structural Risks</b><br>
          <span style="font-size:0.84rem;color:#7A1A0A;">
            · Congressional budget sequestration risk (Continuing Resolutions slow award cycles)<br>
            · Microsoft Azure OpenAI + AWS SageMaker encroaching on commercial AI workflow<br>
            · International government revenue stagnation in non-Five Eyes markets<br>
            · Open-source AI (Llama 3, Mistral) reducing LLM moat component<br>
            · Stock-based compensation dilution: ~10% of revenue annually<br>
            · Geopolitical complexity: some EU nations restricting U.S. AI for sovereignty reasons
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Regulatory & Geopolitical Landscape</div>', unsafe_allow_html=True)
    reg = pd.DataFrame([
        {"Jurisdiction":"United States","Key Regulation":"NDAA Section 232 AI mandates; EO 14110 AI safety; FedRAMP High","Impact on PLTR":"Positive — mandates government AI adoption; PLTR is preferred vendor","Risk Level":"Low"},
        {"Jurisdiction":"European Union","Key Regulation":"EU AI Act (risk-based classification); GDPR data residency requirements","Impact on PLTR":"Medium — high-risk AI classification adds compliance cost; data sovereignty creates friction","Risk Level":"Medium"},
        {"Jurisdiction":"United Kingdom","Key Regulation":"NHS AI Framework; NCSC cloud security standards","Impact on PLTR":"Positive — NHS AIP deployment; GCHQ intelligence sharing relationship","Risk Level":"Low"},
        {"Jurisdiction":"Five Eyes Alliance","Key Regulation":"UKUSA Agreement data sharing; classified network access protocols","Impact on PLTR":"Strongly positive — PLTR is structurally embedded in Five Eyes intelligence infrastructure","Risk Level":"Very Low"},
        {"Jurisdiction":"China / Russia","Key Regulation":"Export control restrictions (EAR); OFAC sanctions compliance","Impact on PLTR":"Neutral — PLTR already avoids these markets by policy","Risk Level":"Low"},
    ])
    st.dataframe(reg, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — VALUATION (DCF)
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "💰  Valuation (DCF)":
    st.markdown('<div class="narrative">Valuing Palantir is an exercise in honest uncertainty. The company is transitioning from a government-dependent contractor to an AI platform company. Traditional DCF metrics struggle with a business that has 80%+ gross margins, zero debt, $5B+ net cash, and a customer base of sovereign governments and Fortune 500 enterprises. We model three scenarios — each defensible.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Interactive DCF Model — Adjust Assumptions</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: wacc      = st.slider("WACC (%)",       7.0, 15.0, 10.0, 0.5)
    with c2: g_term    = st.slider("Terminal Growth (%)", 2.0, 6.0,  4.0, 0.5)
    with c3: rev_cagr  = st.slider("Revenue CAGR (%)", 5.0, 45.0, 27.0, 1.0)
    with c4: ebit_margin = st.slider("EBIT Margin (%)", 10.0, 45.0, 22.0, 1.0)

    result = run_dcf(wacc, g_term, rev_cagr, ebit_margin, live["price"])
    if result is None:
        st.error("⚠️ Invalid: WACC must exceed Terminal Growth Rate. Adjust sliders.")
    else:
        iv, up = result["ivps"], result["upside"]
        iv_color = GREEN if up > 0 else RED
        rating   = "BUY" if up > 20 else ("HOLD" if up > -15 else "SELL")
        rat_col  = GREEN if rating == "BUY" else (GOLD if rating == "HOLD" else RED)

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.markdown(f'<div class="kpi-card"><div class="kpi-label">Intrinsic Value/Share</div><div class="kpi-value" style="color:{iv_color};">${iv}</div><div class="kpi-sub">DCF (5Y explicit)</div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="kpi-card"><div class="kpi-label">Market Price</div><div class="kpi-value">${live["price"]}</div><div class="kpi-sub">Live (Yahoo Finance)</div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="kpi-card"><div class="kpi-label">Upside / Downside</div><div class="kpi-value" style="color:{iv_color};">{up:+.1f}%</div><div class="kpi-sub">vs current price</div></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="kpi-card"><div class="kpi-label">Enterprise Value</div><div class="kpi-value">${result["ev"]/1000:.1f}B</div><div class="kpi-sub">PV(FCFFs) + PV(TV)</div></div>', unsafe_allow_html=True)
        k5.markdown(f'<div class="kpi-card"><div class="kpi-label">Model Verdict</div><div class="kpi-value" style="color:{rat_col};">{rating}</div><div class="kpi-sub">Based on DCF upside</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-head">5-Year Projection Table</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(result["rows"]), use_container_width=True, hide_index=True)
        st.plotly_chart(dcf_bar_chart(result), use_container_width=True)

        st.markdown('<div class="sec-head">Value Bridge — Explicit Period vs Terminal Value</div>', unsafe_allow_html=True)
        bridge_fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative","relative","relative","total"],
            x=["PV Explicit FCFFs","PV Terminal Value","Net Cash (debt-free)","Equity Value"],
            y=[result["pv_explicit"], result["pv_tv"], BASE["net_cash"], 0],
            connector=dict(line=dict(color=BORDER)),
            decreasing=dict(marker_color=RED),
            increasing=dict(marker_color=NAVY),
            totals=dict(marker_color=ORANGE),
            text=[f"${v/1000:.1f}B" for v in [result["pv_explicit"], result["pv_tv"], BASE["net_cash"], result["eq_val"]]],
            textposition="outside"
        ))
        bridge_fig.update_layout(height=300, **_L,
                                  yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#F0F0F0",
                                             tickfont=dict(color="#374151")),
                                  xaxis=dict(tickfont=dict(color="#374151")))
        st.plotly_chart(bridge_fig, use_container_width=True)

        st.markdown('<div class="sec-head">Sensitivity Analysis — IVPS ($/share)</div>', unsafe_allow_html=True)
        st.markdown('<span style="font-size:0.82rem;color:#6B7280;">Rows = Terminal Growth Rate; Columns = WACC. Higher WACC + lower growth = lower value.</span>', unsafe_allow_html=True)
        sens = sensitivity_table(rev_cagr, ebit_margin, live["price"])
        st.dataframe(sens.style.background_gradient(cmap="RdYlGn", axis=None), use_container_width=True)

    st.markdown('<div class="sec-head">Scenario Analysis — Bull / Base / Bear</div>', unsafe_allow_html=True)
    scenarios = [
        ("🐂 Bull Case",  35.0, 30.0, 9.5,  4.5, "q-card-green",
         "AIP achieves hyper-growth across enterprise verticals. U.S. Commercial revenue +60% p.a. Government budget increases. Margin expands to 30%+ as operating leverage kicks in. Platform multiple sustains 150–200× Fwd P/E."),
        ("📊 Base Case",  27.0, 22.0, 10.0, 4.0, "q-card-navy",
         "AIP boot camp conversion continues; U.S. Commercial +40%, International Government +20%. EBIT margin expands steadily to 22–25% by FY2028. Stock re-rates from 170× to 100–120× Fwd P/E as growth sustains."),
        ("🐻 Bear Case",  15.0, 14.0, 11.5, 3.0, "q-card-red",
         "Government budget sequestration slows PLTR's largest revenue segment. Commercial AIP growth disappoints below 30%. Microsoft/AWS displace pipeline deals. Multiple compression to 50–70× Fwd P/E is painful at current prices."),
    ]
    for sname, rg, em, wc, gt, card_cls, desc in scenarios:
        r = run_dcf(wc, gt, rg, em, live["price"])
        if r:
            st.markdown(f"""
            <div class="{card_cls}">
              <b>{sname}</b> &nbsp;
              <span class="tag-navy">Rev CAGR {rg:.0f}%</span>&nbsp;
              <span class="tag-orange">EBIT {em:.0f}%</span>&nbsp;
              <span class="tag-teal">WACC {wc}%</span>&nbsp;
              → &nbsp;<b>IVPS: ${r['ivps']}</b> &nbsp; ({r['upside']:+.1f}% vs current)<br>
              <span style="font-size:0.83rem;color:#374151;margin-top:6px;display:block;">{desc}</span>
            </div>""", unsafe_allow_html=True)
    st.plotly_chart(scenario_bar_chart(), use_container_width=True)

    st.markdown('<div class="sec-head">Monte Carlo Simulation — 1,500 Trials</div>', unsafe_allow_html=True)
    sims = mc_simulation(rev_cagr, ebit_margin, wacc, g_term, live["price"])
    if len(sims) > 0:
        mc_fig = go.Figure()
        mc_fig.add_trace(go.Histogram(x=sims, nbinsx=60, marker_color=NAVY, opacity=0.75, name="Simulated IVPS"))
        mc_fig.add_vline(x=live["price"], line_dash="dash", line_color=RED,
                         annotation_text=f"Market: ${live['price']}", annotation_font_color=RED)
        mc_fig.add_vline(x=np.mean(sims), line_dash="dot", line_color=ORANGE,
                         annotation_text=f"Mean: ${np.mean(sims):.0f}", annotation_font_color=ORANGE)
        mc_fig.update_layout(height=300, **_L,
                             xaxis=dict(tickprefix="$", tickfont=dict(color="#374151"), title="Intrinsic Value per Share"),
                             yaxis=dict(tickfont=dict(color="#374151"), title="Frequency"))
        st.plotly_chart(mc_fig, use_container_width=True)
        p10, p50, p90 = np.percentile(sims, [10, 50, 90])
        prob_above = (sims >= live["price"]).mean() * 100
        st.markdown(f"""
        <div class="q-card-navy">
          <b style="color:{NAVY};">Monte Carlo Summary ({len(sims):,} trials)</b><br>
          <span style="font-size:0.85rem;color:#1e3a5f;">
            P10 (pessimistic): <b>${p10:.2f}</b> &nbsp;·&nbsp;
            P50 (median): <b>${p50:.2f}</b> &nbsp;·&nbsp;
            P90 (optimistic): <b>${p90:.2f}</b><br>
            Probability IVPS ≥ market price (${live["price"]}): <b>{prob_above:.1f}%</b>
          </span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Relative Valuation — Peer Comparison</div>', unsafe_allow_html=True)
    st.dataframe(PEERS, use_container_width=True, hide_index=True)
    st.markdown(f"""
    <div class="q-card-orange">
      <b style="color:{ORANGE};">Valuation Verdict</b><br>
      <span style="font-size:0.85rem;color:#7A2800;">
        Palantir trades at a structural premium to every software peer on P/E and Price/Sales metrics.
        This premium is partially justified by its unique government-commercial platform duality,
        accelerating U.S. commercial growth, and $5B+ net cash cushion. However, DCF analysis
        under base assumptions ($3,754M revenue, 27% CAGR, 22% EBIT margin, 10% WACC)
        suggests the stock is pricing in extended perfection. The margin of safety is thin.
        Only the bull case (35%+ revenue CAGR) justifies the current multiple.
      </span>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — FORECASTING
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "📈  Forecasting":
    st.markdown('<div class="narrative">Forecasting Palantir requires separating the government baseline (predictable, sticky, slower-growing) from the commercial acceleration (high variance, high upside). The AIP boot camp model is a genuine innovation in enterprise software sales — but conversion rates matter as much as the funnel size.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Revenue Forecast — Build Your Own Model</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: fc_cagr  = st.slider("Revenue CAGR (%)", 5.0, 45.0, 27.0, 1.0, key="fc_cagr")
    with c2: fc_ebit  = st.slider("EBIT Margin (%)", 8.0, 40.0, 22.0, 0.5, key="fc_ebit")
    with c3: tax_rate_fc = st.slider("Tax Rate (%)", 15.0, 25.0, 21.0, 0.5, key="fc_tax")

    fc_rows = []
    prev_rev = BASE["revenue"]
    for i in range(1, 6):
        rev_i  = BASE["revenue"] * (1 + fc_cagr/100) ** i
        ebit_i = rev_i * fc_ebit / 100
        ni_i   = ebit_i * (1 - tax_rate_fc/100)
        eps_i  = ni_i / (BASE["shares"] * 1000)
        drv    = rev_i - prev_rev
        fcff_i = ni_i - drv / 3.5 + BASE["da"] * (1 + 0.05*i)
        prev_rev = rev_i
        fc_rows.append({
            "Year":          f"FY{25+i}E",
            "Revenue ($M)":  int(rev_i),
            "Rev Growth":    f"{fc_cagr:.1f}%",
            "EBIT ($M)":     int(ebit_i),
            "EBIT Margin":   f"{fc_ebit:.1f}%",
            "Net Income ($M)": int(ni_i),
            "EPS ($)":       round(eps_i, 2),
            "FCFF ($M)":     int(fcff_i),
        })

    st.dataframe(pd.DataFrame(fc_rows), use_container_width=True, hide_index=True)
    st.plotly_chart(forecast_chart(fc_rows, HIST), use_container_width=True)

    st.markdown('<div class="sec-head">Segment-Level Forecasts — FY2025E–FY2028E</div>', unsafe_allow_html=True)
    seg_fc = pd.DataFrame([
        {"Segment":"U.S. Commercial",   "FY25E ($M)":902, "FY26E ($M)":1264,"FY27E ($M)":1770,"FY28E ($M)":2478,"CAGR (3Y)":"~40%","Drivers":"AIP Boot Camps; Fortune 500 scaling; healthcare + finance verticals"},
        {"Segment":"U.S. Government",   "FY25E ($M)":1199,"FY26E ($M)":1379,"FY27E ($M)":1586,"FY28E ($M)":1824,"CAGR (3Y)":"~15%","Drivers":"DoD AI mandates; TITAN program; Army/NGA renewals"},
        {"Segment":"International Comm.","FY25E ($M)":639,"FY26E ($M)":767, "FY27E ($M)":920, "FY28E ($M)":1104,"CAGR (3Y)":"~20%","Drivers":"EMEA healthcare + manufacturing; Japan + Australia expansion"},
        {"Segment":"International Gov.", "FY25E ($M)":1014,"FY26E ($M)":1115,"FY27E ($M)":1227,"FY28E ($M)":1350,"CAGR (3Y)":"~10%","Drivers":"NATO defence AI; UK NHS; allied intelligence platforms"},
    ])
    st.dataframe(seg_fc, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">AIP Boot Camp — The Growth Engine</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="q-card-orange">
      <b style="color:{ORANGE};">What is AIP Boot Camp and why does it matter?</b><br>
      <span style="font-size:0.85rem;color:#7A2800;">
        Palantir's AIP Boot Camp is a 3–5 day intensive workshop where enterprise clients build 
        working AI prototypes on their own data using Palantir's platform. Boot Camps compress 
        the traditional 6–18 month enterprise SaaS evaluation cycle into days. Conversion from 
        Boot Camp to paid contract has been consistently above 30%. In FY2024, Palantir ran 
        hundreds of Boot Camps globally, and U.S. Commercial revenue grew 52% YoY as a result. 
        The model is capital-light and scalable — each Boot Camp is a high-conversion sales motion 
        that also trains the client's team on PLTR's platform, deepening switching costs.
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Key Forecast Risks & Assumptions</div>', unsafe_allow_html=True)
    risks = pd.DataFrame([
        {"Risk Factor":"U.S. Commercial Growth","Base Assumption":"40–50% YoY","Bear Case Trigger":"AIP Boot Camp conversion drops below 20%","Bull Case Trigger":"Fortune 500 AIP mandates company-wide (100+ seats)"},
        {"Risk Factor":"U.S. Government Revenue","Base Assumption":"12–18% YoY","Bear Case Trigger":"CR/budget sequestration; DoD IT freeze","Bull Case Trigger":"TITAN, Maven Smart System, classified AI contract expansions"},
        {"Risk Factor":"EBIT Margin Expansion","Base Assumption":"~200–300bps/year","Bear Case Trigger":"SBC remains >10% of revenue; hiring surge","Bull Case Trigger":"Operating leverage accelerates; gross margin approaches 85%"},
        {"Risk Factor":"International Government","Base Assumption":"8–12% YoY","Bear Case Trigger":"European AI Act compliance friction; budget constraints","Bull Case Trigger":"NATO AI acceleration; Ukraine war creates new defence deployments"},
        {"Risk Factor":"Stock Dilution (SBC)","Base Assumption":"~1.5–2% annual share count growth","Bear Case Trigger":"Aggressive new grants; employee option exercise","Bull Case Trigger":"PLTR moves to cash compensation; buyback program"},
    ])
    st.dataframe(risks, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Historical vs Projected Revenue Growth Rate</div>', unsafe_allow_html=True)
    growth_years = list(HIST["Year"]) + [r["Year"] for r in fc_rows]
    growth_vals  = [None] + [
        round((HIST["Revenue"].iloc[i] / HIST["Revenue"].iloc[i-1] - 1) * 100, 1)
        for i in range(1, len(HIST))
    ] + [fc_cagr] * 5
    g_fig = go.Figure()
    g_fig.add_trace(go.Scatter(
        x=growth_years, y=growth_vals, mode="lines+markers",
        line=dict(color=ORANGE, width=2.5),
        marker=dict(size=8, color=[NAVY if i < 5 else ORANGE for i in range(len(growth_years))]),
        name="Revenue Growth %"
    ))
    g_fig.add_hline(y=fc_cagr, line_dash="dot", line_color=TEAL,
                    annotation_text=f"Projected: {fc_cagr:.0f}% CAGR",
                    annotation_font_color=TEAL)
    g_fig.update_layout(height=280, **_L,
                         yaxis=dict(ticksuffix="%", gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                         xaxis=dict(tickfont=dict(color="#374151")))
    st.plotly_chart(g_fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — COMPETITION
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "⚔️   Competition":
    st.markdown('<div class="narrative">Palantir competes differently in each market. In the U.S. government, it competes with Booz Allen Hamilton and SAIC — systems integrators, not software companies. In commercial AI, it competes with Snowflake, Databricks, and Microsoft. No single competitor occupies the same strategic position.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Peer Financial Comparison</div>', unsafe_allow_html=True)
    st.dataframe(PEERS, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Competitive Positioning Radar</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1: st.plotly_chart(radar_chart(), use_container_width=True)
    with c2:
        st.markdown(f"""
        <div class="q-card-navy" style="margin-top:0.5rem;">
          <b style="color:{NAVY};">Reading the Radar</b><br>
          <span style="font-size:0.83rem;color:#1e3a5f;">
            Palantir scores highest on <b>AI Moat</b> (ontology + classified data)
            and <b>Government Revenue</b> (unmatched), but trails peers on
            <b>Valuation Attractiveness</b> (inverse P/E). Snowflake and Datadog
            have comparable growth profiles but lack the government platform.
            C3.ai occupies the same government AI space at smaller scale.
            None replicate PLTR's Five Eyes infrastructure position.
          </span>
        </div>
        <div class="q-card-orange" style="margin-top:0.5rem;">
          <b style="color:{ORANGE};">The Core Competitive Moat</b><br>
          <span style="font-size:0.83rem;color:#7A2800;">
            <b>1. Ontology:</b> PLTR's Ontology SDK creates a shared data model across 
            enterprise and government — competitors cannot easily replicate this without 
            re-implementing entire data architecture.<br>
            <b>2. Classification clearances:</b> IL4/IL5/IL6 network access is a 2–4 year 
            process — not replicable by a VC-backed startup.<br>
            <b>3. Trust:</b> Palantir has operated in SIGINT environments since 2004 — 
            20 years of security-cleared trust cannot be marketed into existence.
          </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Competitive Threat Matrix — Government vs Commercial</div>', unsafe_allow_html=True)
    comp = pd.DataFrame([
        {"Competitor":"Booz Allen Hamilton","Segment":"U.S. Government","Threat Level":"Medium","PLTR Advantage":"Software platform vs. labour model — PLTR scales; BAH does not","Risk":"BAH integrating AI tools could become channel conflict"},
        {"Competitor":"Microsoft (Azure OpenAI)","Segment":"Commercial Enterprise","Threat Level":"High","PLTR Advantage":"Ontology + enterprise workflow depth; AIP is production-ready","Risk":"Azure AI Foundry + M365 Copilot replacing lightweight use cases"},
        {"Competitor":"Snowflake","Segment":"Commercial Enterprise","Threat Level":"Medium","PLTR Advantage":"AIP full workflow vs. Snowflake data warehouse; PLTR owns the decision layer","Risk":"Snowflake AI Data Cloud + Cortex encroaching on analytics layer"},
        {"Competitor":"C3.ai","Segment":"Government + Enterprise","Threat Level":"Low-Medium","PLTR Advantage":"Revenue scale (PLTR 10× C3.ai), government depth, product maturity","Risk":"C3.ai cheaper for sector-specific AI (utilities, energy)"},
        {"Competitor":"Databricks","Segment":"Commercial Data/AI","Threat Level":"Medium","PLTR Advantage":"User-facing AI applications vs. Databricks developer-facing infrastructure","Risk":"Databricks Unity Catalog + Genie moving up the stack toward PLTR's layer"},
        {"Competitor":"Leidos / SAIC","Segment":"U.S. Government","Threat Level":"Low-Medium","PLTR Advantage":"Mission software platform vs. hardware integration; PLTR higher margin","Risk":"Large IDIQ vehicles give primes preferred vendor status for DoD IT"},
    ])
    st.dataframe(comp, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Market Share Trajectory — U.S. Enterprise AI Platform</div>', unsafe_allow_html=True)
    ms_fig = go.Figure()
    years_ms = ["FY22","FY23","FY24","FY25E","FY26E","FY27E"]
    ms_fig.add_trace(go.Scatter(x=years_ms, y=[0.8, 1.2, 2.0, 2.8, 3.5, 4.5],
                                name="Palantir", line=dict(color=ORANGE, width=2.5),
                                mode="lines+markers", marker=dict(size=7)))
    ms_fig.add_trace(go.Scatter(x=years_ms, y=[1.5, 2.2, 3.5, 5.0, 7.0, 9.0],
                                name="Microsoft Azure AI", line=dict(color=NAVY, width=2.5),
                                mode="lines+markers", marker=dict(size=7)))
    ms_fig.add_trace(go.Scatter(x=years_ms, y=[1.2, 2.0, 3.0, 4.2, 5.5, 7.0],
                                name="Snowflake+Databricks", line=dict(color=TEAL, width=2),
                                mode="lines+markers", marker=dict(size=6, symbol="square")))
    ms_fig.update_layout(height=300, **_L,
                          title=dict(text="Estimated U.S. Enterprise AI Platform Market Share (%)",
                                     font=dict(color="#1A1A2E", size=13)),
                          yaxis=dict(ticksuffix="%", gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                          xaxis=dict(tickfont=dict(color="#374151")))
    st.plotly_chart(ms_fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 6 — LIFE CYCLE
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🔄  Life Cycle":
    st.markdown('<div class="narrative">Palantir sits at a rare inflection point: a company transitioning from early-growth (2003–2020, government-funded loss-making) through profitability (2023) into accelerated growth maturity. The AIP launch in 2023 essentially reset the product lifecycle clock for the commercial segment — making Palantir simultaneously a maturing government platform and a nascent commercial AI hyper-grower.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Corporate Life Cycle Stage Assessment (Damodaran Framework)</div>', unsafe_allow_html=True)
    lc_fig = go.Figure()
    stages = ["Startup", "Early Growth", "High Growth", "Mature Growth", "Maturity", "Decline"]
    x_pos  = [1, 2, 3, 4, 5, 6]
    rev_curve = [0.1, 0.5, 2.0, 3.5, 4.2, 3.8]
    lc_fig.add_trace(go.Scatter(x=x_pos, y=rev_curve, mode="lines", fill="tozeroy",
                                line=dict(color=NAVY, width=2), fillcolor=f"rgba(11,31,58,0.10)",
                                name="Revenue Curve (stylized)"))
    lc_fig.add_vline(x=3.2, line_dash="dash", line_color=ORANGE, line_width=2.5,
                     annotation_text="← PLTR Today (Govt: Mature Growth | Commercial: High Growth) →",
                     annotation_font=dict(color=ORANGE, size=11),
                     annotation_position="top")
    lc_fig.update_layout(height=250, **_L,
                          xaxis=dict(tickvals=x_pos, ticktext=stages, tickfont=dict(color="#374151")),
                          yaxis=dict(visible=False), showlegend=False)
    st.plotly_chart(lc_fig, use_container_width=True)

    st.markdown('<div class="sec-head">Life Cycle Position by Business Segment</div>', unsafe_allow_html=True)
    lc_segs = pd.DataFrame([
        {"Segment":"U.S. Government","Life Cycle Stage":"Mature Growth","Revenue CAGR":"12–18%","EBIT Margin":"30–35%","Capital Need":"Low","Strategic Priority":"Defend & expand; upsell AIP to existing classified contracts","Damodaran Signal":"High FCF generation; limited reinvestment need"},
        {"Segment":"U.S. Commercial","Life Cycle Stage":"High Growth","Revenue CAGR":"40–55%","EBIT Margin":"15–25%","Capital Need":"Medium","Strategic Priority":"Maximum customer acquisition; AIP Boot Camps at scale; land and expand","Damodaran Signal":"Reinvest aggressively; accept lower near-term margins for market share"},
        {"Segment":"International Government","Life Cycle Stage":"Early-Mature Growth","Revenue CAGR":"8–15%","EBIT Margin":"18–22%","Capital Need":"Medium","Strategic Priority":"NATO AI expansion; strengthen Five Eyes pipeline; EU compliance navigation","Damodaran Signal":"Selective reinvestment; prioritize high-margin NATO allies"},
        {"Segment":"International Commercial","Life Cycle Stage":"Early Growth","Revenue CAGR":"20–30%","EBIT Margin":"10–18%","Capital Need":"High","Strategic Priority":"Replicate U.S. Boot Camp model in EMEA & APAC; local partnerships","Damodaran Signal":"Accept losses for market entry; TAM is $50B+ if AIP globalizes"},
    ])
    st.dataframe(lc_segs, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">FCF and EBIT Margin Trajectory — Damodaran Growth→Maturity Transition</div>', unsafe_allow_html=True)
    lc_years = ["FY21","FY22","FY23","FY24","FY25E","FY26E","FY27E","FY28E","FY30E"]
    margins  = [-33.4,-15.2, 6.8, 12.5, 19.5, 24.0, 28.0, 31.0, 35.0]
    fcffs_lc = [-119,  261,  730, 1154, 1630, 2280, 3100, 4100, 6800]
    lc_m_fig = make_subplots(specs=[[{"secondary_y": True}]])
    lc_m_fig.add_trace(go.Bar(x=lc_years, y=fcffs_lc, name="FCFF ($M)", marker_color=NAVY, opacity=0.75), secondary_y=False)
    lc_m_fig.add_trace(go.Scatter(x=lc_years, y=margins, name="EBIT Margin (%)",
                                   line=dict(color=ORANGE, width=2.5),
                                   mode="lines+markers", marker=dict(size=7, color=ORANGE)), secondary_y=True)
    lc_m_fig.add_hline(y=0, line_color=RED, line_width=1.5, secondary_y=True)
    lc_m_fig.update_layout(height=320, **_L,
                             yaxis=dict(tickprefix="$", ticksuffix="M", gridcolor="#F0F0F0", tickfont=dict(color="#374151")),
                             yaxis2=dict(ticksuffix="%", gridcolor="#F0F0F0", tickfont=dict(color="#374151")))
    lc_m_fig.update_xaxes(tickfont=dict(color="#374151"))
    st.plotly_chart(lc_m_fig, use_container_width=True)

    st.markdown(f"""
    <div class="pullquote">
      The rarest company in technology is one that simultaneously operates a cash-generating government 
      platform with 20+ year relationships and launches a hyper-growth commercial AI product.
      Palantir's life cycle is bifurcated by design — and that is its most powerful structural advantage.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Reinvestment Strategy vs Life Cycle Stage (Damodaran Prescription)</div>', unsafe_allow_html=True)
    reinvest = pd.DataFrame([
        {"Stage":"U.S. Government (Mature)","Damodaran Prescription":"Return excess cash; moderate reinvestment","PLTR Actual":"Reinvesting at 8–12% incremental rate via AIP upsell; appropriate","Assessment":"✅ Aligned"},
        {"Stage":"U.S. Commercial (High Growth)","Damodaran Prescription":"Reinvest aggressively; accept low short-term ROE","PLTR Actual":"Boot Camps, sales hiring, platform R&D — correct capital allocation","Assessment":"✅ Aligned"},
        {"Stage":"SBC as % Revenue (10%)","Damodaran Prescription":"Growth cos may justify SBC, but dilution should decelerate as margins rise","PLTR Actual":"SBC still ~10% revenue — needs to decline toward 5–6% by FY2027","Assessment":"⚠️ Watch"},
        {"Stage":"Capital Return (No Dividend)","Damodaran Prescription":"High-growth cos should not pay dividends; buybacks optional","PLTR Actual":"No dividend; opportunistic buybacks — textbook Damodaran high-growth","Assessment":"✅ Aligned"},
        {"Stage":"Debt Policy (Debt-Free)","Damodaran Prescription":"Pre-profitability growth cos should avoid debt; Palantir is now profitable","PLTR Actual":"Zero debt with $5.2B net cash — could lever modestly for accretive M&A","Assessment":"✅ Conservative"},
    ])
    st.dataframe(reinvest, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 7 — MARKETING STRATEGY
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🎯  Marketing Strategy":
    st.markdown('<div class="narrative">Palantir\'s marketing strategy is unlike any enterprise software company. Its primary commercial acquisition channel is not a Salesforce CRM funnel — it is the AIP Boot Camp, a product-led sales motion that converts prospective clients into paying customers in 3–5 days. This section applies the full marketing strategy framework to decode PLTR\'s approach and prescribe enhancements.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Market Segmentation — B2B Target Profile</div>', unsafe_allow_html=True)
    segs_mkt = pd.DataFrame([
        {"Segment":"U.S. Defense & Intelligence","Profile":"DoD prime contractors, classified intelligence agencies, special operations forces","Buying Trigger":"Mission capability gap; NDAA AI mandate; battlefield decision latency","ACV ($M)":"$10–100M+","Retention":"Very High (10+ year contracts)"},
        {"Segment":"U.S. Federal Civilian","Profile":"HHS, DHS, VA, Treasury — large data-intensive agencies","Buying Trigger":"Digital transformation mandates; fraud detection; citizen services AI","ACV ($M)":"$5–25M","Retention":"High (multi-year IDIQ)"},
        {"Segment":"U.S. Large Enterprise","Profile":"Fortune 500 in healthcare, finance, insurance, manufacturing, energy","Buying Trigger":"AI competitive pressure; operational efficiency; regulatory compliance","ACV ($M)":"$1–10M","Retention":"Growing (AIP lock-in deepens)"},
        {"Segment":"Allied Government (Five Eyes)","Profile":"UK MOD, GCHQ, Australian DSD, Canadian CSE, New Zealand GCSB","Buying Trigger":"Interoperability with U.S. systems; sovereign AI capability","ACV ($M)":"$5–50M","Retention":"Very High"},
        {"Segment":"International Commercial","Profile":"EMEA/APAC enterprises in pharma, aerospace, utilities, financial services","Buying Trigger":"Digital transformation; ESG data compliance; supply chain resilience","ACV ($M)":"$0.5–5M","Retention":"Medium (early-stage)"},
    ])
    st.dataframe(segs_mkt, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Positioning Strategy — STP Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="ansoff-card">
          <div class="ansoff-title">🎯 Target Segment Priority</div>
          <div class="ansoff-sub">Where PLTR should concentrate resources (FY2026–FY2028)</div>
          <div class="ansoff-item">🥇 <b>U.S. Commercial (Large Enterprise)</b> — 40%+ growth; highest ROI on Boot Camps; strategic re-rating catalyst</div>
          <div class="ansoff-item">🥈 <b>U.S. Government</b> — anchor revenue; defend and upsell AIP to classified installed base</div>
          <div class="ansoff-item">🥉 <b>Allied Government (Five Eyes + NATO)</b> — NATO AI acceleration creates $5B+ incremental TAM</div>
          <div class="ansoff-item">📈 <b>International Commercial</b> — long-term option value; invest selectively via regional partners</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="ansoff-card">
          <div class="ansoff-title">📣 Positioning Statement</div>
          <div class="ansoff-sub">How PLTR should position AIP to the C-suite</div>
          <div class="ansoff-item"><i>"For enterprises and governments that cannot afford to make the wrong decision, 
          Palantir AIP is the only AI platform that operates on your most sensitive data, 
          in your most critical workflows, to give your operators — not your AI — 
          the decisive advantage."</i></div>
          <div class="ansoff-item" style="margin-top:8px;">
            <b>POD vs Competitors:</b><br>
            vs. Microsoft: Palantir owns the decision layer, not just the infrastructure.<br>
            vs. Snowflake: AIP is operational AI (act on data), not analytical AI (understand data).<br>
            vs. C3.ai: Palantir has 20 years of classified deployment trust.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Ansoff Growth Matrix — FY2026–FY2028 Strategy</div>', unsafe_allow_html=True)
    ansoff_data = [
        ("Market Penetration (Primary)", "Existing Products × Existing Markets",
         "Deepen AIP deployment in current U.S. Government and Commercial accounts. Upsell AIP modules to the 700+ existing customer base. Target is to grow revenue per customer by 25–35% annually through expanded platform adoption.",
         f'<span class="tag-orange">Primary Strategy</span>'),
        ("Product Development (Secondary)", "New Products × Existing Markets",
         "AIP for Healthcare (FDA submissions + clinical trial AI). AIP for Finance (risk management + fraud detection). AIP for Supply Chain (real-time operational intelligence). These are new product verticals for existing enterprise relationships.",
         f'<span class="tag-navy">Secondary Strategy</span>'),
        ("Market Development (Secondary)", "Existing Products × New Markets",
         "APAC commercial expansion (Japan, Australia, Singapore). NATO Tier-2 allied governments (Poland, Germany, Netherlands). Mid-market U.S. commercial (companies with $500M–$5B revenue) via AIP Express.",
         f'<span class="tag-teal">Secondary Strategy</span>'),
        ("Diversification (Selective)", "New Products × New Markets",
         "AIP for Infrastructure Resilience (utility grids, water systems). Space systems AI (government dual-use). Quantum-ready data platform (FY2028+ horizon). High-risk, high-reward — pursue with venture discipline.",
         f'<span class="tag-gold">Long-Term Horizon</span>'),
    ]
    for title, subtitle, content, badge in ansoff_data:
        st.markdown(f"""
        <div class="ansoff-card">
          <div class="ansoff-title">{title} &nbsp; {badge}</div>
          <div class="ansoff-sub">{subtitle}</div>
          <div class="ansoff-item">{content}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">4Ps Operational Audit — What Needs Fixing Now</div>', unsafe_allow_html=True)
    fourp = pd.DataFrame([
        {"Lever":"Product","The Gap Today":"AIP is powerful but perceived as complex; onboarding beyond Boot Camp needs acceleration; no self-serve tier for mid-market","Required Action (FY26–28)":"AIP Express (self-serve for <$5B revenue companies); modular vertical-specific templates; open-source community SDK to build developer ecosystem","Financial Impact":"Mid-market TAM adds $15B+ addressable revenue by FY2029"},
        {"Lever":"Price","The Gap Today":"Pricing opaque to prospects; enterprise contracts lengthy; no transparent per-seat or usage model for commercial","Required Action (FY26–28)":"Introduce tiered AIP pricing: Starter / Professional / Enterprise / Classified. Consumption-based model for high-growth commercial accounts.","Financial Impact":"Reduces sales cycle from 6 months to <60 days; 2× conversion rate"},
        {"Lever":"Place (Channel)","The Gap Today":"100% direct sales; no GSI/VAR channel; no marketplace presence (AWS/Azure Marketplace)","Required Action (FY26–28)":"List AIP on AWS Marketplace, Azure Marketplace. Partner with Accenture, Deloitte, EY as implementation SIs. Create PLTR-certified partner program.","Financial Impact":"Channel partners could contribute 20–30% of commercial revenue by FY2028"},
        {"Lever":"Promotion","The Gap Today":"Alex Karp's polarizing communication style creates brand noise; developer awareness below Snowflake/Databricks level; no developer community","Required Action (FY26–28)":"Palantir Developer Network (PDN); AIP hackathons at major universities; LinkedIn/YouTube technical content marketing; PLTR-sponsored AI policy research.","Financial Impact":"Developer ecosystem = 5–10 year competitive moat; reduces CAC by 30–40%"},
    ])
    st.dataframe(fourp, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Capital Allocation Prescription — FY2026–FY2028</div>', unsafe_allow_html=True)
    st.markdown('<div class="narrative">Palantir\'s most important capital allocation decision in the next three years is not a product launch — it is the channel buildout and developer ecosystem investment. The $5.2B net cash hoard is an opportunity: deploy it into the commercial growth engine before Microsoft and Snowflake own the enterprise AI mindshare.</div>', unsafe_allow_html=True)
    cap = pd.DataFrame([
        {"Use of Capital":"Share Buybacks",              "FY25 Actual":"~$200M est.","Recommended FY26–28":"$300–500M/yr","Rationale":"Offset SBC dilution; signal confidence without over-returning"},
        {"Use of Capital":"Dividends",                   "FY25 Actual":"$0",         "Recommended FY26–28":"$0 (maintain)","Rationale":"Growth company — no dividend appropriate; reinvest all excess FCF"},
        {"Use of Capital":"R&D (AIP + Ontology + 6G AI)","FY25 Actual":"~$700M est.","Recommended FY26–28":"$900–1,200M/yr","Rationale":"Maintain ontology moat; build next-gen AIP for agentic AI era"},
        {"Use of Capital":"Commercial Sales & Boot Camps","FY25 Actual":"~$300M est.","Recommended FY26–28":"$500–700M/yr","Rationale":"Boot Camp is the highest ROI sales motion ever invented — fund it aggressively"},
        {"Use of Capital":"Developer Ecosystem & Mktg",  "FY25 Actual":"<$100M est.","Recommended FY26–28":"$200–350M/yr","Rationale":"PDN + marketplace presence + technical content = 10-year moat"},
        {"Use of Capital":"Strategic M&A",               "FY25 Actual":"Minimal",    "Recommended FY26–28":"$500M–1.5B (selective)","Rationale":"Acquire vertical AI leaders (healthcare, energy) rather than build from scratch"},
    ])
    st.dataframe(cap, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="pullquote">
      The AI platform company that wins the next decade will be defined not by the demo it ran 
      in the Boot Camp, but by the ecosystem it built around the platform. 
      Palantir has the ontology, the government trust, and the commercial momentum. 
      The only missing piece is the developer community. 
      Build it before Microsoft builds it around you.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Strategy Coherence Audit — 6-Point Consistency Check</div>', unsafe_allow_html=True)
    audit = pd.DataFrame([
        {"Dimension":"Growth Direction (Ansoff)","Strategy":"Market Penetration (1°) + Product Dev (2°)","LC Consistent?":"✅ Yes","Financial Consistent?":"✅ Yes — FCF $1.6B+ funds both","Conflict?":"None"},
        {"Dimension":"Competitive Positioning","Strategy":"Differentiation — Ontology + classified integration","LC Consistent?":"✅ Yes","Financial Consistent?":"✅ Yes — Gross margin 80%+ confirms premium capture","Conflict?":"None"},
        {"Dimension":"Pricing Strategy","Strategy":"Value-based enterprise contracts; Boot Camp-to-AIP conversion","LC Consistent?":"⚠️ Partial","Financial Consistent?":"⚠️ Opaque pricing slows mid-market","Conflict?":"No transparent pricing limits mid-market scale"},
        {"Dimension":"Channel Strategy","Strategy":"100% direct; Boot Camp as primary motion","LC Consistent?":"⚠️ Partial","Financial Consistent?":"⚠️ Limits TAM without SI/marketplace channel","Conflict?":"No GSI channel limits FY2027 commercial scale"},
        {"Dimension":"Promotion / Communication","Strategy":"Thought leadership (Karp) + AIP technical demos","LC Consistent?":"⚠️ Partial","Financial Consistent?":"✅ Yes — SGA 30% revenue absorbs","Conflict?":"Polarizing CEO communication creates brand risk"},
        {"Dimension":"Capital Allocation","Strategy":"Zero dividend + SBC-heavy + selective buyback","LC Consistent?":"✅ Yes","Financial Consistent?":"⚠️ SBC dilution (10% of rev) too high","Conflict?":"SBC must decline as margins expand — currently out of pace"},
    ])
    st.dataframe(audit, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 9 — AIP DEEP DIVE
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "🧠  AIP Deep Dive":
    st.markdown('<div class="narrative">Palantir\'s Artificial Intelligence Platform (AIP) is not merely a product — it is a paradigm shift in how enterprise AI gets deployed from prototype to production. Understanding AIP\'s architecture, deployment model, and economic logic is essential to understanding why Palantir\'s commercial growth is accelerating in ways that even the bulls underestimated.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">AIP Architecture — The Four Layers</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        layers = [
            ("Layer 1: Ontology", "TEAL", f"""
            The semantic data model. Palantir's Ontology SDK creates a unified, live object model
            across all enterprise data sources — ERP, CRM, IoT, operational databases.
            Unlike static data warehouses, the Ontology is <b>action-ready</b>: objects can trigger
            workflows, not just surface insights. This is the foundational moat.
            <br><br><b>Why it matters:</b> Once an enterprise maps its entire operational data landscape
            into the Ontology, the switching cost approaches near-infinity. Rebuilding the Ontology
            from scratch takes 2–3 years. Microsoft and Snowflake can replicate the data layer; they
            cannot replicate the semantic layer at the same depth.
            """, "q-card-teal"),
            ("Layer 2: Foundry (Data Infrastructure)", "NAVY", f"""
            The operational data platform. Ingests, transforms, and pipelines data from hundreds
            of enterprise sources into clean, versioned, audit-ready datasets. FedRAMP High and
            IL4/IL5/IL6 certified — the only commercial AI platform that can operate in classified
            U.S. government environments. Foundry underpins the government revenue base.
            <br><br><b>Commercial significance:</b> Foundry is the Trojan horse. Once a Fortune 500
            migrates its data pipelines to Foundry, deploying AIP applications on top requires
            minimal incremental friction — dramatically compressing the AIP sales cycle.
            """, "q-card-navy"),
        ]
        for title, color, content, cls in layers:
            st.markdown(f'<div class="{cls}"><b style="color:{TEAL if color=="TEAL" else NAVY};">{title}</b><br><span style="font-size:0.83rem;color:#1e3a5f;">{content}</span></div>', unsafe_allow_html=True)
    with c2:
        layers2 = [
            ("Layer 3: AIP (LLM Orchestration)", "ORANGE", f"""
            The intelligence layer. AIP sits on top of Foundry + Ontology and enables enterprises
            to deploy Large Language Models (LLMs) — including GPT-4, Llama 3, Claude, and
            proprietary fine-tuned models — <b>against their live operational data</b>.
            <br><br>Key AIP capabilities: (1) AIP Logic — drag-and-drop LLM workflow builder for
            non-engineers; (2) AIP Assist — AI copilot layer on Foundry workflows; (3) AIP
            Agents — fully autonomous multi-step decision agents operating inside enterprise
            guardrails. The agentic AI era is Palantir's biggest TAM expansion opportunity:
            autonomous AI agents making procurement, logistics, and medical decisions on live data.
            """, "q-card-orange"),
            ("Layer 4: Apollo (Deployment Engine)", "GREEN", f"""
            The continuous delivery platform. Apollo manages the deployment, configuration, and
            monitoring of Palantir software across classified cloud, commercial cloud, and
            air-gapped on-premises environments. Apollo is invisible to the market narrative
            but it is the operational backbone that allows Palantir to maintain 100+ simultaneous
            government deployments without exponential engineering headcount.
            <br><br><b>Financial significance:</b> Apollo is why Palantir's gross margins can
            expand toward 85–90% at scale. Software deployments that would require armies of
            implementation engineers at competitors are fully automated via Apollo.
            """, "q-card-green"),
        ]
        for title, color, content, cls in layers2:
            col_map = {"ORANGE": ORANGE, "GREEN": GREEN}
            st.markdown(f'<div class="{cls}"><b style="color:{col_map.get(color,NAVY)};">{title}</b><br><span style="font-size:0.83rem;color:#1e3a5f;">{content}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">AIP Boot Camp Economics — The Sales Revolution</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="q-card-orange">
      <b style="color:{ORANGE};">Why Boot Camps Are the Most Important Sales Innovation in Enterprise Software</b><br>
      <span style="font-size:0.86rem;color:#7A1A0A;line-height:1.7;">
        Traditional enterprise SaaS sales: 6–18 month PoC cycle → RFP → procurement → integration → go-live.
        Total cost to acquire: $500K–$2M per deal. Palantir Boot Camp model: <b>3–5 day intensive workshop</b>,
        client brings their own data, PLTR engineers build working prototypes live. Conversion rate: 30–40%.
        Time-to-production: weeks, not years.<br><br>
        The Boot Camp is not a marketing event. It is a <b>paid engagement</b> (clients pay to attend),
        it trains the client's team on PLTR's platform (creating internal advocates), and it demonstrates
        production-grade AI on real enterprise data — which no competitor can replicate in a PowerPoint deck.
        In FY2024, PLTR ran hundreds of Boot Camps globally. Each Boot Camp costs PLTR ~$50–150K to run
        and generates an expected contract value of $1–5M. CAC efficiency is extraordinary.
      </span>
    </div>
    """, unsafe_allow_html=True)

    boot_metrics = pd.DataFrame([
        {"Metric": "Average Boot Camp Duration", "Value": "3–5 days", "Notes": "Client brings real data; PLTR engineers co-build"},
        {"Metric": "Boot Camp Conversion Rate", "Value": "~30–40%", "Notes": "Boot Camp attendee → paid AIP contract"},
        {"Metric": "Average Contract Value (post-Boot Camp)", "Value": "$1–5M ARR", "Notes": "Scales to $10M+ for large enterprises"},
        {"Metric": "Time to Production", "Value": "Weeks (not years)", "Notes": "vs 12–18 months for traditional enterprise SaaS"},
        {"Metric": "Boot Camps Run (FY2024E)", "Value": "500+", "Notes": "Global; U.S. Commercial is primary market"},
        {"Metric": "U.S. Commercial Revenue Growth (FY2024)", "Value": "+52% YoY", "Notes": "Direct result of Boot Camp acceleration"},
        {"Metric": "Customer Count (FY2024)", "Value": "700+", "Notes": "AIP-driven; targeting 1,000+ by FY2025"},
        {"Metric": "Net Dollar Retention", "Value": ">115%", "Notes": "Expanding use cases post-initial contract"},
    ])
    st.dataframe(boot_metrics, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">AIP Competitive Moat — Why This Cannot Be Easily Replicated</div>', unsafe_allow_html=True)
    moat_data = pd.DataFrame([
        {"Moat Component": "Ontology Depth", "Replication Timeline": "3–5 years", "Why Hard": "Requires re-mapping entire enterprise data landscape; not a product, a process"},
        {"Moat Component": "Classified Accreditations (IL4/IL5/IL6)", "Replication Timeline": "4–7 years", "Why Hard": "Government security certifications require years of audits, cleared personnel, and trust"},
        {"Moat Component": "Five Eyes Integration", "Replication Timeline": "Not replicable commercially", "Why Hard": "Embedded in SIGINT infrastructure since 2004; structural government trust"},
        {"Moat Component": "AIP Boot Camp Methodology", "Replication Timeline": "1–2 years (process)", "Why Hard": "Easy to copy the format; hard to replicate 2,000+ trained PLTR engineers"},
        {"Moat Component": "Apollo Deployment Automation", "Replication Timeline": "2–4 years", "Why Hard": "Multi-cloud, classified + commercial air-gap management is deeply complex engineering"},
        {"Moat Component": "Customer Ontology Lock-In", "Replication Timeline": "N/A — customer-specific", "Why Hard": "Each client's Ontology is unique; migrating = rebuilding entire operational intelligence layer"},
    ])
    st.dataframe(moat_data, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">AIP Agentic AI — The Next Revenue Wave (FY2026–FY2030)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="q-card-purple">
      <b style="color:{PURPLE};">Why Agentic AI Is Palantir's Biggest Unanswered Opportunity</b><br>
      <span style="font-size:0.85rem;color:#4a0e6a;line-height:1.7;">
        The current AIP use case is primarily <b>assistive</b>: AI helps a human analyst, logistics manager,
        or intelligence officer make a faster, better decision. The next phase — <b>agentic AI</b> —
        removes the human from the decision loop entirely for defined operational workflows.<br><br>
        Examples: (1) Autonomous procurement agents that renegotiate supplier contracts when commodity
        prices move; (2) Autonomous battlefield logistics agents that reroute supply chains in real-time
        during combat operations; (3) Autonomous clinical trial agents that adjust patient protocols
        based on emerging biomarker data.<br><br>
        Palantir's Ontology + Apollo + AIP Agent framework is architecturally the most production-ready
        agentic AI platform for enterprise and government. If agentic AI scales to 10–20% of
        Fortune 500 operational workflows by FY2030, Palantir's TAM expands from $50B to $500B+.
        This is the scenario the market is beginning to price in — and the scenario that justifies
        a 150–200× forward P/E multiple.
      </span>
    </div>
    """, unsafe_allow_html=True)
    
    agentic_tab = pd.DataFrame([
        {"Vertical": "Defence & Intelligence", "Agentic Use Case": "Autonomous target identification and battlefield decision support", "TAM FY30E ($B)": 45, "PLTR Readiness": "⭐⭐⭐⭐⭐ Production"},
        {"Vertical": "Healthcare & Life Sciences", "Agentic Use Case": "Autonomous clinical trial management; drug interaction screening", "TAM FY30E ($B)": 38, "PLTR Readiness": "⭐⭐⭐⭐ Early Production"},
        {"Vertical": "Financial Services", "Agentic Use Case": "Autonomous risk management; real-time fraud detection at network level", "TAM FY30E ($B)": 55, "PLTR Readiness": "⭐⭐⭐ Pilot"},
        {"Vertical": "Energy & Utilities", "Agentic Use Case": "Autonomous grid balancing; predictive infrastructure maintenance", "TAM FY30E ($B)": 30, "PLTR Readiness": "⭐⭐⭐ Pilot"},
        {"Vertical": "Supply Chain & Logistics", "Agentic Use Case": "Autonomous end-to-end supply chain orchestration", "TAM FY30E ($B)": 42, "PLTR Readiness": "⭐⭐⭐⭐ Early Production"},
        {"Vertical": "Government / Civil Services", "Agentic Use Case": "Autonomous benefits administration; fraud detection in social programs", "TAM FY30E ($B)": 28, "PLTR Readiness": "⭐⭐⭐⭐ Early Production"},
    ])
    st.dataframe(agentic_tab, use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 10 — RISK MATRIX
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "⚠️  Risk Matrix":
    st.markdown('<div class="narrative">No investment thesis is complete without a rigorous, honest accounting of the risks. Palantir\'s premium valuation is both a reward for its exceptional platform and a vulnerability — any meaningful miss against inflated expectations carries violent downside. This section maps all material risks across probability, impact, and mitigant dimensions.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Comprehensive Risk Register — 15 Material Risks</div>', unsafe_allow_html=True)
    risks_full = pd.DataFrame([
        {"#": 1, "Risk": "Government Budget Sequestration", "Category": "Political", "Probability": "Medium (30%)", "Impact": "High", "Financial Exposure": "$300–500M revenue at risk", "Mitigant": "Commercial diversification; AIP offset; multi-year contracts"},
        {"#": 2, "Risk": "Microsoft Azure AI encroachment", "Category": "Competitive", "Probability": "High (55%)", "Impact": "Medium", "Financial Exposure": "$150–300M commercial pipeline risk", "Mitigant": "Ontology depth + classified positioning not replicable by MSFT"},
        {"#": 3, "Risk": "Valuation multiple compression", "Category": "Market", "Probability": "High (60%)", "Impact": "High", "Financial Exposure": "30–50% stock price decline on deceleration", "Mitigant": "Accelerating FCF growth; buyback program reduces float"},
        {"#": 4, "Risk": "Stock-Based Compensation dilution", "Category": "Financial", "Probability": "High (70%)", "Impact": "Medium", "Financial Exposure": "~2% annual EPS dilution; $300M+ annual SBC", "Mitigant": "Buyback program; FCF growth outpacing dilution by FY2026E"},
        {"#": 5, "Risk": "Open-source LLM commoditisation", "Category": "Technological", "Probability": "Medium (40%)", "Impact": "Low-Medium", "Financial Exposure": "Reduces LLM component value; not Ontology/Apollo", "Mitigant": "Moat is the Ontology + deployment infra, not the LLM itself"},
        {"#": 6, "Risk": "EU AI Act compliance friction", "Category": "Regulatory", "Probability": "Medium (45%)", "Impact": "Low-Medium", "Financial Exposure": "$50–100M international revenue friction", "Mitigant": "On-prem + private cloud deployment model already EU-compliant"},
        {"#": 7, "Risk": "AIP Boot Camp conversion rate decline", "Category": "Operational", "Probability": "Medium (35%)", "Impact": "High", "Financial Exposure": "U.S. commercial growth decelerates below 30%", "Mitigant": "Increasing PLTR engineer headcount; expanding vertical coverage"},
        {"#": 8, "Risk": "Key person risk (Alex Karp)", "Category": "Governance", "Probability": "Low (15%)", "Impact": "Medium", "Financial Exposure": "Brand/culture disruption; institutional relationship risk", "Mitigant": "Deep management bench; Karp contract runs through 2027"},
        {"#": 9, "Risk": "NATO allied government budget constraints", "Category": "Geopolitical", "Probability": "Low-Medium (25%)", "Impact": "Low-Medium", "Financial Exposure": "$100–200M international gov revenue risk", "Mitigant": "Offsetting demand in UK, Poland, Germany; Ukraine war tailwind"},
        {"#": 10, "Risk": "Cybersecurity breach / classified data incident", "Category": "Operational", "Probability": "Very Low (5%)", "Impact": "Very High", "Financial Exposure": "Existential reputational and contract risk", "Mitigant": "Zero-trust architecture; highest security certifications; no cloud data storage policy"},
        {"#": 11, "Risk": "Customer concentration (top 20 clients)", "Category": "Revenue", "Probability": "Medium (40%)", "Impact": "Medium", "Financial Exposure": "Top 20 clients = ~45% of revenue; churn = material miss", "Mitigant": "Rapid commercial customer diversification; 700+ clients FY2024"},
        {"#": 12, "Risk": "DOGE / U.S. federal budget cuts", "Category": "Political", "Probability": "Medium (35%)", "Impact": "High", "Financial Exposure": "$200–400M DoD/civilian government revenue risk", "Mitigant": "PLTR is efficiency-enhancing software — potential DOGE beneficiary, not target"},
        {"#": 13, "Risk": "Commercial execution gap — international", "Category": "Strategic", "Probability": "Medium (45%)", "Impact": "Medium", "Financial Exposure": "International commercial revenue stagnates at 15–20% margin", "Mitigant": "EMEA healthcare focus; Japan/Australia AIP expansion; SI partnership buildout"},
        {"#": 14, "Risk": "Class A / B / C share governance structure", "Category": "Governance", "Probability": "Low (20%)", "Impact": "Low", "Financial Exposure": "Founder control limits activist shareholder discipline on SBC", "Mitigant": "PLTR shifting toward GAAP profitability reduces SBC concern"},
        {"#": 15, "Risk": "Recession / macro AI spend pullback", "Category": "Macro", "Probability": "Medium (30%)", "Impact": "Medium-High", "Financial Exposure": "Enterprise AI capex freezes; boot camp pipeline slows 20–30%", "Mitigant": "Government revenue (50% of total) is counter-cyclical; FCF fortress"},
    ])
    st.dataframe(risks_full, use_container_width=True, hide_index=True)

    st.markdown('<div class="sec-head">Risk Heat Map — Probability vs. Impact</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        prob_map  = {"Very Low (5%)": 5, "Low (15%)": 15, "Low-Medium (25%)": 25,
                     "Medium (30%)": 30, "Medium (35%)": 35, "Medium (40%)": 40,
                     "Medium (45%)": 45, "High (55%)": 55, "High (60%)": 60, "High (70%)": 70}
        impact_map = {"Low": 1, "Low-Medium": 2, "Medium": 3, "Medium-High": 4, "High": 5, "Very High": 6}
        probs   = [prob_map.get(p, 30) for p in risks_full["Probability"]]
        impacts = [impact_map.get(i, 3) for i in risks_full["Impact"]]
        risk_colors = []
        for p, i in zip(probs, impacts):
            score = p * i / 100
            if score > 15: risk_colors.append(RED)
            elif score > 8: risk_colors.append(GOLD)
            else: risk_colors.append(GREEN)
        heat_fig = go.Figure()
        heat_fig.add_trace(go.Scatter(
            x=probs, y=impacts,
            mode="markers+text",
            marker=dict(size=20, color=risk_colors, opacity=0.85,
                        line=dict(width=2, color="white")),
            text=[str(r) for r in risks_full["#"]],
            textfont=dict(color="white", size=9, family="Inter"),
            textposition="middle center",
            hovertext=[f"#{r['#']}: {r['Risk']}<br>P: {r['Probability']} | I: {r['Impact']}"
                       for _, r in risks_full.iterrows()],
            hoverinfo="text",
        ))
        heat_fig.add_shape(type="rect", x0=40, y0=3.5, x1=75, y1=6.5,
                           fillcolor="rgba(193,18,31,0.08)", line=dict(color=RED, dash="dash", width=1))
        heat_fig.add_annotation(x=57, y=6.3, text="HIGH RISK ZONE", font=dict(color=RED, size=9), showarrow=False)
        heat_fig.update_layout(
            height=320, **_L,
            xaxis=dict(title="Probability (%)", range=[0, 80], tickfont=dict(color="#374151"),
                       gridcolor="#F0F0F0"),
            yaxis=dict(title="Impact (1=Low → 6=Existential)", range=[0.5, 6.5],
                       tickfont=dict(color="#374151"), gridcolor="#F0F0F0"),
            showlegend=False,
        )
        st.plotly_chart(heat_fig, use_container_width=True)
    with c2:
        high_risks = risks_full[risks_full["Impact"].isin(["High", "Very High", "Medium-High"])]
        st.markdown(f'<div class="sec-head" style="margin-top:0;">Top Risks by Impact</div>', unsafe_allow_html=True)
        for _, r in high_risks.iterrows():
            tag_col = "tag-red" if "High" in r["Impact"] else "tag-gold"
            st.markdown(f"""
            <div class="q-card" style="padding:0.6rem 0.8rem;margin-bottom:0.5rem;">
              <span class="{tag_col}">{r["Impact"]}</span>&nbsp;
              <b style="font-size:0.82rem;color:{NAVY};">#{r['#']} {r['Risk']}</b><br>
              <span style="font-size:0.72rem;color:#6B7280;">{r['Financial Exposure']}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Bear Case Stress Test — What Goes Wrong</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="q-card-red">
      <b style="color:{RED};">The Bear Case Narrative (Probability: ~25%)</b><br>
      <span style="font-size:0.86rem;color:#7A0A0A;line-height:1.75;">
        <b>Year 1 (FY2025):</b> U.S. Commercial growth decelerates to 28% as Boot Camp conversion
        drops post-wave 1 Fortune 500 saturation. Government revenue stagnates as DOGE-driven
        budget reviews freeze DoD IT spending. Stock falls 30–40% from peak as market re-rates
        from 170× to 80× forward P/E.<br><br>
        <b>Year 2 (FY2026):</b> Microsoft Azure AI + Copilot wins 3–5 major commercial contracts
        that PLTR had in pipeline. SBC remains at 10% of revenue. Net Income misses consensus
        by 15–20%. Institutional holders begin trimming positions. Stock tests $40–50 level.<br><br>
        <b>Year 3 (FY2027):</b> International commercial growth stagnates below 15% due to EU AI Act
        friction. PLTR stock re-rates to 50–60× forward P/E. Base case DCF intrinsic value:
        $35–45/share. This bear case is painful but does not impair the business — it is a
        valuation re-rating, not a fundamental collapse.
      </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">DOGE Exposure Analysis — Risk or Opportunity?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="q-card-orange">
          <b style="color:{ORANGE};">Why DOGE Could Actually Help Palantir</b><br>
          <span style="font-size:0.84rem;color:#7A1A0A;line-height:1.65;">
            The Department of Government Efficiency's mandate is to identify and eliminate
            government waste. Palantir's AIP platform does exactly this — it replaces teams of
            government analysts and eliminates redundant data workflows with automated AI systems.<br><br>
            Historical precedent: Palantir's Gotham platform was partially funded by cutting
            manual intelligence analysis teams at CIA and NSA. AIP could play the same role
            across civilian agencies (IRS, SSA, HHS).<br><br>
            <b>Contracts at risk:</b> Low — PLTR contracts are outcome-based and efficiency-driving<br>
            <b>New contract potential:</b> High — PLTR AIP is the efficiency tool DOGE needs
          </span>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="q-card-navy">
          <b style="color:{NAVY};">PLTR Government Revenue Exposure Breakdown (FY2025E)</b><br>
          <span style="font-size:0.84rem;color:#1e3a5f;line-height:1.65;">
            · DoD (Army, Air Force, Navy, SOCOM): ~$700M — <b>Low DOGE risk</b><br>
            · Intelligence Community (CIA, NSA, NGA): ~$280M — <b>Very Low risk</b><br>
            · Civilian agencies (IRS, HHS, DHS): ~$120M — <b>Medium risk but upside potential</b><br>
            · International Government: ~$1,014M — <b>No DOGE exposure</b><br><br>
            Net DOGE risk exposure: ~$100–150M (4–5% of FY2025E revenue). More than offset by
            potential DOGE-mandated efficiency AI contract wins.
          </span>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE 8 — LIVE NEWS
# ═════════════════════════════════════════════════════════════════════════════
elif PAGE == "📰  Live News":
    st.markdown('<div class="narrative">News flow is the heartbeat of market sentiment. For Palantir, headlines oscillate between government contract wins (structural positives) and valuation concerns (persistent noise). The analyst who ignores news is flying blind; the one who only watches it loses perspective on the platform\'s long-term trajectory.</div>', unsafe_allow_html=True)

    news = get_live_news()
    pos_n = sum(1 for n in news if n["sentiment"] == "positive")
    neg_n = sum(1 for n in news if n["sentiment"] == "negative")
    neu_n = sum(1 for n in news if n["sentiment"] == "neutral")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Headlines",  f"{len(news)}")
    s2.metric("Positive ✅",      f"{pos_n}")
    s3.metric("Neutral ⬜",       f"{neu_n}")
    s4.metric("Negative ❌",      f"{neg_n}")

    sf = st.selectbox("Filter by sentiment", ["All","positive","neutral","negative"])
    filtered = news if sf == "All" else [n for n in news if n["sentiment"] == sf]

    css_map = {"positive":"news-pos","negative":"news-neg","neutral":"news-neu"}
    tag_map  = {
        "positive": f'<span class="tag-green">positive</span>',
        "negative": f'<span class="tag-red">negative</span>',
        "neutral":  f'<span class="tag-navy">neutral</span>',
    }

    st.markdown("")
    for item in filtered:
        link_html = (f'<a href="{item["link"]}" target="_blank" '
                     f'style="font-size:0.72rem;color:{TEAL};text-decoration:none;font-weight:600;">Read →</a>'
                     if item["link"] != "#" else "")
        st.markdown(f"""
        <div class="{css_map[item['sentiment']]}">
          <div class="news-title">{item['title']}</div>
          <div class="news-meta">
            {tag_map[item['sentiment']]} &nbsp; {item['date']} &nbsp; {link_html}
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">News Sentiment Distribution</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        sent_fig = go.Figure(go.Pie(
            labels=["Positive","Neutral","Negative"],
            values=[max(pos_n,1), max(neu_n,1), max(neg_n,1)],
            hole=0.52,
            marker_colors=[GREEN, TEAL, RED],
            textinfo="label+percent",
            textfont=dict(color="#1A1A2E", size=12)
        ))
        sent_fig.update_layout(height=260, paper_bgcolor="#FFFFFF",
                               margin=dict(l=20,r=20,t=20,b=20),
                               font=dict(color="#1A1A2E"),
                               legend=dict(font=dict(color="#1A1A2E")))
        st.plotly_chart(sent_fig, use_container_width=True)
    with c2:
        st.markdown(f"""
        <div class="q-card-navy">
          <b style="color:{NAVY};">How to Read PLTR News Flow</b><br>
          <span style="font-size:0.85rem;color:#1e3a5f;">
            <b>Signal headlines</b> (high weight): Government contract wins/losses, AIP commercial customer counts,
            U.S. Commercial revenue growth rate, CEO/CFO commentary on AIP conversion rates,
            DoD budget announcements affecting classified AI spending.<br><br>
            <b>Noise headlines</b> (low weight): Analyst price target changes, retail investor sentiment,
            macro rate speculation, Alex Karp's philosophical statements in earnings calls.<br><br>
            <b>Watch for:</b> Any news on U.S. Commercial quarterly growth rate (primary re-rating driver),
            Q1 FY2025 earnings beat/miss, TITAN contract awards, NATO allied government AI expansions.
          </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="q-card-orange">
          <b style="color:{ORANGE};">Key Upcoming Catalysts</b><br>
          <span style="font-size:0.83rem;color:#7A2800;">
            · Q1 FY2025 Earnings (Expected ~May 2025)<br>
            · TITAN (Tactical Intelligence Targeting Access Node) contract awards<br>
            · U.S. Commercial customer count update (watch for >1,000 milestone)<br>
            · NATO allied government AI contract announcements (Poland, Germany)<br>
            · AIP Enterprise pricing/packaging update (potential mid-market catalyst)<br>
            · Any S&P 500 index rebalancing effects on institutional ownership
          </span>
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <div style="margin-bottom:6px;">
    <b style="color:{NAVY};font-size:0.8rem;font-family:'Space Grotesk',sans-serif;">
      PALANTIR TECHNOLOGIES (PLTR) — RESEARCH TERMINAL
    </b>
  </div>
  Live Data: Yahoo Finance &nbsp;·&nbsp;
  Fundamentals: Palantir 10-K FY2021–FY2025E &nbsp;·&nbsp;
  News: Google News RSS &nbsp;·&nbsp;
  Framework: Damodaran (NYU Stern) &nbsp;·&nbsp;
  {datetime.now().strftime("%d %B %Y  %H:%M")}
  <br><br>
  <span class="footer-author">✦ Prepared by: Krrish Bahuguna &nbsp;·&nbsp; IPM2 &nbsp;·&nbsp; MBA Corporate Finance</span>
  <br>
  <b style="color:#9CA3AF;">Academic use only — not investment advice. All projections are estimates.</b>
</div>
""", unsafe_allow_html=True)