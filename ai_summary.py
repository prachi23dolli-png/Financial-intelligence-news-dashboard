import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_news(text):

    prompt = f"""
    You are a financial analyst.

    Summarize this finance article into:

    1. Key headline
    2. 3 bullet points
    3. Market impact
    4. Investor takeaway

    Article:
    {text}
    """

    response = model.generate_content(prompt)

    return response.text