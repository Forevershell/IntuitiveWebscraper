import bs4
import string
import time
import intuitive_webscraper.utils as utils
from intuitive_webscraper.cache import Cache

# imports used for multithreading
import threading
from queue import Queue
from os import cpu_count
from queue import Empty

URL_MAIN  = "http://www.eoddata.com/symbols.aspx"
URL_COMBINE = "http://www.eoddata.com/stocklist/%s/%s.htm"

def parseTickers(url):
    page = utils.getPage(url)
    utils.fixErrors(page)
    table_encoded = page.find('div', {'id' : 'ctl00_cph1_divSymbols'})
    headers = parseHeaders(table_encoded.table)
    tickers = dict()
    for entry in table_encoded.table.find_all('tr')[1::]:
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
    return None

def parseExchanges():
    page = utils.getPage(URL_MAIN)
    utils.fixErrors(page)
    headers_encoded = page.find('select', {'id' : 'ctl00_cph1_cboExchange'}).find_all('option')
    headers = dict()
    for header in headers_encoded:
        headers[header.get('value')] = header.string
    return headers

def getTickers():
    cache = Cache('tickers.json')
    if not (cache.cacheExists() and not cache.cacheExpired()):
        cache.cacheRemove()
        # Threading preparation
        # CPU count (number of threads)
        count = cpu_count()
        # Mutex for dictionary access
        lock = threading.Lock()
        # Queue to store urls
        queue_size = 0
        tickers_processed = 0

        # Default count is 4 CPUs
        if count is None:
            count = 4
        # Parsing the exchanges
        headers = parseExchanges()

        # Parses each individual stock
        def run(save):
            nonlocal queue_size, tickers_processed
            while True:
                try:
                    url = queue.get(timeout=2)
                except Empty:
                    return
                with lock:
                    tickers_processed += 1
                    print('\r[{}/{}] Parsing: {}'.format(
                tickers_processed, queue_size, url), end="")
                try:
                    tickers = parseTickers(url)
                except:
                    tickers = dict()
                with lock:
                    save.update(tickers)
                # Indicate to queue that task is done
                queue.task_done()

        # Starting to parse the final results
        tickers = dict()
        print("running on " + str(count) + " threads")
        # For each exchange
        for header in headers:
            header_tickers = dict()
            queue = Queue()
            # For each letter of the alphabet
            for alpha in string.ascii_uppercase:
                url = URL_COMBINE % (header, alpha)
                queue.put(url)
            queue_size += queue.qsize()
            # Run multithreading on the stock lists
            for _ in range(count):
                thread = threading.Thread(target=run, args=(header_tickers,))
                thread.setDaemon(True)
                thread.start()
            # Block process until all threads are joined
            queue.join()
            tickers[header] = header_tickers
        # Cache the results from tickers
        cache.toCache(tickers)
    return cache.fromCache()