### dashboard.py
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from pymongo import MongoClient
import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt

def fetch_text_feedback_data():
    mongo_client = MongoClient("mongodb+srv://yuniwu:NpCOR24HEnxdnVpX@cluster0.sdsbxna.mongodb.net/")
    db = mongo_client["emotion_platform"]
    text_feedback_collection = db["text_feedbacks"]
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
    mongo_client = MongoClient("mongodb+srv://yuniwu:NpCOR24HEnxdnVpX@cluster0.sdsbxna.mongodb.net/")
    db = mongo_client["emotion_platform"]
    music_feedback_collection = db["music_feedbacks"]
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
                                        text_feedback_df['liked'].sum(),
                                        (~text_feedback_df['liked']).sum()
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
                                        music_feedback_df['liked'].sum(),
                                        (~music_feedback_df['liked']).sum()
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
        ]),
    ], fluid=True)

    return dash_app
