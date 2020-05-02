#import csv
#import time
from Controller.APIController.PopulationAPIController import *
from Controller.APIController.RegionAPIController import *
from Controller.APIController.CountryAPIController import *
from Controller.APIController.InsicurePeopleAPIController import *
from Controller.CountryController import *
from Configuration.configuration  import *
import multiprocessing as mp
import datetime

class FoodSecurityController:
    def __init__(self):
        self.countries = {}

    #call the population csv file and create an in memory structure of
    #countries,
    def initializeCountriesStructure(self):
        #start = datetime.datetime.now()
        #print(f'starting reading population.')
        ##read csv file
        #csv_reader = PopulationAPIController().readPopulation()
        #index = 0
        #l = len(csv_reader)
        #self.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete',
        #length = 50)
        ##loop throwgh regions
        #for indexcsv, rowcsv in csv_reader.iterrows():

        #    #retrieve country ID of a region
        #    regionfatherdata = RegionAPIController().getCountryId(rowcsv[0])
        #    #print(regionfatherdata)
        #    #if country was already inserted in structure -> read country
        #    if regionfatherdata['country_id'] in self.countries:
        #        curcountry = self.countries[regionfatherdata['country_id']]
        #    else: #else -> create country
        #        curcountry =
        #        CountryController().createCountry(regionfatherdata['country_id'])
        #    #update country data
        #    CountryController().addRegion(curcountry, rowcsv['region_id'])
        #    CountryController().addPopulation(curcountry,
        #    rowcsv['population'])
        #    #store country in in.memory structure
        #    self.countries[regionfatherdata['country_id']] = curcountry
        #    index +=1
        #    self.printProgressBar(index, l, prefix = 'Progress:', suffix =
        #    'Complete', length = 50)
                
        #    #print(self.countries[1].regionIds)
        #end = datetime.datetime.now()
        #print(f' execudet in %s .' % (end-start).total_seconds())

        start = datetime.datetime.now().replace(microsecond=0)
        
        print(f'starting reading population.')
        print(f'time: ', datetime.datetime.now().replace(microsecond=0))
        #read csv file
        csv_reader = PopulationAPIController().readPopulation()
        index = 0
        l = len(csv_reader)
        self.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        regioncountriesdictionary = {}
        #loop throwgh regions
        for indexcsv, rowcsv in csv_reader.iterrows():

            #get the country ID of the region
            #first check in the local dictionary
            if rowcsv['region_id'] not in regioncountriesdictionary:
                    #if not found
                        #call API to retrieve country ID of a region
                        regionfatherdata = RegionAPIController().getCountryId(rowcsv[0])
                        #call API to retrieve all the region of a country
                        countrydata = CountryAPIController().getRegionIds(regionfatherdata['country_id'])
                        #store result in local dictionary
                        for keyregion in countrydata["regions"]:
                            regioncountriesdictionary[keyregion["region_id"]] = regionfatherdata['country_id']
            #read country id from dictionary
            countryId = regioncountriesdictionary[rowcsv['region_id']]
            #if country was already inserted in structure -> read country
            if countryId in self.countries:
                curcountry = self.countries[countryId]   
            else: #else -> create country
                curcountry = CountryController().createCountry(countryId)
            #update country data
            CountryController().addRegion(curcountry, rowcsv['region_id'])
            CountryController().addPopulation(curcountry, rowcsv['population'])
            #store country in in.memory structure
            self.countries[regionfatherdata['country_id']] = curcountry
            index +=1
            self.printProgressBar(index, l, prefix = 'Progress:', suffix = 'Complete', length = 50)                
                
            #print(self.countries[1].regionIds)
        end = datetime.datetime.now().replace(microsecond=0)
        timetaken = (end - start).total_seconds()
        print(f'execuded in %s seconds.' % timetaken)
        return timetaken
        

    def checkFoodSecurity(self):
        start = datetime.datetime.now().replace(microsecond=0)
        #Configuration().setPropertyDateTime('DEFAULT',
        #'lastfoodsecuritycheck', datetime.datetime.now())
        print(f'Starting check food security.')
        print(f'time: ', datetime.datetime.now().replace(microsecond=0))
        #get curren data
        foodSecurityCurrent = InsicurePeopleAPIController().getInsicurePeople(0)
        #get 30 days ago data
        foodSecurity30DaysAgo = InsicurePeopleAPIController().getInsicurePeople(30)
        l = len(self.countries)
        self.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        #loop through countries in-memory structure.
        index = 0
        resultstring = "result "
        #N = mp.cpu_count()
        #values = [(self.countries[keycountry], foodSecurityCurrent,
        #foodSecurity30DaysAgo) for keycountry in self.countries]
        #with mp.Pool(processes = N) as pool:
        #    results = pool.map(CountryController().checkInsecurePeople,
        #    values)
        #    print(results)
        
        for keycountry in self.countries:
            #verify insicure people variation for che current country
            countryvariation = CountryController().checkInsecurePeople(self.countries[keycountry], foodSecurityCurrent, foodSecurity30DaysAgo)
            #check if i need to send an email
            if countryvariation >= 5:
                resultstring += "country: {0}, totpop: {1}, var: {2}; -> WARNING \n".format(keycountry,self.countries[keycountry].totPopulation, countryvariation)
                #print("country: {0}, totpop: {1}, var: {2}; ->
                #WARNING".format(keycountry,self.countries[keycountry].totPopulation,countryvariation))
                CountryController().sendEmail(keycountry,self.countries[keycountry].totPopulation, countryvariation)
            else:
                #print("country: {0}, totpop: {1}, var: {2}; ->
                #OK".format(keycountry,self.countries[keycountry].totPopulation,
                #countryvariation))
                resultstring += "country: {0}, totpop: {1}, var: {2}; -> OK \n".format(keycountry,self.countries[keycountry].totPopulation, countryvariation)
            index +=1
            self.printProgressBar(index, l, prefix = 'Progress:', suffix =
            'Complete', length = 50)
        end = datetime.datetime.now().replace(microsecond=0)
        print(f'results: ')
        print(resultstring)
        timetaken = (end - start).total_seconds()
        print(f'execuded in %s seconds.' % timetaken)
        return timetaken

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()

    def runcheck(self):
      
        nextpopulationcheckdatetime = Configuration().getPropertyDateTime('DEFAULT', 'nextpopulationcheckdatetime')
        timetaken1 = 0
        if len(self.countries) is 0 or datetime.datetime.now() >= nextpopulationcheckdatetime :
            pupulationchecktimeinterval = int(Configuration().getProperty('DEFAULT', 'populationcheckintervalminutes'))
            Configuration().setPropertyDateTime('DEFAULT', 'nextpopulationcheckdatetime', (datetime.datetime.now() + datetime.timedelta(minutes=pupulationchecktimeinterval)))
            timetaken1 = self.initializeCountriesStructure()
        
        #lastfoodsecuritycheck = Configuration().setPropertyDateTime('DEFAULT',
        #'lastexecutiondatetime', datetime.datetime.now())
        timetaken2 = 0
        timetaken2 = self.checkFoodSecurity()

        return (timetaken2 + timetaken1)