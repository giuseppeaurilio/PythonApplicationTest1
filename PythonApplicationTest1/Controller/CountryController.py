from Configuration.configuration  import *
from Model.Country import *
import pandas as pd
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class CountryController:

    #function to create a country
    def createCountry(self,countryId):
        return Country(countryId, [], 0)

    #function to add a region to a country
    def addRegion(self,country, regionId):
        #TODO: insert check if region already exists
        country.regionIds.append(regionId)
        
    #function to increase population of a country
    def addPopulation(self,country, regionPop):
        country.totPopulation += regionPop

    #this function calculate the variation for a country
    def checkInsecurePeople(self, country, foodSecurityCurrent, foodSecurity30DaysAgo):
        current = 0
        daysago = 0
        #calculate variation for all the region of a cuontry
        for keyregion in country.regionIds:
                items = foodSecurityCurrent[foodSecurityCurrent['region_id'] == keyregion]
                if len(items) > 0:
                    current += items.iloc[0]['food_insecure_people']
                items = foodSecurity30DaysAgo[foodSecurity30DaysAgo['region_id'] == keyregion]
                if len(items) > 0:
                    daysago += items.iloc[0]['food_insecure_people']
        
        if country.totPopulation > 0: #handle if total population is not > 0
            #calculate the varioation in percentage, rounded at the second
                                                 #decimal place.
                                                 #should i consider only positive variation or absolute?
            #variation = round((abs((current - daysago) / country.totPopulation) * 100),2)
            variation = round((((current - daysago) / country.totPopulation) * 100),2)
        else:
            variation = 0
        return variation

    def print(self,country): #utility function
        return "country: {0}, regioncount: {1}, totpop: {2};".format(country.id, len(country.regionIds), country.totPopulation)

    def sendEmail(self,country, totPopulation, variation):
        path = Configuration().getProperty('DEFAULT', 'emailaddressespath')

        #get email template
        emailtexttemplatepath = path.format(Configuration().getProperty('DEFAULT', 'emailtext'))
        with open(emailtexttemplatepath, 'r') as template_file:
            template_file_content = template_file.read()

        #get country addresses
        countryaddressespath = path.format(Configuration().getProperty('DEFAULT', 'countryemailfilename').format(country))
        if os.path.exists(countryaddressespath):
            countryaddresses = pd.read_json(countryaddressespath)
        else:
            countryaddresses = None

        #get admin addresses
        adminaddressespath = path.format(Configuration().getProperty('DEFAULT', 'adminemailfilename'))
        if os.path.exists(adminaddressespath):
            adminaddresses = pd.read_json(adminaddressespath)
        else:
            adminaddresses = None
       
        msg = MIMEMultipart()       # create a message
        # add in the actual data to the message template
        message = template_file_content.format(country_id=country, totpop=totPopulation, variation=variation)
        

        msg['Subject'] = "Food security checker variation"

        #sender address
        msg['From'] = Configuration().getProperty('DEFAULT', 'emailsenderaddress')
        #add country addresses
        if countryaddresses is not None:
            for contact in countryaddresses["addresses"]:
                if contact["role"] == "to":
                    msg['To'] = contact["email"]
                if contact["role"] == "cc":
                    msg['Cc'] = contact["email"]
                if contact["role"] == "ccn":
                    msg['Ccn'] = contact["email"]
        #add admin addresses
        if adminaddresses is not None:
            for contact in adminaddresses["addresses"]:
                if contact["role"] == "to":
                    msg['To'] = contact["email"]
                if contact["role"] == "cc":
                    msg['Cc'] = contact["email"]
                if contact["role"] == "ccn":
                    msg['Ccn'] = contact["email"]

        msg.attach(MIMEText(message, 'plain'))

        ##setup smtp connection
        #s = smtplib.SMTP(host= Configuration().getProperty('DEFAULT', 'smtpserverurl'), port=Configuration().getProperty('DEFAULT', 'smtpserverport'))
        #s.starttls()
        #s.login(Configuration().getProperty('DEFAULT', 'smtpserverusername'), Configuration().getProperty('DEFAULT', 'smtpserverpassword'))
        ## send the message via the server set up earlier.
        #s.send_message(msg)
        