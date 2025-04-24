# recommender.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = 'AIzaSyBpFbBbEwSA7H0up-Hoa9ky9sLWWn6NmAU'
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

client_id = 'd3bb3143abed4ddea34191cea72c0b46'
client_secret = '174b41640e5641da90be6a65c40f2e52'

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