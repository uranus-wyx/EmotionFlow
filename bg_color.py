### bg_color.py
# Core Libraries
from dotenv import load_dotenv

# Third-Party Libraries
import google.generativeai as genai

# App Configuration
import config

load_dotenv()
api_key = config.GEMINI_API_KEY
genai.configure(api_key = api_key)
model = genai.GenerativeModel(model_name = config.MODEL_NAME)

def generate_color(emotion = None):

    prompt = f"""
    You are an assistant that provides a smooth gradient background for a web page based on the emotion "{emotion}".
    Return a list of 3 HEX color codes that flow well together.
    Respond only with the HEX codes, separated by commas. No extra text.
    """

    response = model.generate_content(prompt)
    color = response.text.strip()

    return color