# @file parse_tickers.py
# @brief Parses all ticker symbols
#
#        Parsing functions that retrieves html from public
#        webites(eodata), and attempts to parse
#        all ticker information(ticker and their
#        corresponding name)
#
#        The information is then cached using the Cache

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

# Global URLs that are scraped
URL_MAIN  = "http://www.eoddata.com/symbols.aspx"
URL_COMBINE = "http://www.eoddata.com/stocklist/%s/%s.htm"

# @function parseTickers
# @brief Parses entire ticker to company name data from URL
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

# @function parseHeaders
# @brief Parses headers for the ticker data parsed
def parseHeaders(table):
    if table:
        headers = dict()
        i = 0
        for head in table.find('tr').find_all('th'):
            headers[head.string] = i
            i += 1
        return headers
    return None

# @function parseExchanges
# @brief Parses all the exchange headers and their abbreviations
def parseExchanges():
    page = utils.getPage(URL_MAIN)
    utils.fixErrors(page)
    headers_encoded = page.find('select', {'id' : 'ctl00_cph1_cboExchange'}).find_all('option')
    headers = dict()
    for header in headers_encoded:
        headers[header.get('value')] = header.string
    return headers

# @function getTickers
# @brief A slow function that gets entire ticker to company name data
#        Will update the cache and store in cache when necessary
#        Multithreads based on system as loading from URL is an expensive process
#        Runs in the background while main app runs in the foreground
# @return An aggregate ticker to company name data
def getTickers():
    cache = Cache('tickers.json')
    if not (cache.cacheExists() and not cache.cacheExpired()):
        # Removes the cache file when update is necessary
        cache.cacheRemove()
        # Threading preparation
        # CPU count (number of threads)
        count = cpu_count() - 4
        # Default count is 4 CPUs
        if count is None or count < 4:
            count = 4
        # Mutex for dictionary access
        lock = threading.Lock()
        # Initiating queue_size to keep track of processed tickers
        queue_size = 0
        tickers_processed = 0
        # Parsing the exchanges
        headers = parseExchanges()

        # Parses and stores each individual alphabet for an exchange
        # @param: save is the data that is to be updated in place (save is a dictionary)
        def run(save):
            nonlocal queue_size, tickers_processed
            while True:
                try:
                    url = queue.get(timeout=2)
                except Empty:
                    return
                with lock:
                    tickers_processed += 1
                # Prints output on the progress
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

        # Parse each exchange and each alphabet
        tickers = dict()
        print("running on " + str(count) + " threads")
        # For each exchange
        for header in headers:
            header_tickers = dict()
            queue = Queue()
            # For each letter of the alphabet
            for alpha in string.ascii_uppercase:
                # Generate the URL that is to be parsed
                url = URL_COMBINE % (header, alpha)
                # Dump to the queue so the url can be processed
                queue.put(url)
            queue_size += queue.qsize()
            # Run multithreading on the ticker lists
            for _ in range(count):
                thread = threading.Thread(target=run, args=(header_tickers,))
                thread.setDaemon(True)
                thread.start()
            # Block progress until all tickers in the 
            # exchange is processed or attempted
            queue.join()
            tickers[header] = header_tickers
        # Cache the results from tickers
        cache.toCache(tickers)
    return cache.fromCache()