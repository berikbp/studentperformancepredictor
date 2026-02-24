# Student Performance Prediction System

A full-stack application for predicting student exam scores based on study habits, lifestyle, and environmental factors.

## 🚀 Quick Start (Docker)

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up --build
```

- **Frontend**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## 🛠️ Local Development

### Prerequisites
- Python 3.9+
- `uv` (recommended) or `pip`

### Set up
1. Install dependencies:
   ```bash
   uv sync
   ```
2. Start the Backend API:
   ```bash
   uv run uvicorn api.main:app --reload
   ```
3. Start the Streamlit Frontend:
   ```bash
   uv run streamlit run ui/app.py
   ```
