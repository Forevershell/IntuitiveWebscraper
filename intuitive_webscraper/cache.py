import os.path
import json
from datetime import date
from pathlib import Path
from intuitive_webscraper.utils import getProjectRoot, getCacheDir

# A cache is internally stored as a json
# Could improve to become SQL database, but for now it has data and a date
# Updating logic is very convoluted with an SQL database, managing json is simpler
# Cache are updated by the day every time the application loads
# When any requests request a specific cache, it is either loaded or fetched from the scraper
class Cache:
    def __init__(self, outfile):
        self.outfile = outfile
        self.date = None
        self.data = None
        if self.cacheExists():
            self.loadCache()
    
    def toCache(self, data):
        result = dict()
        result['date'] = date.today().strftime("%d/%m/%Y")
        result['data'] = data
        with open(os.path.join(getCacheDir(), self.outfile), 'w') as file:
            json.dump(result, file)
    
    def loadCache(self):
        with open(os.path.join(getCacheDir(), self.outfile), 'r') as file:
            dump = json.load(file)
        self.data = dump['data']
        self.date = dump['date']
        if (not self.date):
            print('Cache corrupted')

    def fromCache(self):
        return self.data
        
    def cacheExists(self):
        if Path(os.path.join(getCacheDir(), self.outfile)).exists():
            return True
        else:
            return False
    
    def cacheExpired(self):
        return self.date != date.today().strftime("%d/%m/%Y")

    def cacheRemove(self):
        file_path = os.path.join(getCacheDir(), self.outfile)
        if Path(file_path).exists():
            os.remove(file_path)
        else:
            print("The file does not exist")
            
        


    
    

            
