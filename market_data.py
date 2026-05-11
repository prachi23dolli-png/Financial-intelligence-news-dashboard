import streamlit as st
import yfinance as yf

@st.cache_data(ttl=60)
def get_market_data():

    symbols = {
        "NIFTY50": "^NSEI",
        "SENSEX": "^BSESN",
        "USDINR": "INR=X",
        "GOLD": "GC=F",
        "CRUDE": "CL=F"
    }

    data = {}

    for name, ticker in symbols.items():

        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")

        if not hist.empty:

            latest = hist["Close"].iloc[-1]
            open_price = hist["Open"].iloc[0]

            change = latest - open_price
            pct_change = (change / open_price) * 100

            data[name] = {
                "price": round(latest, 2),
                "change": round(pct_change, 2)
            }

    return data