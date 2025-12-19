### classifier.py
import json
from dotenv import load_dotenv
import google.generativeai as genai
from secret import get_secret
from google.api_core.exceptions import ResourceExhausted, GoogleAPIError

load_dotenv()
gemini_api_key = get_secret("GEMINI_API_KEY")

api_key = gemini_api_key
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

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
        response = model.generate_content(prompt)
        emotion = response.text.strip()
        category = get_emotion_category(emotion)

        return {
            "ok": True,
            "emotion": emotion,
            "category": category
        }

    except ResourceExhausted as e:
        # 偵測到 Gemini 配額/速率限制用完
        print(f"[ERROR] Gemini quota exceeded: {e}")
        return {
            "ok": False,
            "error_type": "quota",
            "message": "The emotion analysis service has exceeded its quota. Please try again later."
        }

    except GoogleAPIError as e:
        # Google API（Gemini）其他錯誤
        print(f"[ERROR] Gemini API error: {e}")
        return {
            "ok": False,
            "error_type": "api",
            "message": "A Gemini API error occurred. Please try again later."
        }

    except Exception as e:
        # 捕捉所有未知錯誤，避免 500
        print(f"[ERROR] Unexpected error: {e}")
        return {
            "ok": False,
            "error_type": "unknown",
            "message": "Unexpected server error occurred."
        }