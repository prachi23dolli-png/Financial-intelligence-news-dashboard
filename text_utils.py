from bs4 import BeautifulSoup
import re

def clean_summary(text):

    # Remove HTML
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()

    # Remove extra spaces
    clean_text = re.sub(r'\s+', ' ', clean_text)

    return clean_text.strip()

def short_paragraph(text, max_sentences=2):

    sentences = text.split('.')

    short_text = '. '.join(sentences[:max_sentences])

    return short_text.strip() + "."
def extract_key_points(text):

    finance_keywords = [
        "RBI",
        "Fed",
        "inflation",
        "repo rate",
        "GDP",
        "crude oil",
        "bond yields",
        "earnings",
        "IPO",
        "stocks",
        "markets",
        "forex",
        "USD",
        "banking"
    ]

    points = []

    sentences = text.split('.')

    for sentence in sentences:

        for keyword in finance_keywords:

            if keyword.lower() in sentence.lower():

                points.append(sentence.strip())

                break

    return points[:3]