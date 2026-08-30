import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st


API_URL = os.getenv("STOCKBOT_API_URL", "http://localhost:8000")

st.set_page_config(page_title="Stockflow | Investment dashboard", page_icon="◈", layout="wide")

st.markdown(
    """
    <style>
    :root { --bg: #07111f; --panel: #0d1a2d; --panel-2: #101f35; --line: #203452;
            --text: #f1f5fb; --muted: #94a3b8; --blue: #4f8cff; --green: #2dd4a4; }
    .stApp { background: radial-gradient(circle at 78% -8%, #15315b 0, transparent 25rem), #07111f; color: var(--text); }
    [data-testid="stSidebar"] { background: #091629; border-right: 1px solid #1b2d49; }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.1rem; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { max-width: 1440px; padding: 1.5rem 2.2rem 3rem; }
    .brand { display:flex; align-items:center; gap:10px; font-size:1.15rem; font-weight:750; letter-spacing:-.02em; margin: .25rem .4rem 2rem; }
    .brand-mark { display:grid; place-items:center; width:31px; height:31px; border-radius:10px; background:linear-gradient(135deg,#4f8cff,#5b47e5); color:white; }
    .eyebrow { color:#8da0bd; font-size:.82rem; font-weight:650; text-transform:uppercase; letter-spacing:.08em; }
    .page-title { font-size:1.85rem; font-weight:760; letter-spacing:-.045em; margin: .2rem 0; }
    .subtle { color:var(--muted); font-size:.9rem; }
    .metric-card { background:linear-gradient(145deg,#11213a,#0c192c); border:1px solid #203452; border-radius:15px; padding:1.1rem 1.15rem; min-height:120px; }
    .metric-label { color:#9aabc3; font-size:.83rem; margin-bottom:.65rem; }
    .metric-value { font-size:1.55rem; font-weight:730; letter-spacing:-.04em; }
    .metric-change { color:#2dd4a4; font-size:.78rem; margin-top:.6rem; }
    .panel { background:rgba(13,26,45,.88); border:1px solid #203452; border-radius:15px; padding:1.2rem; height:100%; }
    .panel-title { font-weight:700; font-size:1rem; margin-bottom:.25rem; }
    .allocation-bar { height:11px; border-radius:99px; overflow:hidden; display:flex; background:#14223a; margin:1.15rem 0 .6rem; }
    .empty-state { border:1px dashed #304667; border-radius:14px; padding:1.3rem; color:#a8b7cb; text-align:center; margin-top:.6rem; }
    .stButton > button { background: #377df6; color:white; border:0; border-radius:9px; font-weight:650; padding:.55rem 1rem; }
    .stButton > button:hover { background:#5593fb; color:white; border:0; }
    .stTextInput input, .stNumberInput input { background:#0a1628 !important; border:1px solid #28405f !important; color:#edf5ff !important; border-radius:9px !important; }
    [data-testid="stMetric"] { background:#0d1a2d; border:1px solid #203452; border-radius:12px; padding:1rem; }
    /* Sidebar navigation: clean full-width buttons with no radio bullets. */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: .28rem; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent; border-radius: 8px; padding: .58rem .7rem; width: 100%;
        color: #aebed4; font-size: .92rem; font-weight: 560; transition: background .15s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: #102441; color: #f1f5fb; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background: #17356b; color: #f6f9ff; font-weight: 680; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display: none; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label > div:last-child { margin-left: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def money(value, currency="INR"):
    if value is None:
        return "—"
    try:
        value = float(value)
        if currency == "INR":
            if abs(value) >= 10_000_000:
                return f"₹{value / 10_000_000:.2f} Cr"
            if abs(value) >= 100_000:
                return f"₹{value / 100_000:.2f} L"
            return f"₹{value:,.2f}"
        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"
        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return str(value)


def api_request(method, endpoint, **kwargs):
    try:
        return requests.request(method, f"{API_URL}{endpoint}", timeout=8, **kwargs)
    except requests.RequestException:
        return None


with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span> Stockflow</div>', unsafe_allow_html=True)
    page = st.radio("Navigate", ["Overview", "Market explorer", "Portfolio", "AI analyst"], label_visibility="collapsed")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("YOUR WORKSPACE")
    st.markdown("**Personal portfolio**  ")
    st.caption("Live market data · INR")
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("© 2026 STOCKFLOW")


def page_heading(label, title, description):
    left, right = st.columns([7, 1])
    with left:
        st.markdown(f'<div class="eyebrow">{label}</div><div class="page-title">{title}</div><div class="subtle">{description}</div>', unsafe_allow_html=True)
    with right:
        st.markdown(f"<div style='text-align:right; padding-top:.6rem' class='subtle'>● Live<br>{datetime.now().strftime('%b %d, %Y')}</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)


if page == "Overview":
    page_heading("Personal finance", "Your investing command center", "See your holdings, allocation, and market opportunities at a glance.")
    response = api_request("GET", "/portfolio")
    holdings = response.json() if response and response.ok else []
    invested = sum(float(item.get("quantity", 0)) * float(item.get("buy_price", 0)) for item in holdings)
    positions = len(holdings)
    c1, c2, c3, c4 = st.columns(4)
    values = [("Portfolio value", money(invested), "Your cost basis"), ("Invested capital", money(invested), f"Across {positions} positions"), ("Today's movement", "—", "Connect live holdings to track"), ("Available cash", "₹0.00", "Add your cash balance")]
    for col, (label, val, delta) in zip([c1, c2, c3, c4], values):
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{val}</div><div class="metric-change">{delta}</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    left, right = st.columns([1.65, 1])
    with left:
        st.markdown('<div class="panel"><div class="panel-title">Portfolio allocation</div><div class="subtle">Your exposure by holding</div>', unsafe_allow_html=True)
        if holdings and invested:
            colors = ["#4f8cff", "#2dd4a4", "#8b5cf6", "#f5b945", "#f9736c"]
            segments = "".join(f'<span style="width:{item["quantity"] * item["buy_price"] / invested * 100:.1f}%;background:{colors[i % len(colors)]}"></span>' for i, item in enumerate(holdings))
            st.markdown(f'<div class="allocation-bar">{segments}</div>', unsafe_allow_html=True)
            cols = st.columns(min(len(holdings), 4))
            for i, item in enumerate(holdings[:4]):
                share = item["quantity"] * item["buy_price"] / invested * 100
                cols[i].markdown(f"**{item['symbol'].upper()}**  \n<span class='subtle'>{share:.1f}% · {money(item['quantity'] * item['buy_price'])}</span>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state">Your allocation will appear here after you add your first investment.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><div class="panel-title">Market pulse</div><div class="subtle">Build a watchlist in Market explorer to stay on top of ideas.</div><div class="empty-state">No securities tracked yet</div></div>', unsafe_allow_html=True)

elif page == "Market explorer":
    page_heading("Research", "Market explorer", "Look up a company before deciding whether it belongs in your portfolio.")
    symbol = st.text_input("Ticker symbol", placeholder="Try RELIANCE.NS, TCS.NS, INFY.NS")
    if st.button("Search market data", use_container_width=False):
        if not symbol.strip():
            st.warning("Enter a ticker symbol first.")
        else:
            with st.spinner("Fetching market data..."):
                response = api_request("GET", f"/stock/{symbol.strip().upper()}")
            if response and response.ok:
                data = response.json()
                st.success(f"Market snapshot for {symbol.upper()}")
                a, b, c, d = st.columns(4)
                is_indian_stock = symbol.strip().upper().endswith((".NS", ".BO"))
                market_currency = "INR" if is_indian_stock else "USD"
                a.metric("Current price", money(data.get("current price"), market_currency))
                b.metric("Market cap", money(data.get("market_cap"), market_currency))
                c.metric("52-week high", money(data.get("high_52week"), market_currency))
                d.metric("52-week low", money(data.get("low_52week"), market_currency))
            else:
                st.error("Could not load this symbol. Ensure the API server is running and try a valid ticker.")

elif page == "Portfolio":
    page_heading("Holdings", "Portfolio", "Keep a simple, clear record of every investment you own.")
    left, right = st.columns([1, 1.8])
    with left:
        st.markdown('<div class="panel"><div class="panel-title">Add an investment</div><div class="subtle">Record your purchase price and number of shares.</div>', unsafe_allow_html=True)
        with st.form("add_holding", clear_on_submit=True):
            symbol = st.text_input("Ticker symbol", placeholder="RELIANCE.NS")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            buy_price = st.number_input("Average buy price", min_value=0.0, step=0.01)
            submitted = st.form_submit_button("Add to portfolio", use_container_width=True)
        if submitted:
            response = api_request("POST", "/portfolio", json={"symbol": symbol.upper().strip(), "quantity": quantity, "buy_price": buy_price})
            if response and response.ok:
                st.success("Investment added to your portfolio.")
                st.rerun()
            else:
                st.error("Could not save the holding. Is the API server running?")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        response = api_request("GET", "/portfolio")
        holdings = response.json() if response and response.ok else []
        st.markdown('<div class="panel"><div class="panel-title">Your positions</div><div class="subtle">Cost basis based on the entries below.</div>', unsafe_allow_html=True)
        if holdings:
            frame = pd.DataFrame(holdings)
            frame["Cost basis"] = frame["quantity"] * frame["buy_price"]
            frame = frame.rename(columns={"symbol": "Symbol", "quantity": "Shares", "buy_price": "Avg. cost"})[["Symbol", "Shares", "Avg. cost", "Cost basis"]]
            st.dataframe(frame, use_container_width=True, hide_index=True, column_config={"Avg. cost": st.column_config.NumberColumn(format="₹%.2f"), "Cost basis": st.column_config.NumberColumn(format="₹%.2f")})
        else:
            st.markdown('<div class="empty-state">No investments yet. Use the form to add your first position.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    page_heading("Intelligence", "AI investment analyst", "Ask concise research questions and get a focused market perspective.")
    st.markdown('<div class="panel"><div class="panel-title">What would you like to understand?</div><div class="subtle">For example: “What should I watch before investing in NVDA?”</div>', unsafe_allow_html=True)
    prompt = st.text_area("Ask your question", placeholder="Ask about a stock, sector, or market concept…", label_visibility="collapsed", height=125)
    if st.button("Ask analyst"):
        if not prompt.strip():
            st.warning("Write a question for the analyst first.")
        else:
            with st.spinner("Analyst is reviewing your question..."):
                response = api_request("POST", "/chat", json={"content": prompt})
            if response and response.ok:
                st.markdown("<br>", unsafe_allow_html=True)
                st.info(response.json().get("response", "No response received."))
            else:
                st.error("Could not reach the analyst service. Check that the API and its credentials are configured.")
    st.markdown("</div>", unsafe_allow_html=True)
