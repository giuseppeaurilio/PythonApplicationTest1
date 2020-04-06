import pandas as pd
from Configuration.configuration  import *

class InsicurePeopleAPIController:
    def __init__(self):
        #self.urlCurrent =
        #'https://api.hungermapdata.org/swe-notifications/foodsecurity'
        self.url = 'https://api.hungermapdata.org/swe-notifications/foodsecurity?days_ago={0}'

    def getInsicurePeople(self, daysago):
        if Configuration().getProperty('DEFAULT', 'testMode') == 'True':
            path = Configuration().getProperty('TESTMODE','mockdatapath').format(Configuration().getProperty('TESTMODE','foodcheckdatafilename').format(daysago))
        else:
            path = self.url.format(daysago)
        return pd.read_json(path)