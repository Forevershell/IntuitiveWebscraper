# @file cache.py
# @brief Cache class implementation
#
#        A cache that can do a few things
#        1. Load data
#        2. Store data
#        3. Be updated (by the day)
#
#        Currently implemented as a json cache
#        Can be later moved to an SQL database,
#        but update logic is simpler with json files

import os.path
import json
from datetime import date
from pathlib import Path
from intuitive_webscraper.utils import getProjectRoot, getCacheDir

class Cache:
    def __init__(self, outfile):
        self.outfile = outfile
        self.date = None
        self.data = None
        if self.cacheExists():
            self.loadCache()
    
    # @function cache.toCache
    # @brief Loads data to cache and timestamps the cache file
    # @param data: data to be saved
    def toCache(self, data):
        result = dict()
        result['date'] = date.today().strftime("%d/%m/%Y")
        result['data'] = data
        with open(os.path.join(getCacheDir(), self.outfile), 'w') as file:
            json.dump(result, file)
    
    # @function cache.loadCache
    # @brief Loads cache data upon cache creation, checks for cache corruption
    def loadCache(self):
        with open(os.path.join(getCacheDir(), self.outfile), 'r') as file:
            dump = json.load(file)
        self.data = dump['data']
        self.date = dump['date']
        if (not self.date):
            print('Cache corrupted')

    # @function cache.fromCaceh
    # @brief Gets the cache's data once the data is loaded
    # @return Data from the requested cache
    def fromCache(self):
        return self.data

    # @function cache.cacheExists
    # @brief Checks if the current cache exists in the cache files
    # @return If cache exists
    def cacheExists(self):
        if Path(os.path.join(getCacheDir(), self.outfile)).exists():
            return True
        else:
            return False
    
    # @function cache.cacheExpired
    # @brief Checks if the current cache is expired
    # @return If cache is expired
    def cacheExpired(self):
        return self.date != date.today().strftime("%d/%m/%Y")

    # @function cache.cacheRemove
    # @brief Removes the cache from the cache files
    def cacheRemove(self):
        file_path = os.path.join(getCacheDir(), self.outfile)
        if Path(file_path).exists():
            os.remove(file_path)
        else:
            print("The file does not exist")
            
        


    
    

            
