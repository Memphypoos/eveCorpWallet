import configparser
import requests
import json
from requests.auth import HTTPBasicAuth

##Eve developers.com ID's
client_id = '2ed1867da31440ad8296567d75cc8727'
client_key = '7ZcremKn9S7OlaAsv89jaMlL70OFMKSUjOuPI6MC'

##Configuration File - to hide the refresh_token
config = configparser.ConfigParser()
config.read("config.ini")
print("reading config...")
refresh_token = config.get("config", "refresh_token")
slack_token = config.get("slack","slack_key")

##Request access_token using refresh token
print("refreshing token...")
def refresh_esi_token():
  req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(client_id,client_key), data={'grant_type':'refresh_token','refresh_token':refresh_token})
  if req.status_code == 200: return req.json()["access_token"]
  print(access_token)
refresh_esi_token()

print("Getting Journal...")
access_token = refresh_esi_token()

header1 = {'User-Agent':"eveCorpWallet:Github\Memphypoos",'Authorization':'Bearer '+access_token}
print("Auth Success")
div_one = requests.get("https://esi.evetech.net/v3/corporations/98088408/wallets/1/journal/", headers=header1).json

#declare variables
slack_message = ""
piExIncome = 0 # this is the base amount
piImIncome = 0 
ratting = 0 # this is the base amount
bounty = 0 # this is the base amount

# Sort through the transactions one by one - Put the row into a variable called transaction
for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "planetary_export_tax":
   (transaction["amount"]) > 0
   piExIncome += transaction["amount"]
   
#print("Planetary Exports: "+"{:,.2f}".format(piExIncome))


 
for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "planetary_import_tax":
   (transaction["amount"]) > 0
   piImIncome += transaction["amount"]
#print("Planetary Imports: "+"{:,.2f}".format(piImIncome))

###Constructing the Slack Message###
slack_message = str("*Corp Wallet - Division 1*\n")+str("Planetary Import Tax: ")+ str("{:,.2f}".format(piImIncome))+str("\n") + str("Planetary Export Tax: ") + str("{:,.2f}".format(piExIncome))
#slack_message = ("Corp Wallet - Division 1\n")+"{:,.2f}".format(piImIncome)+(" ISK from Planetary Export Tax\n")+"{:,.2f}".format(piExIncome)+(" ISK from Planetary Import Tax")

print(slack_message)

##Comment from here onwards to stop the slack message going out###
##Posting the request to Slack###
def post_balance(slack_message):
 print("loading header2...")
 header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+slack_token, 'Content-Type': "application/json; charset=utf-8"}
 print("header2 loaded....")
 slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, data=json.dumps({'channel' : 'h0s_notifications', 'text': slack_message, 'as_user': 'true'}))
 print("Request posted to slack")
 print(slack_message)
post_balance(slack_message)
