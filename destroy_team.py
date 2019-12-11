import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecretSantaTable')

def remove_team(year, team):
    item_key = {
        "year": int(year),
        "team": str(team),
    }
    return table.delete_item(Key=item_key)

def lambda_handler(event, context):
    
    year = event['currentIntent']['slots']['year']
    team = event['currentIntent']['slots']['team']

    print('overwriting table {year}:{team}'.format(year=year, team=team))
    
    remove_team(year, team)
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "🎅 It is done."
            },
        }
    }
    
    return response
