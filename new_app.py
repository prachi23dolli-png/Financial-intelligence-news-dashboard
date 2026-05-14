import streamlit as st
from market_data import get_market_data
from news_fetcher import fetch_news, RSS_FEEDS
from text_utils import (
    clean_summary,
    short_paragraph,
    extract_key_points
)
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Financial Intelligence Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- AUTO REFRESH ---------------- #

st_autorefresh(interval=60000, key="refresh")

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main App */
.stApp {
    background-color: #0B0F19;
    color: white;
}

/* Headings */
h1, h2, h3 {
    color: #00D4FF;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background-color: #161B22;
    border: 1px solid #2D3748;
    padding: 15px;
    border-radius: 14px;
}

/* News Cards */
.news-card {
    background-color: #161B22;
    border: 1px solid #2D3748;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
}

/* Featured Card */
.feature-card {
    background: linear-gradient(
        135deg,
        #1A2333,
        #111827
    );
    border: 1px solid #00D4FF;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 25px;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 600;
}

/* Search */
.stTextInput input {
    background-color: #161B22;
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.title("AI Financial Intelligence Dashboard")

st.caption(
    "Live markets, macro tracking, and financial intelligence"
)

# ---------------- MARKET STATUS ---------------- #

market_status = "🟢 Market Open"

current_time = datetime.now().strftime(
    "%d %b %Y | %I:%M %p"
)

st.markdown(
    f"""
    <div style='
        background-color:#111827;
        padding:12px;
        border-radius:12px;
        margin-bottom:20px;
    '>
    <b>{market_status}</b>
    <span style='float:right'>
    Last Updated: {current_time}
    </span>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- MARKET TICKER ---------------- #

market_data = get_market_data()

st.subheader("Live Market Overview")

market_cols = st.columns(len(market_data))

for col, (market, values) in zip(
    market_cols,
    market_data.items()
):

    with col:

        st.metric(
            market,
            values["price"],
            f"{values['change']}%"
        )

st.markdown("---")

# ---------------- SEARCH ---------------- #

search_query = st.text_input(
    "Search financial news"
)

# ---------------- FETCH NEWS ---------------- #

news = fetch_news()

# ---------------- FEATURED STORY ---------------- #

if news:

    top_story = news[0]

    featured_summary = short_paragraph(
        clean_summary(top_story["summary"]),
        max_sentences=3
    )

    st.markdown("## 🔥 Top Market Story")

    st.badge(
        top_story.get("category", "General")
    )

    st.subheader(top_story["title"])

    st.write(featured_summary)

    st.link_button(
        "Read Full Story",
        top_story["link"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- TABS ---------------- #

tabs = st.tabs(
    ["All"] + list(RSS_FEEDS.keys())
)

# ---------------- RENDER NEWS ---------------- #

for tab, category in zip(
    tabs,
    ["All"] + list(RSS_FEEDS.keys())
):

    with tab:

        filtered_news = []

        for article in news:

            article_category = article.get(
                "category",
                "General"
            )

            # Tab filtering
            if category != "All":

                if article_category != category:
                    continue

            # Search filtering
            if search_query:

                if (
                    search_query.lower()
                    not in article["title"].lower()
                ):
                    continue

            filtered_news.append(article)

        # News Count
        st.caption(
            f"Showing {len(filtered_news)} articles"
        )

        # Compact 2-column layout
        cols = st.columns(2)

        for idx, article in enumerate(filtered_news):

            clean_text = clean_summary(
                article["summary"]
            )

            short_text = short_paragraph(
                clean_text,
                max_sentences=2
            )

            key_points = extract_key_points(
                clean_text
            )

            with cols[idx % 2]:

                st.badge(
                    article.get(
                        "category",
                        "General"
                    )
                )

                st.markdown(
                    f"### {article['title']}"
                )

                st.write(short_text)

                if key_points:

                    st.markdown(
                        "#### Key Points"
                    )

                    for point in key_points[:2]:

                        st.write(
                            f"• {point}"
                        )

                st.link_button(
                    "Read More",
                    article["link"]
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown(
    """
    <div class="footer">
    Built using Python, Streamlit, RSS feeds,
    and financial market APIs
    </div>
    """,
    unsafe_allow_html=True
)
