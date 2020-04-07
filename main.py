import alpaca_trade_api as tradeapi
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import time, os

# initiate keys
ALPACA_API_KEY = os.path.expandvars('$ALPACA_API_KEY')
ALPACA_API_SECRET_KEY = os.path.expandvars('$ALPACA_API_SECRET_KEY')
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"
ALPHA_VANTAGE_KEY = os.path.expandvars('$ALPHA_VANTAGE_KEY')

print(ALPACA_API_KEY)
print(ALPACA_API_SECRET_KEY)

# connect to alpaca
alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET_KEY, ALPACA_API_BASE_URL, api_version='v2')
account = alpaca.get_account()

# initiate tech indicator and time series
ti = TechIndicators(key=ALPHA_VANTAGE_KEY, output_format='pandas')
ts = TimeSeries(ALPHA_VANTAGE_KEY, output_format='pandas')

while(True):
    current_sma = ti.get_sma('AAPL', interval='1min', time_period=30)[0].tail(2)['SMA'][1]
    last_sma = ti.get_sma('AAPL', interval='1min', time_period=30)[0].tail(2)['SMA'][0]
    price = ts.get_intraday(symbol='AAPL', interval='1min')[0].tail(1)['4. close'][0]

    print(price)

    # buy signal, price breaks through SMA from below
    if price > current_sma and price < last_sma:
        alpaca.submit_order('AAPL', 1, 'buy', 'market', 'day')
    # sell signal, price breaks through SMA from above
    elif price < current_sma and price > last_sma:
        alpaca.submit_order('AAPL', 1, 'sell', 'market', 'day')

    time.sleep(60)
