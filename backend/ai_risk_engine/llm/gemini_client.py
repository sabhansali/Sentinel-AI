import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

def ask_gemini(prompt):
    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )
    response = model.generate_content(prompt)

    return response.text