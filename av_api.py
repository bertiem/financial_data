import numpy as np
import pandas as pd
import requests

# global variables
api_key = "TMT13HK02BF7WA8C"
# Documentation : https://www.alphavantage.co/documentation/#dailyadj


def get_stock_data(aggregation, company):
    # "TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY"

    url = f'https://www.alphavantage.co/query?function={aggregation}&symbol={company}&interval=5min&apikey={api_key}'

    with requests.get(url) as req:
        data = req.json()

    df = pd.DataFrame(data)
    return df

print(get_stock_data("TIME_SERIES_DAILY_ADJUSTED", "DEO").head(1))
