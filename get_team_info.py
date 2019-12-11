import json
import boto3
from boto3.dynamodb.conditions import Key
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecretSantaTable')

now = datetime.datetime.now()

def get_team(team):

    response = table.query(KeyConditionExpression=Key('year').eq(now.year) & Key('team').eq(team))
    
    return response["Items"]
    

def lambda_handler(event, context):

    print('received request: ' + str(event))
    team = event['currentIntent']['slots']['team']
    
    team_data = get_team(team)
    if len(team_data) > 0:
        team_data = team_data[0]
        
        num_members = len(team_data["participants"])
        members = team_data["participants"]
        matched_message = (" Members have not been matched up yet. You can match up this list with the 'create matches' command.", " Members have already been matched up with the 'create matches' command.")["matched_pairs" in team_data]
    
        message = "🎅 {team} has {num_members} members: {members}. {matched_message}".format(
            team=team, 
            num_members=num_members, 
            members= members,
            matched_message = matched_message
        )
    else: 
        message = "🎅 I did not find a list by that name from this year. You can create that list by providing that list name during signup!"
    
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