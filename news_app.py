import streamlit as st
from market_data import get_market_data
from news_fetcher import fetch_news, RSS_FEEDS
from streamlit_autorefresh import st_autorefresh
from text_utils import (
    clean_summary,
    short_paragraph,
    extract_key_points
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Financial Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- AUTO REFRESH ---------------- #

st_autorefresh(interval=300000, key="refresh")

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Headers */
h1, h2, h3 {
    color: #00D4FF;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Market Cards */
div[data-testid="metric-container"] {
    background-color: #1A1F2E;
    border: 1px solid #2A2F3E;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
}

/* News Cards */
.news-card {
    background-color: #161B22;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #2D3748;
    margin-bottom: 20px;
}

/* Search Box */
.stTextInput > div > div > input {
    background-color: #1A1F2E;
    color: white;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #1A1F2E;
}

/* Divider */
hr {
    border-color: #2D3748;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Dashboard Controls")

categories = ["All"] + list(RSS_FEEDS.keys())

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

search_query = st.sidebar.text_input(
    "Search Financial News"
)

st.sidebar.markdown("---")

st.sidebar.caption("AI Financial Intelligence Dashboard")

# ---------------- HEADER ---------------- #

st.title("AI Financial Intelligence Dashboard")

st.caption(
    "Live markets, macro updates, and financial news"
)

st.markdown("---")

# ---------------- MARKET DATA ---------------- #

market_data = get_market_data()

st.subheader("Live Market Overview")

market_cols = st.columns(len(market_data))

for col, (market, values) in zip(market_cols, market_data.items()):

    with col:

        st.metric(
            market,
            values["price"],
            f'{values["change"]}%'
        )

st.markdown("---")

# ---------------- NEWS SECTION ---------------- #

st.subheader("Latest Financial News")

news = fetch_news()

for article in news:

    article_category = article.get("category", "General")

    # Category Filter
    if selected_category != "All":

        if article_category != selected_category:
            continue

    # Search Filter
    if search_query:

        if search_query.lower() not in article["title"].lower():
            continue

    clean_text = clean_summary(article["summary"])

    short_text = short_paragraph(clean_text)

    key_points = extract_key_points(clean_text)

    # -------- NEWS CARD -------- #

key_points_html = ""

for point in key_points:
    key_points_html += f"<li>{point}</li>"

card_html = f"""
<div style="
    background-color:#161B22;
    padding:25px;
    border-radius:18px;
    border:1px solid #2D3748;
    margin-bottom:20px;
">

    <span style="
        background-color:#00D4FF;
        color:black;
        padding:6px 12px;
        border-radius:10px;
        font-size:12px;
        font-weight:bold;
    ">
        {article_category}
    </span>

    <h3 style="
        color:white;
        margin-top:15px;
    ">
        {article["title"]}
    </h3>

    <p style="
        color:#D1D5DB;
        font-size:16px;
        line-height:1.7;
    ">
        {short_text}
    </p>

    <h4 style="color:#00D4FF;">
        Key Points
    </h4>

    <ul style="
        color:#E5E7EB;
        line-height:1.8;
    ">
        {key_points_html}
    </ul>

    <a href="{article['link']}"
       target="_blank"
       style="
        text-decoration:none;
       ">
        <button style="
            background-color:#00D4FF;
            color:black;
            border:none;
            padding:10px 18px;
            border-radius:10px;
            cursor:pointer;
            font-weight:bold;
        ">
            Read Full Article
        </button>
    </a>

</div>
"""

st.markdown(card_html, unsafe_allow_html=True)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.caption(
    "Built using Streamlit, Python, RSS feeds, and financial market APIs"
)