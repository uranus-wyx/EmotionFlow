### classifier.py
import json
from dotenv import load_dotenv
import google.generativeai as genai
from secret import get_secret

GEMINI_API_KEY = "AIzaSyBpFbBbEwSA7H0up-Hoa9ky9sLWWn6NmAU"
MONGODB_URI = "mongodb+srv://yuniwu:NpCOR24HEnxdnVpX@cluster0.sdsbxna.mongodb.net/"

load_dotenv()
# gemini_api_key = get_secret("GEMINI_API_KEY")
gemini_api_key = GEMINI_API_KEY

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
    You are an emotion classification assistant. Based on the text input, return the most likely emotion from this list:

    {emotion_list}

    User input: "{user_input}"

    Respond with only the emotion and one emoji.
    """

    response = model.generate_content(prompt)
    emotion = response.text.strip()
    category = get_emotion_category(emotion)
    
    return {
        "emotion": emotion,
        "category": category
    }