#import csv
#import time
from Controller.APIController.PopulationAPIController import *
from Controller.APIController.RegionAPIController import *
from Controller.APIController.CountryAPIController import *
from Controller.APIController.InsicurePeopleAPIController import *
from Controller.CountryController import *


class FoodSecurityController:
    def __init__(self):
        self.countries = {}

    #call the population csv file and create an in memory structure of
    #countries,
    def initializeCountriesStructure(self):
        print(f'starting reading population.')
        #read csv file
        csv_reader = PopulationAPIController().readPopulation()
        index = 0
        l = len(csv_reader)
        self.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        #loop throwgh regions
        for indexcsv, rowcsv in csv_reader.iterrows():

            #retrieve country ID of a region
            regionfatherdata = RegionAPIController().getCountryId(rowcsv[0])
            #print(regionfatherdata)
            #if country was already inserted in structure -> read country
            if regionfatherdata['country_id'] in self.countries:
                curcountry = self.countries[regionfatherdata['country_id']]   
            else: #else -> create country
                curcountry = CountryController().createCountry(regionfatherdata['country_id'])
            #update country data
            CountryController().addRegion(curcountry, rowcsv['region_id'])
            CountryController().addPopulation(curcountry, rowcsv['population'])
            #store country in in.memory structure
            self.countries[regionfatherdata['country_id']] = curcountry
            index +=1
            self.printProgressBar(index, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
            #countrydata =
            #CountryAPIController().getRegionIds(regionfatherdata[1])
            #print(countrydata)
            #for indexcountry, rowcountry in countrydata.iterrows():
            #    #print(f'{rowcountry}');
            #    if rowcountry[0] in self.countries:
            #        print(f'non trovato');
            #        curcountry = self.countries[rowcountry[0]]
            #        #print(countrydata)
            #    else:
            #        print(f'trovato');
            #        curcountry = Country(rowcountry[0], [], 0)
            #    curcountry.addRegion(rowcsv[0])
                
                
            #print(self.countries[1].regionIds)
        print(f'end.')
        #for key in self.countries:
        #    print(CountryController().print(self.countries[key]))
        #print('Processed {0}'.format(len(self.countries)))
        

    def checkFoodSecurity(self):
        print(f'starting check food security.')
        #get curren data
        foodSecurityCurrent = InsicurePeopleAPIController().getInsicurePeople(0)
        #get 30 days ago data
        foodSecurity30DaysAgo = InsicurePeopleAPIController().getInsicurePeople(30)
        l = len(self.countries)
        self.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        #loop through countries in-memory structure.
        index = 0
        for keycountry in self.countries:
            #verify insicure people variation for che current country
            countryvariation = CountryController().checkInsecurePeople(self.countries[keycountry], foodSecurityCurrent, foodSecurity30DaysAgo)
            #check if i need to send an email
            if countryvariation >= 5:         
                #print("country: {0},  totpop: {1},  var: {2}; ->  WARNING".format(keycountry,self.countries[keycountry].totPopulation, countryvariation))
                CountryController().sendEmail(keycountry,self.countries[keycountry].totPopulation, countryvariation)
            #else:
            #    print("country: {0},  totpop: {1},  var: {2}; -> OK".format(keycountry,self.countries[keycountry].totPopulation, countryvariation))
            index +=1
            self.printProgressBar(index, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        print(f'end.')

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