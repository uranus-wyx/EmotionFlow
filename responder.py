### responder.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from openai import OpenAI, RateLimitError, APIError
from secret import get_secret

load_dotenv()
# gemini_api_key = get_secret("GEMINI_API_KEY")
# api_key = gemini_api_key
# genai.configure(api_key = api_key)
# model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

openai_api_key = get_secret("OPENAI_API_KEY")

api_key = openai_api_key
client = OpenAI(api_key=openai_api_key)

def generate_response_gemini(user_input, emotion=None):
    """
    Generate an empathetic response using OpenAI (gpt-4o-mini).
    This keeps the original function name for backward compatibility.
    """

    # Build empathetic system prompt
    system_prompt = """
    You are an empathetic AI counselor.
    Your job is to respond with emotional warmth, support, validation,
    and encouragement. Your tone should be calm, caring, and human-like.
    
    Always reply in **1 or 2 sentences only**, no more.
    Do NOT give advice unless asked. Focus on empathy first.
    """

    # Build user prompt
    user_prompt = f'User says: "{user_input}"'
    if emotion:
        user_prompt = f'The user is feeling: "{emotion}".\n' + user_prompt

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.6,  # more emotional + warm
        )

        output = response.choices[0].message.content.strip()
        return output

    except RateLimitError as e:
        print(f"[ERROR] OpenAI rate limit exceeded: {e}")
        return "I’m here for you, even if I’m a bit overwhelmed right now. Please try again shortly."

    except APIError as e:
        print(f"[ERROR] OpenAI API error: {e}")
        return "I'm so sorry — something went wrong on my end. Please try again in a moment."

    except Exception as e:
        print(f"[ERROR] Unexpected error in generate_response_gemini: {e}")
        return "I'm here for you, even though I'm having a little trouble responding right now."
