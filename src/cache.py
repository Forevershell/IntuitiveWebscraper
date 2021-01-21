import os.path
import json
from datetime import date
from utils import get_project_root
from pathlib import Path

SOURCES = Path(os.path.join(get_project_root(), "cache"))

# A cache is internally stored as a json
# Could improve to become SQL database, but for now it has data and a date
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
        with open(os.path.join(SOURCES, self.outfile), 'w') as file:
            print("sadas")
            json.dump(result, file)
    
    def loadCache(self):
        with open(os.path.join(SOURCES, self.outfile), 'r') as file:
            dump = json.load(file)
        self.data = dump['data']
        self.date = dump['date']
        if (not self.date):
            print('Cache corrupted')

    def fromCache(self):
        return self.data
        
    def cacheExists(self):
        if Path(os.path.join(SOURCES, self.outfile)).exists():
            return True
        else:
            return False
    
    def cacheExpired(self):
        return self.date != date.today().strftime("%d/%m/%Y")
        
        


    
    

            
