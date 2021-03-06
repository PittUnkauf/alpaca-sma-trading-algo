import alpaca_trade_api as tradeapi
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time, os

# initiate keys
ALPACA_API_KEY = os.path.expandvars('$ALPACA_API_KEY')
ALPACA_API_SECRET_KEY = os.path.expandvars('$ALPACA_API_SECRET_KEY')
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"
ALPHA_VANTAGE_KEY = os.path.expandvars('$ALPHA_VANTAGE_KEY')

# connect to alpaca
alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET_KEY, ALPACA_API_BASE_URL, api_version='v2')
account = alpaca.get_account()

# initiate tech indicator and time series
ti = TechIndicators(key=ALPHA_VANTAGE_KEY, output_format='pandas')
ts = TimeSeries(ALPHA_VANTAGE_KEY, output_format='pandas')

while(True):
    sma = ti.get_sma(symbol='IBM', interval='1min', time_period=30)[0].tail(2)['SMA']
    current_sma = sma[1]
    last_sma = sma[0]

    price = ts.get_intraday(symbol='IBM', interval='1min')[0].tail(2)['4. close']
    current_price = price[1]
    last_price = price[0]

    try:
        position = int(alpaca.get_position('IBM').qty)
    except:
        position = 0

    # buy signal, price breaks through SMA from below
    if current_price > current_sma and last_price < last_sma and position == 0:
        alpaca.submit_order('IBM', 100, 'buy', 'market', 'day')
        print("buy")
    # sell signal, price breaks through SMA from above
    elif current_price < current_sma and last_price > last_sma and position != 0:
        alpaca.submit_order('IBM', 100, 'sell', 'market', 'day')
        print("sell")
    else:
        print("no signal")

    time.sleep(60)
