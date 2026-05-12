from bs4 import BeautifulSoup
import streamlit as st
import re

@st.cache_data
def clean_summary(text):

    # Remove HTML
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text()

    # Remove extra spaces
    clean_text = re.sub(r'\s+', ' ', clean_text)

    return clean_text.strip()

@st.cache_data
def short_paragraph(text, max_sentences=2):

    sentences = text.split('.')

    short_text = '. '.join(sentences[:max_sentences])

    return short_text.strip() + "."

@st.cache_data

def extract_key_points(
    text,
    skip_sentences=2,
    max_points=5
):

    sentences = text.split('.')

    points = []

    seen = set()

    # Skip summary sentences
    remaining_sentences = sentences[
        skip_sentences:
    ]

    for sentence in remaining_sentences:

        clean_sentence = sentence.strip()

        if (
            len(clean_sentence) > 30
            and clean_sentence not in seen
        ):

            seen.add(clean_sentence)

            points.append(clean_sentence)

    return points[:max_points]