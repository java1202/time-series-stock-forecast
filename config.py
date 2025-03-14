# config.py
import os

ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "YOUR_ALPHA_VANTAGE_API_KEY")
INFLUXDB_URL = os.environ.get("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN", "YOUR_INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG", "YOUR_ORG")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET", "stock_data")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
