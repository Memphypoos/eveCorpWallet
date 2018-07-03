import configparser

config = configparser.ConfigParser()
config.read('config.ini')
config.sections()
for key in config['SLACK']
  print(key)