import matplotlib.pyplot as plt
import folium
from textblob import TextBlob
import pandas as pd
from folium.plugins import MarkerCluster

# Sample citizen messages
messages = [
    "There’s a huge pile of garbage near the community center. It’s been there for 3 days and smells awful!",
    "The traffic on Main Street is unbearable during rush hour. Can something be done?",
    "Great job on cleaning up the park! It looks beautiful now.",
    "Loud music from the apartment complex next to the library is disturbing the neighborhood every night.",
    "Water leakage near the school has been going on for a week. Please fix it urgently!"
]

# Location mapping for geolocation
location_coords = {
    "community center": (49.2827, -123.1207),
    "Main Street": (49.2636, -123.1386),
    "park": (49.2845, -123.1119),
    "library": (49.2800, -123.1150),
    "school": (49.2781, -123.1225)
}

# Function to analyze messages
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
    if "urgent" in msg_lower or "awful" in msg_lower:
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

# Analyze all messages
analysis_results = [analyze_message(msg) for msg in messages]
df = pd.DataFrame(analysis_results)

# Visualization: Topic Distribution
plt.figure(figsize=(6,4))
df['topic'].value_counts().plot(kind='bar', color='skyblue')
plt.title("Topic Distribution")
plt.xlabel("Topic")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("topic_distribution.png")
plt.close()

# Visualization: Urgency Levels
plt.figure(figsize=(6,4))
df['urgency'].value_counts().plot(kind='bar', color='salmon')
plt.title("Urgency Levels")
plt.xlabel("Urgency")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("urgency_levels.png")
plt.close()

# Visualization: Sentiment Analysis
plt.figure(figsize=(6,4))
df['sentiment'].value_counts().plot(kind='bar', color='lightgreen')
plt.title("Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("sentiment_analysis.png")
plt.close()

# Geolocation Mapping
map_center = [49.2827, -123.1207]
feedback_map = folium.Map(location=map_center, zoom_start=13)
marker_cluster = MarkerCluster().add_to(feedback_map)

for _, row in df.iterrows():
    loc_name = row['location']
    if loc_name in location_coords:
        lat, lon = location_coords[loc_name]
        popup_text = f"Topic: {row['topic']}<br>Urgency: {row['urgency']}<br>Sentiment: {row['sentiment']}<br>Message: {row['message']}"
        folium.Marker(location=[lat, lon], popup=popup_text).add_to(marker_cluster)

feedback_map.save("citizen_feedback_map.html")

# Save structured summary
df.to_csv("citizen_feedback_summary.csv", index=False)
