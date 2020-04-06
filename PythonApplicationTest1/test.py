import unittest

from Configuration.configuration  import *
from Controller.CountryController import *
from Controller.FoodSecurityController import *
from Controller.APIController.InsicurePeopleAPIController import *

class Test_test(unittest.TestCase):

    def test_inizialization(self):
        p1 = FoodSecurityController()
        p1.initializeCountriesStructure()
        self.assertEqual(len(p1.countries), 5)
        for key in p1.countries:
            if key == 1:
                self.assertEqual(len(p1.countries[key].regionIds), 3)
                self.assertEqual(p1.countries[key].totPopulation, 60)
            if key == 2:
                self.assertEqual(len(p1.countries[key].regionIds), 3)
                self.assertEqual(p1.countries[key].totPopulation, 150)
            if key == 3:
                self.assertEqual(len(p1.countries[key].regionIds), 2)
                self.assertEqual(p1.countries[key].totPopulation, 150)
            if key == 4:
                self.assertEqual(len(p1.countries[key].regionIds), 1)
                self.assertEqual(p1.countries[key].totPopulation, 90)
            if key == 16:
                self.assertEqual(len(p1.countries[key].regionIds), 1)
                self.assertEqual(p1.countries[key].totPopulation, 0)
        #for key in p1.countries:
        #    print(CountryController().print(p1.countries[key]))
        #print('Processed {0}'.format(len(p1.countries)))
       
    def test_foodsecuritytreshold(self):
        p1 = FoodSecurityController()
        p1.initializeCountriesStructure()
        #get curren data
        foodSecurityCurrent = InsicurePeopleAPIController().getInsicurePeople(0)
        #get 30 days ago data
        foodSecurity30DaysAgo = InsicurePeopleAPIController().getInsicurePeople(30)
        for keycountry in p1.countries:
            #verify insicure people variation for che current country
            countryvariation = CountryController().checkInsecurePeople(p1.countries[keycountry], foodSecurityCurrent, foodSecurity30DaysAgo)
            if keycountry == 1:
                self.assertEqual(countryvariation, 33.33)
            if keycountry == 2:
                self.assertEqual(countryvariation, -13.33)
            if keycountry == 3:
                self.assertEqual(countryvariation, 3.33)
            if keycountry == 4:
                self.assertEqual(countryvariation, -2.22)
            if keycountry == 16:
                self.assertEqual(countryvariation, 0)

    def test_foodsecurityemailsender(self):
        p1 = FoodSecurityController()
        p1.initializeCountriesStructure()
        #get curren data
        foodSecurityCurrent = InsicurePeopleAPIController().getInsicurePeople(0)
        #get 30 days ago data
        foodSecurity30DaysAgo = InsicurePeopleAPIController().getInsicurePeople(30)
        for keycountry in p1.countries:
            #verify insicure people variation for che current country
            countryvariation = CountryController().checkInsecurePeople(p1.countries[keycountry], foodSecurityCurrent, foodSecurity30DaysAgo)
            if countryvariation >= 5:
                 CountryController().sendEmail(keycountry,p1.countries[keycountry].totPopulation, countryvariation)

    def test_foodsecurityemailsender_missingemailaddresses(self):
        CountryController().sendEmail(12,100, 10)

if __name__ == '__main__':
    unittest.main()
