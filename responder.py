# responder_gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = 'AIzaSyBpFbBbEwSA7H0up-Hoa9ky9sLWWn6NmAU'
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def generate_response_gemini(user_input, emotion=None):
    """
    使用 Gemini 生成共情回复。
    emotion: 可传入先前分类得到的情绪词，帮助改善提示效果。
    """
    # prompt
    prompt = f"""
    You are an empathetic AI counselor. 
    Your goal is to understand the user's emotional state and respond in a warm, supportive, and caring way.

    {"The user's emotion is: " + emotion + "." if emotion else ""}
    User says: "{user_input}"

    Please reply with one or two sentences that show empathy and encouragement.
    """

    # API
    response = model.generate_content(prompt)
    return response.text.strip()
