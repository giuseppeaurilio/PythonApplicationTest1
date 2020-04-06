import pandas as pd
from Configuration.configuration  import *

class CountryAPIController:
    def __init__(self):
        self.url = 'https://api.hungermapdata.org/swe-notifications/country/{0}/regions'

    def getRegionIds(self, countrId):
        
        if Configuration().getProperty('DEFAULT', 'testMode') == 'True':
            path = Configuration().getProperty('TESTMODE','mockdatapath').format(Configuration().getProperty('TESTMODE','countrydatafilename').format(countrId))
            #return pd.read_json(localpath)
        else:
            path = self.url.format(countrId)
        return pd.read_json(path)
            