from pymongo import MongoClient
from datetime import datetime, timezone
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import re
import dash_bootstrap_components as dbc
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

app = dash.Dash(__name__, external_stylesheets=[
        dbc.themes.CYBORG,
        "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap"
    ])
app.title = "Emotion Trend Dashboard"

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["emotion_platform"]
user_collection = db["user_inputs"]
text_feedback_collection = db["text_feedbacks"]
music_feedback_collection = db["music_feedbacks"]

def fetch_user_data():
    cursor = user_collection.find()
    data = list(cursor)
    if not data:
        return pd.DataFrame(columns=['user_id', 'text', 'timestamp'])
    df = pd.DataFrame(data)
    return df[['user_id', 'text', 'timestamp']]

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
    return df[['user_id', 'text', 'response', 'emotion', 'liked', 'timestamp']]

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
    return df[['user_id', 'recommendations', 'emotion', 'liked', 'timestamp']]

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

app.layout = dbc.Container([
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
                                    sum(1 for d in fetch_text_feedback_data().to_dict('records') if d['liked'] is True),
                                    sum(1 for d in fetch_text_feedback_data().to_dict('records') if d['liked'] is False)
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
                                    sum(1 for d in fetch_music_feedback_data().to_dict('records') if d['liked'] is True),
                                    sum(1 for d in fetch_music_feedback_data().to_dict('records') if d['liked'] is False)
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

@app.callback(
    Output('reward-output', 'children'),
    Input('feedback-slider', 'value')
)
def update_reward(value):
    return f"Simulated Reward Score: {value * 10:.1f}"

if __name__ == '__main__':
    app.run(debug=True)