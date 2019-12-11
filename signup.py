import json
import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecretSantaTable')

now = datetime.datetime.now()

#get list of current signups, returns empty list if there are no signups
def get_participants(team):
    data = table.get_item(Key={
        "year": now.year,
        "team": team,
    })
    
    if "Item" in data:
        list = data["Item"].get("participants")
        return list

    else:
        return []


def save_signup(name, team):
    participants = get_participants(team)
    
    #only allow for registration if name is not alreday in db
    if name not in participants:
        participants.append(name)
        
    signup = {
        "year": now.year,
        "team": team,
        "participants": participants,
    }
    return table.put_item(Item=signup) #create new signup list (this is a destructive operation)

def lambda_handler(event, context):

    print('received request: ' + str(event))
    name = event['currentIntent']['slots']['name']
    team = event['currentIntent']['slots']['team']
    print('Signing up {name} for Secret Santa List {team}'.format(name=name, team=team))
    save_signup(name, team)

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "🎅 I've added {name} to the {team} list. Merry fucking christmas. 🎄".format(name=name, team=team)
            },
        }
    }
    
    return response