# @file utils.py
# @brief Utility functions used throughout the project

from pathlib import Path
import os.path
import urllib.request
import bs4

# @function getProjectRoot()
# @brief Fetches the project root directory path
def getProjectRoot() -> Path:
    return Path(__file__).parent.parent

# @function getCacheDir()
# @brief Fetches the cache directory path
def getCacheDir() -> Path:
    return Path(os.path.join(getProjectRoot(), "cache"))

# @function getPage()
# @brief Attempts to get the page html information using urllib
def getPage(url):
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        response = opener.open(url)
    except:
        return None
    return bs4.BeautifulSoup(response.read(), 'html.parser')

# @function fixErrors()
# @brief Attempts to fix known erros about the page 
#        information after page is fetched
def fixErrors(page):
    # If page fetch is unsuccessful initially
    if page is None:
        raise Exception('Invalid URL')
    return page