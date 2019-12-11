import json
import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecretSantaTable')

now = datetime.datetime.now()

def get_teams(name=None):

    matched_teams=[]
    
    response = table.scan()
    
    for team in response["Items"]:
        if name in team["participants"]:
            matched_teams.append(team["team"])
    
    return matched_teams

def lambda_handler(event, context):

    print('received request: ' + str(event))
    name = event['currentIntent']['slots']['name']
    
    teams = get_teams(name)

    message = ("🎅 You aren't on any lists, You still need to sign up.  If you want to see what lists I already have, try asking 'show all lists'.", "🎅 I found that name on these lists from this year: {}".format(teams))[(len(teams) > 0)]
    
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