### bg_color.py
from dotenv import load_dotenv
import google.generativeai as genai
import openai
from openai import OpenAI, RateLimitError, APIError
from secret import get_secret

load_dotenv()
# gemini_api_key = get_secret("GEMINI_API_KEY")

# api_key = gemini_api_key
# genai.configure(api_key = api_key)
# model = genai.GenerativeModel(model_name = "models/gemini-2.0-flash")

openai_api_key = get_secret("OPENAI_API_KEY")

api_key = openai_api_key
client = OpenAI(api_key=openai_api_key)

def generate_color(emotion=None):
    prompt = f"""
    You are an assistant that provides a smooth gradient background color theme 
    for a web page based on the emotion "{emotion}".

    Output RULES:
    - Return EXACTLY 3 HEX color codes
    - Format: "#RRGGBB, #RRGGBB, #RRGGBB"
    - No explanations, no additional text.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate aesthetic HEX color gradients."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,  # 稍微高一點，讓顏色更有創意
        )

        colors = response.choices[0].message.content.strip()
        return colors

    except RateLimitError as e:
        print(f"[ERROR] OpenAI rate limit exceeded in generate_color: {e}")
        return "#CCCCCC, #999999, #666666"  # fallback 灰階

    except APIError as e:
        print(f"[ERROR] OpenAI API error in generate_color: {e}")
        return "#CCCCCC, #999999, #666666"

    except Exception as e:
        print(f"[ERROR] Unexpected error in generate_color: {e}")
        return "#CCCCCC, #999999, #666666"