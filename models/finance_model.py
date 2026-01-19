from pydantic import BaseModel
from typing import List, Dict, Any

# -------------------------------
# 1️⃣ Financial Report Model
# -------------------------------
class FinancialReport(BaseModel):
    email: str
    report_name: str
    summary: str


# -------------------------------
# 2️⃣ Sentiment Model
# -------------------------------
class SentimentData(BaseModel):
    email: str
    text: str
    sentiment: str
    confidence: float


# -------------------------------
# 3️⃣ Forecast Model
# -------------------------------
class ForecastData(BaseModel):
    email: str
    ticker: str
    forecast_period_days: int
    predictions: List[Dict[str, Any]]  # e.g., [{"date": "2025-11-01", "predicted_price": 178.45}]
