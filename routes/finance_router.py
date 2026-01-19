from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from models.finance_model import FinancialReport, SentimentData, ForecastData
from db.connection import reports_collection, forecasts_collection,sentiment_collection
from datetime import datetime
import pandas as pd

router = APIRouter(tags=["Finance"])

# -------------------------------
# 1️⃣ Save Financial Report
# -------------------------------
@router.post("/save_report")
def save_report(report: FinancialReport):
    """Save or upload a financial report for a user"""
    existing = reports_collection.find_one({
        "email": report.email,
        "report_name": report.report_name
    })

    if existing:
        raise HTTPException(status_code=400, detail="Report already exists with this name")

    new_report = {
        "email": report.email,
        "report_name": report.report_name,
        "summary": report.summary,
        "timestamp": datetime.utcnow().isoformat()
    }

    reports_collection.insert_one(jsonable_encoder(new_report))
    return {"message": "Report saved successfully"}


# -------------------------------
# 2️⃣ Get All Reports by User
# -------------------------------
@router.get("/get_reports/{email}")
def get_reports(email: str):
    """Fetch all reports uploaded by a specific user"""
    reports = list(reports_collection.find({"email": email}, {"_id": 0}))

    for r in reports:
        if "timestamp" in r and not isinstance(r["timestamp"], str):
            r["timestamp"] = str(r["timestamp"])

    return {"reports": jsonable_encoder(reports)}


# -------------------------------
# 3️⃣ Get a Specific Report
# -------------------------------
@router.get("/get_report/{email}/{report_name}")
def get_report(email: str, report_name: str):
    """Fetch a specific report by name for a user"""
    report = reports_collection.find_one(
        {"email": email, "report_name": report_name},
        {"_id": 0}
    )

    if not report:
        raise HTTPException(status_code=404, detail="No report found")

    if "timestamp" in report and not isinstance(report["timestamp"], str):
        report["timestamp"] = str(report["timestamp"])

    return {"report": jsonable_encoder(report)}


# -------------------------------
# 4️⃣ Save Market Forecast
# -------------------------------
@router.post("/save_forecast")
def save_forecast(data: dict):
    try:
        # Extract data
        user_email = data.get("user_email")
        ticker = data.get("ticker")
        forecast_period_days = data.get("forecast_period_days")
        predictions = data.get("predictions", [])

        if not user_email or not ticker or not predictions:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Convert timestamps to strings if needed
        for p in predictions:
            if not isinstance(p["date"], str):
                p["date"] = str(p["date"])

        # Create forecast document
        forecast_doc = {
            "user_email": user_email,
            "ticker": ticker,
            "timestamp": datetime.utcnow().isoformat(),
            "forecast_period_days": forecast_period_days,
            "predictions": predictions
        }

        # ✅ Synchronous insert (no await)
        result = forecasts_collection.insert_one(forecast_doc)

        return {"message": "Forecast saved successfully!", "id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving forecast: {str(e)}")

# -------------------------------
# 5️⃣ Get User Forecasts
# -------------------------------
@router.get("/get_forecasts/{email}")
def get_forecasts(email: str):
    """Fetch all saved forecasts by user"""
    forecasts = list(forecasts_collection.find({"email": email}, {"_id": 0}))

    for f in forecasts:
        if "timestamp" in f and not isinstance(f["timestamp"], str):
            f["timestamp"] = str(f["timestamp"])

    return {"forecasts": jsonable_encoder(forecasts)}

# -------------------------------
# 6️⃣ Save Sentiment Data 🧠
# -------------------------------
@router.post("/save_sentiment")
def save_sentiment(data: SentimentData):
    try:
        sentiment_entry = {
            "email": data.email,
            "text": data.text,
            "sentiment": data.sentiment,
            "confidence": data.confidence,
            "timestamp": datetime.utcnow().isoformat()
        }
        sentiment_collection.insert_one(sentiment_entry)
        return {"message": "Sentiment data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving sentiment: {e}")
