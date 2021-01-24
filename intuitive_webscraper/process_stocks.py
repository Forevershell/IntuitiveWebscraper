import os.path
import re
from pathlib import Path
from intuitive_webscraper.parse_tickers import getTickers
from intuitive_webscraper.parse_stocks import getTicker, getTickerCacheName
from intuitive_webscraper.cache import Cache
from intuitive_webscraper.utils import getCacheDir

def getStock(ticker, exchange = None):
    return getTicker(ticker, exchange)

def getStocks():
    stocks = []
    for root, dirs, files in os.walk(getCacheDir()):
        for f in files:
            ticker = re.search('ticker_cache_(.+?).json', f)
            if ticker:
                stocks.append(getTicker(ticker.group(1)))
    return stocks     

def removeStock(ticker):
    cache = Cache(getTickerCacheName(ticker))
    cache.cacheRemove()

def getExchanges():
    cache =  Cache('tickers.json')
    if cache.cacheExists():
        return list(getTickers().keys())
    else:
        raise(Exception())

def getTickersInExchange(exchange):
    cache =  Cache('tickers.json')
    if cache.cacheExists():
        return getTickers()[exchange]
    else:
        raise(Exception())
