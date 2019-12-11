# Secret Santa Chat Bot

This repo houses lambda scripts for a Lex-backed Secret Stanta chatbot powered by twillio SMS.

The bot is capable of managing lists of people particiapting in a Secret Santa event, and matching particiapnts with their gift reciepinets.

Supported commands (and some variants):

```
hi 
```
displays welcome message and brief instructions
```
show commands
```
returns some of the availble commands
```
sign up
```
directs you through signup for a list (must supply list name, user name)
```
get all lists
```
returns all lists created in the current year
```
get my lists
```
returns all lists that user is a member of (must supply user name)
```
get list info
``` 
returns membership (list) and matching info (boolean) (must supply list name)
```
create matches
```
matches all participants on a list. this will replace all existing list matches (must supply list name)
```
destroy list
```
deletes a list from the DB
