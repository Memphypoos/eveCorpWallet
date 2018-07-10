import configparser
import requests

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

##Request character names
def get_char_name(char_id):
  req = requests.get("https://esi.evetech.net/latest/characters/"+str(char_id))
  if req.status_code == 200: return req.json()["name"]

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
slack_message_ratting_title = "*Total Ratting Income for the past 30 days, less tax:*\n\n"
slack_message_agent_title = "*Total Agent Mission Reward for the past 30 days, less tax:*\n\n"
slack_message_bounty_title = "*Total Pirate Bounty Reward for the past 30 days, less tax:*\n\n"
slack_message_ratting = ""
slack_message_agent = ""
slack_message_bounty = ""
bounty = 0 # killing players with bounty bounty_prize
ratting = 0 # ratting bounty_prizes
agent = 0 # this is the base amount
char_bounty = {}
char_ratting = {}
char_agent = {}

#Agent Transactions
for transaction in div_one():
  if transaction["ref_type"] == "agent_mission_reward"and transaction["amount"] > 0:
    agent += transaction["amount"]
    if not transaction["second_party_id"] in char_agent:
      char_agent[transaction["second_party_id"]] = 0
    char_agent[transaction["second_party_id"]] += transaction["amount"]
  if transaction["ref_type"] == "agent_mission_time_bonus_reward" and transaction["amount"] > 0:
    agent += transaction["amount"]
    if not transaction["second_party_id"] in char_agent:
      char_agent[transaction["second_party_id"]] = 0
    char_agent[transaction["second_party_id"]] += transaction["amount"]
 #Bounty Transactions
  if transaction["ref_type"] == "bounty_prize" and transaction["amount"] > 0:
    bounty += transaction["amount"]
    if not transaction["second_party_id"] in char_bounty:
     char_bounty[transaction["second_party_id"]] = 0
    char_bounty[transaction["second_party_id"]] += transaction["amount"]
#Ratting Transactions
  if transaction["ref_type"] == "bounty_prizes" and transaction["amount"] > 0:
    ratting += transaction["amount"]
    if not transaction["second_party_id"] in char_ratting:
     char_ratting[transaction["second_party_id"]] = 0
    char_ratting[transaction["second_party_id"]] += transaction["amount"]
    

##Deriving the 95%
ratting100 = ratting * 100 / 5
agent100 = agent * 100 / 5
bounty100 = bounty * 100 / 5
ratting95 = ratting100 - ratting
agent95 = agent100 - agent
bounty95 = bounty100 - bounty

for character in char_agent:
  val100 = char_agent[character] * 100 / 5
  val95 = val100 - char_agent[character]
  slack_message_agent += get_char_name(character)+" received Agent rewards totalling "+str("{:,.2f}".format(val95))+" ISK"+"\n"
  #print(get_char_name(character))

for character in char_bounty:
  val100 = char_bounty[character] * 100 / 5
  val95 = val100 - char_bounty[character]
  slack_message_bounty += get_char_name(character)+" received Bounty rewards totalling "+str("{:,.2f}".format(val95))+" ISK"+"\n"
  #print(get_char_name(character))

for character in char_ratting:
  val100 = char_ratting[character] * 100 / 5
  val95 = val100 - char_ratting[character]
  slack_message_ratting += get_char_name(character)+" received Ratting rewards totalling "+str("{:,.2f}".format(val95))+" ISK"+"\n"
  #print(get_char_name(character))

###Constructing the Slack Message###

##Comment from here onwards to stop the slack message going out###
##Posting the request to Slack###
def post_to_slack(slack_message_ratting):
  print("loading header2...")
  header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+slack_token, 'Content-Type': "application/json; charset=utf-8"}
  print("header2 loaded....")
  slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, json=({'channel' : 'h0s_it', 'text': slack_message_ratting, 'as_user': 'true'}))
  print("Request posted to slack")
post_to_slack(slack_message_ratting_title + slack_message_ratting)

##Posting the request to Slack###
def post_to_slack(slack_message_agent):
  print("loading header2...")
  header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+slack_token, 'Content-Type': "application/json; charset=utf-8"}
  print("header2 loaded....")
  slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, json=({'channel' : 'h0s_notifications', 'text': slack_message_agent, 'as_user': 'true'}))
  print("Request posted to slack")
#post_to_slack(slack_message_agent_title + slack_message_agent)

def post_to_slack(slack_message_bounty):
  print("loading header2...")
  header2 = {'User-Agent':"slack:Github\Memphypoos",'Authorization':'Bearer '+slack_token, 'Content-Type': "application/json; charset=utf-8"}
  print("header2 loaded....")
  slack = requests.post("https://slack.com/api/chat.postMessage", headers=header2, json=({'channel' : 'h0s_notifications', 'text': slack_message_bounty, 'as_user': 'true'}))
  print("Request posted to slack")
#post_to_slack(slack_message_bounty_title + slack_message_bounty)
