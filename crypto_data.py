import requests
import pandas as pd


# Функция для получения данных по криптовалюте
def get_crypto_data(ticker, interval='1d', limit='6'):
    url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={limit}'
    response = requests.get(url)
    raw_data = response.json()
    df = pd.DataFrame(raw_data, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                         'quote_asset_volume', 'number_of_trades', 'last_price',
                                         'taker_buy_quote_asset_volume', 'unknown'])
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    df['open'] = pd.to_numeric(df['open'])
    df['close'] = pd.to_numeric(df['close'])
    return df

# Функция для обновления данных по криптовалюте
def update_crypto_data(ticker, crypto_data):
    crypto_data[ticker] = get_crypto_data(ticker)