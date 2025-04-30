### dashboard.py
from collections import Counter
import re
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from pymongo import MongoClient
from secret import get_secret

mongo_uri = get_secret("MONGODB_URI")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["emotion_platform"]
text_feedback_collection = db["text_feedbacks"]
music_feedback_collection = db["music_feedbacks"]

def fetch_text_feedback_data():
    cursor = text_feedback_collection.find()
    data = list(cursor)
    if not data:
        return pd.DataFrame(columns=['user_id', 'text', 'response', 'emotion', 'liked', 'timestamp'])

    processed_data = [{
        'user_id': d['user_id'],
        'text': d['text_feedback']['text'],
        'response': d['text_feedback']['response'],
        'emotion': d['text_feedback']['emotion'],
        'liked': d['text_feedback']['liked'],
        'timestamp': d['timestamp']
    } for d in data]

    df = pd.DataFrame(processed_data)
    return df

def fetch_music_feedback_data():
    cursor = music_feedback_collection.find()
    data = list(cursor)
    if not data:
        return pd.DataFrame(columns=['user_id', 'recommendations', 'emotion', 'liked', 'timestamp'])

    processed_data = [{
        'user_id': d['user_id'],
        'recommendations': d['music_feedback']['recommendations'],
        'emotion': d['music_feedback']['emotion'],
        'liked': d['music_feedback']['liked'],
        'timestamp': d['timestamp']
    } for d in data]

    df = pd.DataFrame(processed_data)
    return df

def fetch_emotion_distribution():
    cursor = text_feedback_collection.find()
    emotions = [
        re.sub(r'[^a-zA-Z\s]', '', d['text_feedback']['emotion']).strip()
        for d in cursor if 'text_feedback' in d and 'emotion' in d['text_feedback']
    ]
    emotion_counts = Counter(emotions)
    return dict(emotion_counts)

def generate_color_palette(emotions):
    cmap = plt.get_cmap("tab20")
    return {emotion: f"rgb{tuple([int(c*255) for c in cmap(i % 20)[:3]])}" for i, emotion in enumerate(emotions)}

emotion_counts = fetch_text_feedback_data()['emotion'].value_counts().to_dict()
emotion_color_map = generate_color_palette(list(emotion_counts.keys()))

def create_dashboard(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        routes_pathname_prefix="/dashboard/",
        external_stylesheets=[
            dbc.themes.CYBORG,
            "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap"
        ]
    )

    dash_app.title = "Emotion Trend Dashboard"

    text_feedback_df = fetch_text_feedback_data()
    music_feedback_df = fetch_music_feedback_data()

    dash_app.layout = dbc.Container([
        html.H1("Dashboard", className="my-4 text-center", style={"color": "#00e3ff"}),
        html.H2("RLHF Feedback Dashboard", className="my-4 text-center", style={"color": "#38f9d7"}),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("Text Feedback Summary", style={"color": "#a1ffe7"}),
                    dcc.Graph(
                        id='text-feedback-summary',
                        figure={
                            'data': [
                                go.Bar(
                                    x=['👍 Liked', '👎 Disliked'],
                                    y=[
                                        sum(1 for d in text_feedback_df.to_dict('records') if d['liked'] is True),
                                        sum(1 for d in text_feedback_df.to_dict('records') if d['liked'] is False)
                                    ],
                                    marker_color=['#00ffc6', '#ff5e78']
                                )
                            ],
                            'layout': go.Layout(
                                title='Text Feedback Summary',
                                plot_bgcolor='#1e1e2f',
                                paper_bgcolor='#1e1e2f',
                                font={"color": "#e0e0e0", "family": "Orbitron"}
                            )
                        }
                    )
                ], className="p-3 shadow rounded bg-dark")
            ], md=6),

            dbc.Col([
                html.Div([
                    html.H4("Music Feedback Summary", style={"color": "#a1ffe7"}),
                    dcc.Graph(
                        id='music-feedback-summary',
                        figure={
                            'data': [
                                go.Bar(
                                    x=['👍 Liked', '👎 Disliked'],
                                    y=[
                                        sum(1 for d in music_feedback_df.to_dict('records') if d['liked'] is True),
                                        sum(1 for d in music_feedback_df.to_dict('records') if d['liked'] is False)
                                    ],
                                    marker_color=['#b0ff8e', '#ffa474']
                                )
                            ],
                            'layout': go.Layout(
                                title='Music Feedback Summary',
                                plot_bgcolor='#1e1e2f',
                                paper_bgcolor='#1e1e2f',
                                font={"color": "#e0e0e0", "family": "Orbitron"}
                            )
                        }
                    )
                ], className="p-3 shadow rounded bg-dark")
            ], md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                html.H4("Emotion Distribution", style={"color": "#00e3ff"}),
                dcc.Graph(
                    id='emotion-distribution',
                    figure={
                        'data': [
                            go.Bar(
                                x=list(fetch_emotion_distribution().keys()),
                                y=list(fetch_emotion_distribution().values()),
                                marker_color=[emotion_color_map.get(emotion, 'gray') for emotion in emotion_counts.keys()]
                            )
                        ],
                        'layout': go.Layout(
                            title='Detected Emotion Frequency',
                            xaxis={'title': 'Emotion'},
                            yaxis={'title': 'Count'},
                            plot_bgcolor='#1e1e2f',
                            paper_bgcolor='#1e1e2f',
                            font={"color": "#e0e0e0", "family": "Orbitron"}
                        )
                    }
                )
            ], md=12)
        ]),

        html.Hr(),

        html.Div([
            html.H4("Reward Score Simulation", className="text-warning"),
            html.P("Use the slider below to simulate a reward score based on feedback intensity."),
            dcc.Slider(
                id='feedback-slider',
                min=0,
                max=10,
                step=1,
                value=5,
                marks={i: str(i) for i in range(11)}
            ),
            html.Div(id='reward-output', className='mt-3 lead text-center', style={"color": "#fcd34d", "fontFamily": "Orbitron"})
        ], className="p-4 bg-dark rounded shadow-sm")

    ], fluid=True, style={
        'backgroundColor': '#121212',
        'fontFamily': "Orbitron, sans-serif",
        'paddingTop': '0px',
        'paddingBottom': '0px',
        'margin': '0px'
    })

    return dash_app
