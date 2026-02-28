from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import os
from api.models import StudentData, PredictionResponse

app = FastAPI(title="Student Performance Prediction API")

MODEL_PATH = "best_linear_model.pkl"
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}. Attempting to re-train...")

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(data: StudentData):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert Pydantic model to DataFrame for the scikit-learn pipeline
        input_df = pd.DataFrame([data.dict()])
        prediction = model.predict(input_df)[0]
        return PredictionResponse(prediction=float(prediction), status="success")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
