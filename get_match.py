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


def create_error_msg(team_data, name):
    if name not in team_data["participants"]:
        return "🎅 You are not a member of that team. You need to sign up first."
    if "matched_pairs"not in team_data:
        return "🎅 Matched pairs have not been created for this group yet."


def lambda_handler(event, context):

    print('received request: ' + str(event))
    team = event['currentIntent']['slots']['team']
    name = event['currentIntent']['slots']['name']
    
    team_data = get_team(team)
    if len(team_data) > 0:
        team_data = team_data[0]
        if name in team_data["participants"] and "matched_pairs" in team_data:
            my_match = ''
            pairs = team_data["matched_pairs"]["L"] #because of the way dynamo returns shit have to specifcfy the list 'L'
            for pair in pairs:
                if pair["giver"] == name:
                    my_match = pair["getter"]

            message = " 🎅 You are supposed to get a present for {my_match}. You => 🎁  => {my_match}.".format(my_match=my_match, name=name)
        else:
            message = create_error_msg(team_data, name)
    else: 
        message = "🎅 I did not find a list by that name from this year. You can look for yourself by asking 'show all lists'."
    
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