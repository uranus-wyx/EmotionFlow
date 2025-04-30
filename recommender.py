### recommender.py
from dotenv import load_dotenv
import google.generativeai as genai
from secret import get_secret

load_dotenv()
gemini_api_key = get_secret("GEMINI_API_KEY")
api_key = gemini_api_key
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def generate_music_recommendation(user_input, emotion):
    prompt = f"""
    You are a music therapist AI. Based on the user's emotion and what they said, recommend a song that matches their feelings and may help them feel understood or comforted.

    Emotion: {emotion}
    User input: "{user_input}"

    Please respond in the following format:
    Song: <song name>
    Artist: <artist>
    Reason: <short reason>
    """
    response = model.generate_content(prompt)
    return response.text.strip()