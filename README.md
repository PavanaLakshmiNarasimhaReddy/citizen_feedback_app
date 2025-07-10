# 🏙️ Citizen Feedback Dashboard

A Flask-based web application that allows citizens to submit feedback about community issues and visualizes the data in real-time using charts and an interactive map.

---

## 📌 Features

- Submit feedback via a simple web form
- Automatically analyzes:
  - **Topic** (e.g., sanitation, traffic, noise)
  - **Urgency** (normal or high)
  - **Sentiment** (positive, neutral, negative)
  - **Location** (based on known landmarks)
- Real-time dashboard with:
  - Topic distribution chart
  - Urgency level chart
  - Sentiment analysis chart
  - Interactive map with feedback markers
- Stores all feedback in a CSV file

---

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/citizen-feedback-dashboard.git
   cd citizen-feedback-dashboard
   ```
