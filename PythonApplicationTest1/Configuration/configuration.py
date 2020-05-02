import configparser
import datetime

class Configuration:
    def __init__(self):
        self.filename = 'PythonApplicationTest1.ini'
        self.defaultsection = 'DEFAULT'
        self.datetimeformatproperty = 'datetimeformat'

    def getProperty(self, section, property):
        config = configparser.ConfigParser()
        config.sections()
        config.read(self.filename)
        if section is "DEFAULT" and config.has_option(section, property):
            return config[section][property]
        elif config.has_section(section) and config.has_option(section, property):
            return config[section][property]
    
    def setProperty(self, section, property, value):
        config = configparser.ConfigParser()
        config.sections()
        config.read(self.filename)
        config.set(section,property,value)

        with open(self.filename,'w') as configfile:
            config.write(configfile)

    def getPropertyDateTime(self, section, property):
        return datetime.datetime.strptime(self.getProperty(section, property), self.getProperty(self.defaultsection, self.datetimeformatproperty))

    def setPropertyDateTime(self, section, property, value):
         self.setProperty(section, property, value.replace(microsecond=0).strftime(Configuration().getProperty(self.defaultsection, self.datetimeformatproperty)))