# forecast.py
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import logging

logger = logging.getLogger(__name__)

def forecast_stock_prices(df, order=(5, 1, 0), steps=10):
    """
    Performs an ARIMA forecast on the 'close' price and assigns
    a proper datetime index to the forecast.
    
    Args:
        df (DataFrame): DataFrame containing historical data with a 'close' column.
        order (tuple): ARIMA order parameters.
        steps (int): Number of future time steps to forecast.
    
    Returns:
        forecast (Series): Forecasted values with a datetime index.
    """
    try:
        # If the DataFrame still has a 'time' column, set it as index
        if "time" in df.columns:
            df.set_index("time", inplace=True)
        # At this point, the index should already be datetime from database.py
        df = df.sort_index()

        ts = df["close"]

        # Check that we have a valid last date
        last_date = ts.index[-1]
        if pd.isnull(last_date):
            raise ValueError("Last historical date is not valid. Check your timestamp conversion.")
        logger.info(f"Last historical date in data: {last_date}")

        model = ARIMA(ts, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)

        # Generate a new datetime index starting the day after the last historical date
        forecast_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=steps, freq='D')
        forecast.index = forecast_dates

        logger.info(f"Forecast starts from: {forecast.index[0]}")
        return forecast
    except Exception as e:
        logger.exception(f"Failed to forecast stock prices: {e}")
        raise
