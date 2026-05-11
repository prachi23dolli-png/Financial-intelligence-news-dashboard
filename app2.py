import streamlit as st
from market_data import get_market_data
from news_fetcher import fetch_news, RSS_FEEDS
from streamlit_autorefresh import st_autorefresh
from text_utils import (
    clean_summary,
    short_paragraph,
    extract_key_points
)
st_autorefresh(interval=300000, key="refresh")

st.title("AI Financial Dashboard")
categories = categories = ["All"] + list(RSS_FEEDS.keys())

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

search_query = st.text_input("Search News")

market_data = get_market_data()

for market, values in market_data.items():

    st.metric(
        market,
        values["price"],
        f'{values["change"]}%'
    )
    

st.header("Latest Financial News")

news = fetch_news()

for article in news:

    article_category = article.get("category", "General")

    # Category filter
    if selected_category != "All":

        if article_category != selected_category:
            continue

    # Search filter
    if search_query:

        if search_query.lower() not in article["title"].lower():
            continue

    clean_text = clean_summary(article["summary"])

    short_text = short_paragraph(clean_text)

    key_points = extract_key_points(clean_text)

    st.badge(article_category)

    st.subheader(article["title"])

    st.write(short_text)

    st.markdown("### Key Points")

    for point in key_points:

        st.write(f"• {point}")

    st.write(article["link"])

    st.divider()


