import requests
from datetime import datetime, date
import pandas as pd


def get_current(cookies=None):
    url = 'https://ruleof40.trade/r40app/getCurrent'
    df = __get_query(url, cookies=cookies)
    if len(df) > 0:
        df = df.set_index('Ticker')
    return df

def get_hist_per_date(date:datetime, cookies=None):
    url = 'https://ruleof40.trade/r40app/getHistPerDate'
    df = __get_query(url, date=date, cookies=cookies)
    if len(df) > 0:
        df = df.set_index('Ticker')
    return df

def get_hist_per_symbol(symbol:str, cookies=None):
    url = 'https://ruleof40.trade/r40app/getHistPerSymbol'
    df = __get_query(url, symbol=symbol, cookies=cookies)
    if len(df) > 0:
        df = df.set_index('Last Update date')
    return df

def __get_query(url:str, date:datetime=None, symbol:str=None, cookies=None):
    params = None
    if date is not None:
        datestr = date.strftime('%Y-%m-%d')
        params = {'date': datestr}

    if symbol is not None:
        params = {'symbol': symbol}

    response = requests.get(url, cookies=cookies, params=params)
    df = pd.json_normalize(response.json())

    return df

if __name__ == '__main__':
    current = get_current()
    print(current[:5])

    histdate = get_hist_per_date(datetime(2021, 1, 1, 0, 0))
    print(histdate[:5])

    histsym = get_hist_per_symbol('ADBE')
    print(histsym[:5])


