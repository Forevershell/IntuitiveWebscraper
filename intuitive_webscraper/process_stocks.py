# @file process_stocks.py
# @brief Interface to communicate with the app
#
#        The interface that serves as the middleman between
#        the webscraper backend and the application

import os.path
import re
from pathlib import Path
from intuitive_webscraper.parse_tickers import getTickers
from intuitive_webscraper.parse_stocks import getTicker, getTickerCacheName
from intuitive_webscraper.cache import Cache
from intuitive_webscraper.utils import getCacheDir

# @function getStock
# @brief Adds stock/ticker to the watchlist
# @param ticker: Ticker that is being investigated
# @param exchange: Exchange of the ticker
# @return Stock Data
def getStock(ticker, exchange = None):
    return getTicker(ticker, exchange)

# @function getStocks
# @brief Gets all stocks on the watchlist, which
#        are saved in the cache files
# @return Stocks on the watchlist/ saved in the cache
def getStocks():
    stocks = []
    for root, dirs, files in os.walk(getCacheDir()):
        for f in files:
            ticker = re.search('ticker_cache_(.+?).json', f)
            if ticker:
                stocks.append(getTicker(ticker.group(1)))
    return stocks     

# @function removeStock
# @brief Removes a stock from the watchlist
# @param ticker: Ticker to be removed from watchlist 
def removeStock(ticker):
    cache = Cache(getTickerCacheName(ticker))
    cache.cacheRemove()

# @function getExchanges
# @brief Attempts to get the exchange information so users can
#        choose which exchange to browse their tickers
# @return Stock exchange list
def getExchanges():
    cache =  Cache('tickers.json')
    if cache.cacheExists():
        return list(getTickers().keys())
    else:
        raise(Exception())

# @function getTickersInExchange
# @brief Attempts to get the stock ticker information 
#        in the stock exchange
#        that is designated
# @param exchange: The stock exchange to list all tickers for
# @return Stock ticker information for the designated stock exchange
def getTickersInExchange(exchange):
    cache =  Cache('tickers.json')
    if cache.cacheExists():
        return getTickers()[exchange]
    else:
        raise(Exception())
