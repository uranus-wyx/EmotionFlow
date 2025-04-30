### app.py
from datetime import datetime, timezone
import uuid
import json
import urllib.parse
import os
from flask import Flask, render_template, request, jsonify, session
from pymongo import MongoClient
from classifier import classify_emotion_gemini
from responder import generate_response_gemini
from recommender import generate_music_recommendation
from bg_color import generate_color
from dashboard import create_dashboard
from secret import get_secret

app = Flask(__name__)
app.secret_key = "super-secret-key-12345"

# GEMINI_API_KEY = "AIzaSyBpFbBbEwSA7H0up-Hoa9ky9sLWWn6NmAU"
# MONGODB_URI = "mongodb+srv://yuniwu:NpCOR24HEnxdnVpX@cluster0.sdsbxna.mongodb.net/"

mongo_uri = get_secret("MONGODB_URI")
# mongo_uri = MONGODB_URI

mongo_client = MongoClient(mongo_uri)
db = mongo_client["emotion_platform"]
collection = db["user_inputs"]
text_feedback_collection = db["text_feedbacks"]
music_feedback_collection = db["music_feedbacks"]

dash_app = create_dashboard(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    user_input = data["user_input"]
    user_id = data.get("user_id") or session.get("user_id", "anonymous")
    collection.insert_one({
        "user_id": user_id,
        "text": user_input,
        "timestamp": datetime.now(timezone.utc)
    })
    ai_reply = generate_response_gemini(user_input)
    return jsonify({"ai_response": ai_reply})

@app.route("/predict", methods=["POST"])
def predict_emotions():
    data = request.get_json()
    user_input = data.get("text")
    if not user_input:
        return jsonify({"error": "Missing 'text' in request body"}), 400
    result = classify_emotion_gemini(user_input)
    return jsonify(result)

@app.route("/api/respond", methods=["POST"])
def generate_response():
    data = request.get_json()
    text = data.get("text", "")
    emotion = data.get("emotion") 
    reply = generate_response_gemini(text, emotion)
    return jsonify({"response": reply})

@app.route("/api/music", methods=["POST"])
def recommend_music():
    data = request.json
    user_input = data["text"]
    emotion = data["emotion"]
    music = generate_music_recommendation(user_input, emotion)
    lines = music.split("\n")
    song = lines[0].replace("Song: ", "").strip()
    artist = lines[1].replace("Artist: ", "").strip()
    reason = lines[2].replace("Reason: ", "").strip()
    youtube_url = get_youtube_search_url(song, artist)
    recommendation = (
        f"{song} - {artist}<br>"
        f"{reason}<br>"
        f"🔗 <a href='{youtube_url}' target='_blank'>Watch on YouTube</a>"
    )
    return jsonify({"recommendation": recommendation})

def get_youtube_search_url(song, artist):
    query = urllib.parse.quote(f"{song} {artist}")
    return f"https://www.youtube.com/results?search_query={query}"

@app.route("/api/color", methods=["POST"])
def get_emotion_color():
    data = request.get_json()
    emotion = data.get("emotion", "neutral")
    color = generate_color(emotion)
    return jsonify({"color": color})

@app.route("/anonymous-login", methods=["POST"])
def anonymous_login():
    user_id = str(uuid.uuid4())[:8]
    session["user_id"] = user_id
    session["anonymous"] = True
    return jsonify({"status": "ok", "user_id": user_id})

@app.route("/text_feedback", methods=["POST"])
def text_save_feedback():
    data = request.json
    text_feedback_collection.insert_one({
        "user_id": data.get("user_id", "anonymous"),
        "text_feedback": {
            "text": data.get("text_feedback_text"),
            "response": data.get("text_feedback_response"),
            "emotion": data.get("text_feedback_emotion"),
            "liked": data.get("text_feedback_liked")
        },
        "timestamp": datetime.now(timezone.utc)
    })
    return {"status": "ok"}, 200

@app.route("/music_feedback", methods=["POST"])
def music_save_feedback():
    data = request.json
    music_feedback_collection.insert_one({
        "user_id": data.get("user_id", "anonymous"),
        "music_feedback": {
            "recommendations": data.get("music_recommendations"),
            "emotion": data.get("music_emotion"),
            "liked": data.get("music_liked")
        },
        "timestamp": datetime.now(timezone.utc)
    })
    return {"status": "ok"}, 200

@app.route("/callback")
def callback():
    code = request.args.get('code')
    return f"Authorization code received: {code}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    # app.run(debug=True)
