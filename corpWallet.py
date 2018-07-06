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
def refresh_esi_token():
  req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(client_id,client_key), data={'grant_type':'refresh_token','refresh_token':refresh_token})
  if req.status_code == 200: return req.json()["access_token"]

##Authenticate refresh_token against user
def get_balance():
 access_token = refresh_esi_token()
 header1 = {'User-Agent':"eveCorpWallet:Github\Memphypoos",'Authorization':'Bearer '+access_token}
 cwallet = requests.get("https://esi.evetech.net/v1/corporations/98088408/wallets/", headers=header1, json={'division': 'balance'})
 return cwallet.json()

##Creating and Formatting the Slack Message - note the .formatting
slack_message = ""
esi_balances = get_balance()
for esi_balance in esi_balances:
 slack_message = slack_message+"*Wallet Division* "+str(esi_balance["division"])+" has balance ""{:,.2f}".format(esi_balance["balance"])+" ISK\n"

##Posting the request to Slack
def post_balance(slack_message):
 print("loading header2...")
 header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+slack_token, 'Content-Type': "application/json; charset=utf-8"}
 print("header2 loaded....")
 slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, data=json.dumps({'channel' : 'h0s_notifications', 'text': slack_message, 'as_user': 'true'}))
 print("Request posted to slack")
 print(slack_message)
post_balance(slack_message)
 