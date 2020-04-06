import configparser

class Configuration:

    def getProperty(self, section, property):
        config = configparser.ConfigParser()
        config.sections()
        config.read('PythonApplicationTest1.ini')
        return config[section][property]