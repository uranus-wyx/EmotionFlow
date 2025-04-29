### recommender.py
# Core Libraries
from dotenv import load_dotenv

# Third-Party Libraries
import google.generativeai as genai

# App Configuration
import config

load_dotenv()
api_key = config.GEMINI_API_KEY
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name=config.MODEL_NAME)

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