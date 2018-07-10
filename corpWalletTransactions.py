import configparser
import requests
import json
import csv
from requests.auth import HTTPBasicAuth

##Eve developers.com ID's
client_id = '2ed1867da31440ad8296567d75cc8727'
client_key = '7ZcremKn9S7OlaAsv89jaMlL70OFMKSUjOuPI6MC'

##Configuration File - to hide the refresh_token
config = configparser.ConfigParser()
config.read("config.ini")
print("reading config...")
refresh_token = config.get("main", "refresh_token")
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
piImIncome = 0 # this is the base amount
bounty = 0 # killing players with bounty bounty_prize
ratting = 0 # ratting bounty_prizes
agent = 0 # this is the base amount
insurance = 0 # this is the base amount
bounty = 0 # this is the base amount
discover = 0 # this is the base amount

# Sort through the transactions one by one - Put the row into a variable called transaction
for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "planetary_export_tax":
   (transaction["amount"]) > 0
   piExIncome += transaction["amount"]
    
for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "planetary_import_tax":
   (transaction["amount"]) > 0
   piImIncome += transaction["amount"]

for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "agent_mission_reward":
   (transaction["amount"]) > 0
   agent += transaction["amount"]

for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "agent_mission_time_bonus_reward":
   (transaction["amount"]) > 0
   agent += transaction["amount"]

for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "bounty_prize":
   (transaction["amount"]) > 0
   bounty += transaction["amount"]

for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "bounty_prizes":
   (transaction["amount"]) > 0
   ratting += transaction["amount"]

for transaction in div_one():
# Build an extra line into the slack message for this transaction
 if (transaction["ref_type"]) == "project_discovery_reward":
   (transaction["amount"]) > 0
   discover += transaction["amount"]


###Constructing the Slack Message###
slack_message = str("*Corp Wallet - Division 1 (Income)*\n")+str("Planetary Import Tax: ")+ str("{:,.2f}".format(piImIncome))+" ISK"+str("\n") + str("Planetary Export Tax: ") + str("{:,.2f}".format(piExIncome))+" ISK"+"\n" +"Agent Mission Reward: "+str("{:,.2f}".format(agent))+" ISK"+"\n" + "Bounty Prizes: "+str("{:,.2f}".format(bounty))+" ISK"+ "\n" + "Ratting: "+str("{:,.2f}".format(ratting))+" ISK"+ "\n" + "Project Discovery Reward: "+str("{:,.2f}".format(discover))+" ISK"+"\n"+"\n"+"_Totals are as of the last 30 days_"

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
