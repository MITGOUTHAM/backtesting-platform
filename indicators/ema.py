import pandas as pd

def calculate_ema(series: pd.Series, period: int = 20) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()
