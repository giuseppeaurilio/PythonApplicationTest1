import pandas as pd
from Configuration.configuration  import *

class RegionAPIController:
    def __init__(self):
        self.url = 'https://api.hungermapdata.org/swe-notifications/region/{region_id}/country'

    def getCountryId(self, regionId):
        if Configuration().getProperty('DEFAULT', 'testMode') == 'True':
            path = Configuration().getProperty('TESTMODE','mockdatapath').format(Configuration().getProperty('TESTMODE','regiondatafilename').format(regionId))
        else:
             path = self.url.format(region_id = regionId)
        return pd.read_json(path, typ = 'series')