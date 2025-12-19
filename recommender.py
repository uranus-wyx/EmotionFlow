### recommender.py
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

def generate_music_recommendation(user_input, emotion):
    """
    Recommend a therapeutic music track based on user's input and emotion.
    Uses OpenAI gpt-4o-mini.
    """

    system_prompt = """
    You are a music therapist AI who recommends songs based on emotional tone.
    Your music knowledge spans pop, indie, R&B, classical, and global music.
    You choose songs that create emotional resonance, validation, or comfort.

    Rules:
    - Respond ONLY in the required format.
    - Must recommend real songs.
    - Keep the explanation short (1–2 sentences).
    """

    user_prompt = f"""
    User emotion: {emotion}
    User input: "{user_input}"

    Please respond **exactly** in this format:

    Song: <song name>
    Artist: <artist>
    Reason: <short emotional reason>
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,  # 少許創意，音樂建議更貼近情緒
        )

        output = response.choices[0].message.content.strip()
        return output

    except RateLimitError as e:
        print(f"[ERROR] OpenAI rate limit exceeded in music: {e}")
        return (
            "Song: Weightless\n"
            "Artist: Marconi Union\n"
            "Reason: I'm temporarily unable to generate new suggestions, "
            "but this track is scientifically known to reduce stress."
        )

    except APIError as e:
        print(f"[ERROR] OpenAI API error in music: {e}")
        return (
            "Song: Clair de Lune\n"
            "Artist: Claude Debussy\n"
            "Reason: A calming fallback recommendation while I'm having trouble responding."
        )

    except Exception as e:
        print(f"[ERROR] Unexpected error in generate_music_recommendation: {e}")
        return (
            "Song: River Flows in You\n"
            "Artist: Yiruma\n"
            "Reason: A gentle fallback choice to help you relax."
        )