import pandas as pd
import requests


# global variables
api_key = "TMT13HK02BF7WA8C"
# Documentation : https://www.alphavantage.co/documentation/#dailyadj


def get_stock_data(aggregation, company):
    """
    Function used to query the Aplha Vantage API and return a dataframe of daily stock information for a given company.

    Args:
        aggregation: The level of data you want in the dataframe: eg. "TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY"
        company: The ticker name for the company

    Returns: A dataframe with the daily stock info.
    """

    url = f'https://www.alphavantage.co/query?function={aggregation}&symbol={company}&interval=5min&apikey={api_key}'

    with requests.get(url) as req:
        data = req.json()

    # Create the dataframes
    new_data = pd.DataFrame(data)
    meta_data = new_data.loc[~new_data["Meta Data"].isnull()]
    raw_data = new_data.loc[new_data["Meta Data"].isnull()].reset_index()

    cols = ["open", "high", "low", "close",
            "adjusted_close", "volume",
            "dividend_amount", "split_coef"
            ]

    # Create a dataframe from the nested dictionary
    nested = raw_data["Time Series (Daily)"].astype("string").str.split(",", expand=True)
    nested = nested.rename(columns={0: cols[0], 1: cols[1],
                                    2: cols[2], 3: cols[3],
                                    4: cols[4], 5: cols[5],
                                    6: cols[6], 7: cols[7]
                                    })

    # clean the nested dictionary to only get the relevant data
    nested["open"] = nested["open"].str.replace("{'1. open':|'", "", regex=True).astype('float')
    nested["high"] = nested["high"].str.replace("'2. high':|'", "", regex=True).astype('float')
    nested["low"] = nested["low"].str.replace("'3. low': |'", "", regex=True).astype('float')
    nested["close"] = nested["close"].str.replace("'4. close':|'", "", regex=True).astype('float')
    nested["adjusted_close"] = nested["adjusted_close"].str.replace("'5. adjusted close':|'",
                                                                    "",
                                                                    regex=True
                                                                    ).astype('float')
    nested["volume"] = nested["volume"].str.replace("'6. volume':|'",
                                                    "",
                                                    regex=True
                                                    ).astype('float')
    nested["dividend_amount"] = nested["dividend_amount"].str.replace("'7. dividend amount':|'",
                                                                      "",
                                                                      regex=True
                                                                      ).astype('float')
    nested["split_coef"] = nested["split_coef"].str.replace("'8. split coefficient':|'|}",
                                                            "",
                                                            regex=True
                                                            ).astype('float')

    # Merge the two dataframes and clean
    df = pd.merge(left=raw_data, right=nested, left_index=True, right_index=True)
    df = df.drop(["Meta Data", "Time Series (Daily)"], axis=1)
    df = df.rename(columns={"Unnamed: 0": "date", "index": "date"})
    df["date"] = df["date"]
    # df = df.set_index('date')
    df["ticker"] = company

    return df, meta_data


diageo, _ = get_stock_data("TIME_SERIES_DAILY_ADJUSTED", "DEO")
diageo.to_csv("diagio.csv")

# get_stock_data("TIME_SERIES_DAILY_ADJUSTED", "DEO").to_csv("deageo_2.csv")
