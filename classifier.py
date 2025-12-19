### classifier.py
import json
from dotenv import load_dotenv
import google.generativeai as genai
from secret import get_secret
from google.api_core.exceptions import ResourceExhausted, GoogleAPIError
import openai
from openai import OpenAI
from openai import APIError, RateLimitError

load_dotenv()
# gemini_api_key = get_secret("GEMINI_API_KEY")
openai_api_key = get_secret("OPENAI_API_KEY")

api_key = openai_api_key
client = OpenAI(api_key=openai_api_key)
# genai.configure(api_key = api_key)
# model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

with open("emotions.json", "r", encoding="utf-8") as f:
    emotion_categories = json.load(f)

emotion_list = []
for emotions in emotion_categories.values():
    emotion_list.extend(emotions)

def get_emotion_category(emotion_label):
    for category, emotions in emotion_categories.items():
        if emotion_label in emotions:
            return category
    return "Unknown"

def classify_emotion_gemini(user_input):
    prompt = f"""
    You are an emotion classification assistant. Based on the text input, return
    the most likely emotion from this list:

    {emotion_list}

    User input: "{user_input}"

    Respond with only the emotion and one emoji.
    """

    try:
        # response = model.generate_content(prompt)
        # emotion = response.text.strip()
        # category = get_emotion_category(emotion)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.2,
        )

        # Extract output text
        output = response.choices[0].message.content.strip()

        # Determine category
        category = get_emotion_category(output)

        return {
            "ok": True,
            "emotion": output,
            "category": category
        }

    except RateLimitError as e:
        print(f"[ERROR] OpenAI rate limit: {e}")
        return {
            "ok": False,
            "error_type": "quota",
            "message": "OpenAI rate limit exceeded. Please try again later."
        }

    except APIError as e:
        print(f"[ERROR] OpenAI API error: {e}")
        return {
            "ok": False,
            "error_type": "api",
            "message": "OpenAI API error occurred. Please try again later."
        }

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return {
            "ok": False,
            "error_type": "unknown",
            "message": "Unexpected server error occurred."
        }