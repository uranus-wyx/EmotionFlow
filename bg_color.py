### bg_color.py
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
model = genai.GenerativeModel(model_name = "models/gemini-2.0-flash")

def generate_color(emotion = None):

    prompt = f"""
    You are an assistant that provides a smooth gradient background for a web page based on the emotion "{emotion}".
    Return a list of 3 HEX color codes that flow well together.
    Respond only with the HEX codes, separated by commas. No extra text.
    """

    response = model.generate_content(prompt)
    color = response.text.strip()

    return color