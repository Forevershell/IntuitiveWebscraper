# @file parse_stocks.py
# @brief Parses individual ticker symbols
#
#        Parsing functions that retrieves html from public
#        webites(yahoo or eodata), and attempts to parse
#        information about the stock (open, close, high, low, volume)
#
#        The information is then cached using the Cache

import bs4
import re
import intuitive_webscraper.utils as utils
from intuitive_webscraper.cache import Cache

# Global URLs that are scraped
URL_YAHOO = "https://finance.yahoo.com/quote/%s/history?p=%s"
URL_EODATA = "http://www.eoddata.com/stockquote/%s/%s.htm"

# @function parseYahoo
# @brief Parses ticker data from Yahoo
def parseYahoo(url):
    page = utils.getPage(url)
    utils.fixErrors(page)
    find_params   = {'data-test': 'historical-prices'}
    try:
        table_encoded = page.find(attrs = find_params)
        header = parseHeaderYahoo(table_encoded)
        stocks = parseBodyYahoo(header, table_encoded)
    except:
        raise Exception("Ticker isn't valid")
    return stocks

# @function parseHeaderYahoo
# @brief Parses ticker data headers from Yahoo
def parseHeaderYahoo(table):
    header_encoded = table.find('thead').find_all('th')
    header = []
    for head_encoded in header_encoded:
        header.append(head_encoded.string)
    return header

# @function parseBodyYahoo
# @brief Parses ticker data body from Yahoo
def parseBodyYahoo(header, table):
    data = dict()
    body_encoded = table.find('tbody').find('tr')
    body = []
    day_data = dict()
    day_encoded = body_encoded.find_all('td')
    for i in range(1, len(day_encoded)):
        day_data[header[i]] = day_encoded[i].string
    return day_data

# @function parseEOData
# @brief Parses ticker data from EOData
def parseEOData(url):
    page = utils.getPage(url)
    utils.fixErrors(page)
    try:
        table_encoded = page.find('div', {'id' : 'ctl00_cph1_divHistory'}).table
        header = parseHeaderEOData(table_encoded)
        stocks = parseBodyEOData(header, table_encoded)
    except:
        raise Exception("Ticker isn't valid")
    return stocks

# @function parseHeaderEOData
# @brief Parses ticker data headers from EOData
def parseHeaderEOData(table):
    header_encoded = table.find_all('th')
    header = []
    for head_encoded in header_encoded:
        header.append(head_encoded.string)
    return header

# @function parseBodyEOData
# @brief Parses ticker data body from EOData
def parseBodyEOData(header, table):
    data = dict()
    body_encoded = table.find_all('tr')[1]
    body = []
    day_data = dict()
    day_encoded = body_encoded.find_all('td')
    for i in range(1, len(day_encoded)):
        day_data[header[i]] = day_encoded[i].string
    return day_data

# All available getter methods for getting specific tickers

# @function getTickerYahoo
# @brief Get ticker data from Yahoo
def getTickerYahoo(ticker):
    url = URL_YAHOO % (ticker, ticker)
    return parseYahoo(url)

# @function getTickerEOData
# @brief Get ticker data from EOData
def getTickerEOData(ticker, market):
    url = URL_EODATA % (market, ticker)
    return parseEOData(url)

# @function getTickerCacheName
# @brief Get ticker cache file name
def getTickerCacheName(ticker):
    return 'ticker_cache_' + ticker + '.json'

# @function getTicker
# @brief Gets ticker data in a unified format and caches if needed
# @param ticker: Ticker symbol
# @param market: Exchange abbreviation that represents
#                the exchange the ticker is traded in
# @return Updated ticker data
def getTicker(ticker, market = None):
    cache = Cache(getTickerCacheName(ticker))
    if not (cache.cacheExists() and not cache.cacheExpired()):
        if market != None:
            data = getTickerEOData(ticker, market)
        else:
            data = getTickerYahoo(ticker)
        result = dict()
        result['name'] = ticker
        for key in data:
            if re.match('(open)(?! )', key.lower().strip()):
                result['open'] = data[key]
            if re.match('(high)(?! )', key.lower().strip()):
                result['high'] = data[key]
            if re.match('(low)(?! )', key.lower().strip()):
                result['low'] = data[key]
            if re.match('(close)(?! )', key.lower().strip()):
                result['close'] = data[key]
            if re.match('(volume)(?! )', key.lower().strip()):
                result['volume'] = data[key]
        cache.toCache(result)
    return cache.fromCache()