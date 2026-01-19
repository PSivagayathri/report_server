from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["financial_analysis_db"]
users_collection = db["users"]
reports_collection = db["financial_reports"]
sentiment_collection = db["sentiments"]
forecasts_collection = db["forecasts"]
