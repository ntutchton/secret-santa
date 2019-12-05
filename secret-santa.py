import random

people = [
  'Adrianna', 
  'Alek', 
  'Grandma E', 
  'Grandpa E', 
  'Mom',
  'Nathan',
  'Robin'
]

def get_random_person(people):
  random_index = random.randint(0,len(people))
  return people[random_index - 1]

def secret_santa(people):
  gifted = [] #list for people who are set to recieve a gift already
  matches = [] #finalized matches list

  for person in people:
    matched = False
    while not matched:
      match = get_random_person(people)
      if (match != person) and (match not in gifted): #cant gift yourself or someone already gifteed
        gifted.append(match)
        matches.append((person, match))
        matched = True

  return matches

print(secret_santa(people))