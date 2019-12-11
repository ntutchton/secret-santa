import json
import boto3
# import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecretSantaTable')

# now = datetime.datetime.now()

def get_teams():

    matched_teams=[]
    
    response = table.scan()
    
    for team in response["Items"]:
        matched_teams.append(team["team"])
    
    return matched_teams

def lambda_handler(event, context):

    print('received request: ' + str(event))
    
    teams = get_teams()

    message = ("🎅 I don't have any lists right now. You can start a new one by providing a list name during signup.", "🎅 Here are all my list names: {}. If you want to know which ones you are on, try asking 'get my lists'.  If you want more info about a specific lists, ask 'list info'".format(teams))[len(teams)>0]
    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": message
            },
        }
    }
    
    return response