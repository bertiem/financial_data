import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def import_stock_historics(ticker):
    """
    Imports a dataframe of the historic data for the given company.
    
    ARGS:
    ticker: the companys ticker name
    """
    df = yf.Ticker(ticker).history(period="max")
    return df

diagio = import_stock_historics("DEO")
df = diagio[diagio.index.year > 2018]

plt.plot(df.index.month, df.Close, color="purple", label="Close")
plt.xlabel("date")
plt.ylabel("close")
plt.title("Diagio - Close Prices")
plt.show()
