#Imports
import urllib.request
import bs4
from cache import Cache
import string

URL_MAIN  = "http://www.eoddata.com/symbols.aspx"
URL_COMBINE = "http://www.eoddata.com/stocklist/%s/%s.htm"

def getPage(url):
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        response = opener.open(url)
    except:
        print(url)
        return None
    return bs4.BeautifulSoup(response.read(), 'html.parser')

def fix_errors(page):
    # For capturing edge cases in bs4 parser
    return page

def parseTickers(url):
    page = getPage(url)
    if page != None:
        fix_errors(page)
        table_encoded = page.find('div', {'id' : 'ctl00_cph1_divSymbols'}).table
        headers = parseHeaders(table_encoded)
        tickers = dict()
        for entry in table_encoded.find_all('tr')[1::]:
            ticker_data = entry.find_all('td')
            tickers[ticker_data[headers['Code']].string] = ticker_data[headers['Name']].string
        return tickers

def parseHeaders(table):
    if table:
        headers = dict()
        i = 0
        for head in table.find('tr').find_all('th'):
            headers[head.string] = i
            i += 1
        return headers
    

def parseExchanges():
    page = getPage(URL_MAIN)
    if page != None:
        headers_encoded = page.find('select', {'id' : 'ctl00_cph1_cboExchange'}).find_all('option')
        headers = dict()
        for header in headers_encoded:
            headers[header.get('value')] = header.string
        return headers

def getTickers():
    cache = Cache('tickers.json')
    if not (cache.cacheExists() and not cache.cacheExpired()):
        print("hi")
        headers = parseExchanges()
        tickers = dict()
        for header in headers:
            header_tickers = dict()
            for alpha in string.ascii_uppercase:
                url = URL_COMBINE % (header, alpha)
                header_tickers.update(parseTickers(url))
            tickers[header] = header_tickers
        cache.toCache(tickers)
    return cache.fromCache()

getTickers()