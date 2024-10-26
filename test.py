import time
import ccxt
import pandas as pd

def get_upbit_data(symbol, timeframe, limit=100):
    upbit = ccxt.upbit()
    ohlcv = upbit.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def moving_average_strategy(df, short_window=5, long_window=20):
    df['short_ma'] = df['close'].rolling(window=short_window).mean()
    df['long_ma'] = df['close'].rolling(window=long_window).mean()
    if df['short_ma'].iloc[-1] > df['long_ma'].iloc[-1] and df['short_ma'].iloc[-2] <= df['long_ma'].iloc[-2]:
        return 'buy'
    elif df['short_ma'].iloc[-1] < df['long_ma'].iloc[-1] and df['short_ma'].iloc[-2] >= df['long_ma'].iloc[-2]:
        return 'sell'
    else:
        return 'hold'

def place_order(symbol, side, amount):
    try:
        upbit = ccxt.upbit({
            'apiKey': 'YOUR_API_KEY',
            'secret': 'YOUR_SECRET_KEY',
            'enableRateLimit': True,
        })
        order = upbit.create_order(symbol=symbol, type='market', side=side, amount=amount)
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    symbol = 'BTC/KRW'
    timeframe = '1h'
    amount = 0.001  # 거래할 비트코인 양

    while True:
        df = get_upbit_data(symbol, timeframe)
        action = moving_average_strategy(df)
        
        if action == 'buy':
            print("Signal: Buy")
            place_order(symbol, 'buy', amount)
        elif action == 'sell':
            print("Signal: Sell")
            place_order(symbol, 'sell', amount)
        else:
            print("Signal: Hold")

        time.sleep(60 * 60)  # 1시간 대기

if __name__ == "__main__":
    main()
