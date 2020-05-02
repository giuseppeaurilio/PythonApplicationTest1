from Controller.FoodSecurityController import FoodSecurityController
from Configuration.configuration  import *
import time
import datetime
import sys

#p1 = FoodSecurityController()
#p1.initializeCountriesStructure()foodsecuritycheckinterval
index = 0
elapsed = 0
p1 = FoodSecurityController()
#if bool(Configuration().getProperty('DEFAULT', 'runatstartup')) == 'True':
#    print("iteration ", index)
#    elapsed = p1.runcheck()
#    index +=1
while True:
    #verify startup condition
    nextexec = Configuration().getPropertyDateTime('DEFAULT', 'nextexecutiondatetime')
    
    if datetime.datetime.now() >= nextexec:
        runtimecycleminutes = int(Configuration().getProperty('DEFAULT', 'runtimecycleminutes'))
        nextexec = datetime.datetime.now() + datetime.timedelta(minutes=runtimecycleminutes)
        Configuration().setPropertyDateTime('DEFAULT', 'nextexecutiondatetime', nextexec)
        print(f"iteration %s                                      " % (index))
        elapsed = p1.runcheck()
        index +=1
        while datetime.datetime.now() > nextexec:
            nextexec += datetime.timedelta(minutes=runtimecycleminutes)
        Configuration().setPropertyDateTime('DEFAULT', 'nextexecutiondatetime', nextexec)
   
    sleeper = nextexec - datetime.datetime.now()
    loopindex = sleeper.seconds
    while loopindex >= 0: 
    #if sleeper.seconds > 0:
        #print('next iteration will be executed in %s seconds.' % loopindex, end = '\r')
        time.sleep(1)
        loopindex -= 1


     