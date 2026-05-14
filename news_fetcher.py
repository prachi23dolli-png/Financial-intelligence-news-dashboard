
import streamlit as st
import feedparser
IMPORTANT_KEYWORDS = [

    # Macro
    "inflation",
    "GDP",
    "recession",
    "economy",
    "economic growth",
    "fiscal deficit",

    # Central Banks
    "RBI",
    "Federal Reserve",
    "ECB",
    "interest rates",
    "repo rate",
    "monetary policy",

    # Markets
    "stocks",
    "markets",
    "Sensex",
    "Nifty",
    "bond yields",
    "forex",
    "USD",
    "treasury",

    # Banking
    "bank",
    "banking",
    "liquidity",
    "credit growth",

    # Commodities
    "gold",
    "crude oil",
    "oil prices",

    # Corporate
    "earnings",
    "IPO",
    "profit",
    "revenue",
    "valuation",

    # Global
    "China",
    "US economy",
    "trade war",
    "tariffs"
]

def is_relevant_news(title, summary):

    text = f"{title} {summary}".lower()

    for keyword in IMPORTANT_KEYWORDS:

        if keyword.lower() in text:
            return True

    return False
RSS_FEEDS = {

    "Global": [
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://feeds.a.dj.com/rss/RSSWorldNews.xml"
    ],
    "Markets": [
        "https://www.livemint.com/rss/markets",
        "https://www.moneycontrol.com/rss/business.xml",
        "https://www.financialexpress.com/market/feed/"
    ],
    "RBI": [
    "https://news.google.com/rss/search?q=RBI+monetary+policy"
],
    "Economy": [
        "https://feeds.feedburner.com/ndtvprofit-latest",
        "https://www.moneycontrol.com/rss/economy.xml"
    ],

    "Technology":[
        "https://feeds.feedburner.com/TechCrunch/",
    ],
    
    "Startups":[
        "https://yourstory.com/feed"
    ]
}

@st.cache_data(ttl=60)
def fetch_news():

    articles = []

    seen_titles = set()

    for category, urls in RSS_FEEDS.items():

        for url in urls:

            feed = feedparser.parse(url)
            print(category, len(feed.entries))

            for entry in feed.entries[:5]:

                title = entry.title

                # Skip duplicates
                if title in seen_titles:
                    continue

                seen_titles.add(title)

                summary = entry.summary if "summary" in entry else ""
                if not is_relevant_news(title, summary):
                    continue
                
                articles.append({
                    "category": category,
                    "title": title,
                    "summary": summary,
                    "link": entry.link,
                    "published": entry.published
                    if "published" in entry
                    else ""
})

                articles = sorted(
                    articles,
                    key=lambda x: x.get("published", ""),
                    reverse=True
                    )
    return articles