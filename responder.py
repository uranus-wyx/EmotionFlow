### responder.py
# Core Libraries
import os
from dotenv import load_dotenv

# Third-Party Libraries
import google.generativeai as genai

# App Configuration
import config

load_dotenv()
api_key = config.GEMINI_API_KEY
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name=config.MODEL_NAME)

def generate_response_gemini(user_input, emotion=None):
    """
    Response with empathetic by Gemini
    emotion: input classification emotion words to improve the prompt.
    """
    # prompt
    prompt = f"""
    You are an empathetic AI counselor. 
    Your goal is to understand the user's emotional state and respond in a warm, supportive, and caring way.

    {"The user's emotion is: " + emotion + "." if emotion else ""}
    User says: "{user_input}"

    Please reply with one or two sentences that show empathy and encouragement.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
