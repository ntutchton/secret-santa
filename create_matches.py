import json
import boto3
import random
from boto3.dynamodb.conditions import Key
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SecretSantaTable')

now = datetime.datetime.now()

def get_team(team):
    response = table.query(KeyConditionExpression=Key('year').eq(now.year) & Key('team').eq(team))
    return response["Items"]

def get_random_person(people):
  random_index = random.randint(0,len(people))
  return people[random_index - 1]

def secret_santa(people):
  gifted = [] #people who are set to recieve a gift already
  matches = [] #finalized secret santa pairs

  for person in people:
    matched = False
    while not matched:
      match = get_random_person(people)
      if (match != person) and (match not in gifted): #cant gift yourself or someone already gifted
        gifted.append(match)
        matches.append({'giver': person, 'getter': match})
        matched = True

  return matches

def save_matches(matched_pairs, team):
        
    return table.update_item(Key={
        "year": now.year,
        "team": team,
    }, AttributeUpdates={
        'matched_pairs': {
            'Action': 'PUT',
            'Value': { 'L': matched_pairs }
        }
    })
    

def lambda_handler(event, context):

    print('received request: ' + str(event))
    team = event['currentIntent']['slots']['team']
    
    team_data = get_team(team)
    if len(team_data) > 0:
        team_data = team_data[0]
        if len(team_data["participants"]) > 1:
            matched_pairs = secret_santa(team_data["participants"])
            save_matches(matched_pairs, team)
            message = "🎅 Successfully created new matches for the {team} list. Creating new matches will overwrite existing matches.".format(team=team)
        elif len(team_data["participants"]) <= 1:
            message = "🎅 That list has only one member - can't create matches."
    else: 
        message = "🎅 I did not find a list by that name from this year."
    
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