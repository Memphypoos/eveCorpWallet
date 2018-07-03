import configparser

##Create the config file programatically##
config = configparser.ConfigParser()
config['EVEDEV'] = {'Client ID': 'key', 
                    'Secret Key': 'key'}
config['SLACK'] = {'Slack ID': 'key',
                   'Slack Key': 'key'}
with open('config.ini', 'w') as configfile:
  config.write(configfile)



                   