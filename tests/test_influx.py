# test_influx.py
import os
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read credentials from environment variables
url = os.environ.get("INFLUXDB_URL", "http://localhost:8086")
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")

try:
    # Create the InfluxDB client
    client = InfluxDBClient(url=url, token=token, org=org)
    # Ping the server to check the connection
    health = client.health()
    print("InfluxDB Health:", health)
except Exception as e:
    print("Error connecting to InfluxDB:", e)
