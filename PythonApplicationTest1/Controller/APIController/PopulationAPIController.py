import pandas as pd
from Configuration.configuration  import *

class PopulationAPIController:
    def __init__(self):
        self.url = 'https://api.hungermapdata.org/swe-notifications/population.csv'
    
    def readPopulation(self):
        if Configuration().getProperty('DEFAULT', 'testMode') == 'True':
            path = Configuration().getProperty('TESTMODE','mockdatapath').format(Configuration().getProperty('TESTMODE','populationdatafilename'))
        else:
            path = self.url
        return pd.read_csv(path, delimiter=',')