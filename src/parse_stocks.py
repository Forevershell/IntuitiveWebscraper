#Imports
import urllib.request
import bs4
import cache

URL_YAHOO = "https://finance.yahoo.com/quote/%s/history?p=%s"

def getPage(url):
    try:
        response = urllib.request.urlopen(url)
    except:
        raise Exception("")
        return None
    return bs4.BeautifulSoup(response.read(), 'html.parser')

def fix_errors(page):
    # For capturing edge cases in bs4 parser
    return page

def parseYahoo(ticker):
    page = getPage(ticker)
    fix_errors(page)
    find_params   = {'data-test': 'historical-prices'}
    table_encoded = page.find(attrs = find_params)
    header = parseHeader(table_encoded)
    stocks = parseBody(header, table_encoded)
    return stocks

def parseHeader(table):
    header_encoded = table.find('thead').find_all('th')
    header = []
    for head_encoded in header_encoded:
        header.append(head_encoded.string)
    return header

def parseBody(header, table):
    data = dict()
    body_encoded = table.find('tbody').find_all('tr')
    body = []
    for day_encoded in body_encoded:
        day_data = dict()
        day_encoded_list = day_encoded.find_all('td')
        for i in range(1, len(day_encoded_list)):
            day_data[header[i]] = day_encoded_list[i].string
        data[day_encoded_list[0].string] = day_data
    return data

def getCall(ticker, cache):
    cache = Cache(ticker + '.json')
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