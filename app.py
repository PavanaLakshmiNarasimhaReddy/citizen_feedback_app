from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import matplotlib.pyplot as plt
from textblob import TextBlob
import folium
from folium.plugins import MarkerCluster

app = Flask(__name__)

CSV_FILE = "citizen_feedback.csv"

location_coords = {
    "community center": (49.2827, -123.1207),
    "main street": (49.2636, -123.1386),
    "park": (49.2845, -123.1119),
    "library": (49.2800, -123.1150),
    "school": (49.2781, -123.1225)
}

os.makedirs("static", exist_ok=True)

def analyze_message(msg):
    msg_lower = msg.lower()
    topic = "unknown"
    if "garbage" in msg_lower or "cleaning" in msg_lower:
        topic = "sanitation"
    elif "traffic" in msg_lower:
        topic = "traffic"
    elif "music" in msg_lower or "noise" in msg_lower:
        topic = "noise"
    elif "leakage" in msg_lower or "infrastructure" in msg_lower:
        topic = "infrastructure"

    urgency = "normal"
    if "urgent" in msg_lower or "awful" in msg_lower or "please fix" in msg_lower:
        urgency = "high"

    sentiment = TextBlob(msg).sentiment.polarity
    sentiment_label = "positive" if sentiment > 0.1 else "negative" if sentiment < -0.1 else "neutral"

    location = "unspecified"
    for loc in location_coords:
        if loc in msg_lower:
            location = loc
            break

    return {
        "message": msg,
        "topic": topic,
        "urgency": urgency,
        "sentiment": sentiment_label,
        "location": location
    }

def update_dashboard(dataframe):
    plt.figure(figsize=(6,4))
    dataframe['topic'].value_counts().plot(kind='bar', color='skyblue')
    plt.title("Topic Distribution")
    plt.xlabel("Topic")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/topic_distribution.png")
    plt.close()

    plt.figure(figsize=(6,4))
    dataframe['urgency'].value_counts().plot(kind='bar', color='salmon')
    plt.title("Urgency Levels")
    plt.xlabel("Urgency")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/urgency_levels.png")
    plt.close()

    plt.figure(figsize=(6,4))
    dataframe['sentiment'].value_counts().plot(kind='bar', color='lightgreen')
    plt.title("Sentiment Analysis")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/sentiment_analysis.png")
    plt.close()

    map_center = [49.2827, -123.1207]
    feedback_map = folium.Map(location=map_center, zoom_start=13)
    marker_cluster = MarkerCluster().add_to(feedback_map)

    for _, row in dataframe.iterrows():
        loc_name = row['location']
        if loc_name in location_coords:
            lat, lon = location_coords[loc_name]
            popup_text = f"Topic: {row['topic']}<br>Urgency: {row['urgency']}<br>Sentiment: {row['sentiment']}<br>Message: {row['message']}"
            folium.Marker(location=[lat, lon], popup=popup_text).add_to(marker_cluster)

    feedback_map.save("static/citizen_feedback_map.html")

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    message = request.form['message']
    result = analyze_message(message)

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=["message", "topic", "urgency", "sentiment", "location"])

    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    update_dashboard(df)

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
