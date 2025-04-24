import google.generativeai as genai
import json

api_key = 'AIzaSyBpFbBbEwSA7H0up-Hoa9ky9sLWWn6NmAU'
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

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