# forecast.py
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import logging

logger = logging.getLogger(__name__)

def forecast_stock_prices(df, order=(5, 1, 0), steps=10):
    """
    Performs an ARIMA forecast on the 'close' price.
    
    Args:
        df (DataFrame): DataFrame containing historical data with a 'close' column.
        order (tuple): ARIMA order parameters.
        steps (int): Number of future time steps to forecast.
    
    Returns:
        forecast (Series): Forecasted values.
    """
    try:
        if "time" in df.columns:
            df.set_index("time", inplace=True)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        ts = df["close"]
        model = ARIMA(ts, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        logger.info(f"Successfully forecasted stock prices for {steps} steps")
        return forecast
    except Exception as e:
        logger.exception(f"Failed to forecast stock prices: {e}")
        raise
