from Controller.FoodSecurityController import FoodSecurityController
from Configuration.configuration  import *
import time

#p1 = FoodSecurityController()
#p1.initializeCountriesStructure()

while True:
    p1 = FoodSecurityController()
    p1.initializeCountriesStructure()
    p1.checkFoodSecurity()
    time.sleep(int(Configuration().getProperty('DEFAULT', 'runtimesecondsinterval')))
     