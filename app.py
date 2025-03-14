# app.py
from flask import Flask, request, render_template, jsonify
import pandas as pd
import plotly
import plotly.graph_objs as go
import json
import logging
from data_collector import fetch_stock_data
from database import write_stock_data, query_stock_data
from forecast import forecast_stock_prices
from config import LOG_LEVEL
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch():
    symbol = request.form.get('symbol')
    if not symbol:
        return jsonify({"status": "error", "message": "No stock symbol provided"}), 400
    try:
        df = fetch_stock_data(symbol)
        write_stock_data(symbol, df)
        return jsonify({"status": "success", "message": f"Data for {symbol} fetched and stored."})
    except Exception as e:
        logger.exception(f"Error in /fetch endpoint for symbol {symbol}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/history', methods=['GET'])
def history():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"status": "error", "message": "No stock symbol provided"}), 400
    try:
        df = query_stock_data(symbol)
        data = df.to_dict(orient='records')
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        logger.exception(f"Error in /history endpoint for symbol {symbol}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/forecast', methods=['GET'])
def forecast():
    symbol = request.args.get('symbol')
    steps = int(request.args.get('steps', 10))
    if not symbol:
        return jsonify({"status": "error", "message": "No stock symbol provided"}), 400
    try:
        df = query_stock_data(symbol)
        if 'close' not in df.columns:
            return jsonify({"status": "error", "message": "Historical data not found or missing 'close' field."}), 500
        forecast_values = forecast_stock_prices(df, steps=steps)
        forecast_dict = forecast_values.to_dict()
        return jsonify({"status": "success", "forecast": forecast_dict})
    except Exception as e:
        logger.exception(f"Error in /forecast endpoint for symbol {symbol}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/visualize', methods=['GET'])
def visualize():
    """
    Visualizes historical stock data using Plotly.
    Expects query parameter: symbol=<stock symbol>
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"status": "error", "message": "No stock symbol provided"}), 400
    try:
        df = query_stock_data(symbol)
        trace = go.Scatter(x=df.index, y=df["close"], mode='lines', name='Close Price')
        layout = go.Layout(title=f"Historical Close Prices for {symbol}",
                           xaxis=dict(title='Date'),
                           yaxis=dict(title='Close Price'))
        fig = go.Figure(data=[trace], layout=layout)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('visualize.html', graphJSON=graphJSON, symbol=symbol)
    except Exception as e:
        logger.exception(f"Error in /visualize endpoint for symbol {symbol}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
