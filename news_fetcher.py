import streamlit as st
import feedparser

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
    "https://rbi.org.in/rss/RSS.aspx?Id=200"
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

@st.cache_data(ttl=300)
def fetch_news():

    articles = []

    seen_titles = set()

    for category, urls in RSS_FEEDS.items():

        for url in urls:

            feed = feedparser.parse(url)
            print(category, len(feed.entries))

            for entry in feed.entries[:10]:

                title = entry.title

                # Skip duplicates
                if title in seen_titles:
                    continue

                seen_titles.add(title)

                articles.append({

                    "category": category,

                    "title": title,

                    "summary": entry.summary if "summary" in entry else "",

                    "link": entry.link
                })

    return articles