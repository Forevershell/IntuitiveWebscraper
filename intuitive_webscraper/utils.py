from pathlib import Path
import os.path
import urllib.request
import bs4

def getProjectRoot() -> Path:
    return Path(__file__).parent.parent

def getCacheDir() -> Path:
    return Path(os.path.join(getProjectRoot(), "cache"))

def getPage(url):
    try:
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
        response = opener.open(url)
    except:
        return None
    return bs4.BeautifulSoup(response.read(), 'html.parser')

def fixErrors(page):
    if page is None:
        raise Exception('Invalid URL')
    # For capturing edge cases in bs4 parser
    return page