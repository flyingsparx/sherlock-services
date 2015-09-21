#!/usr/bin/python
#
# Script to convert JSON output from experiments into
# wide CSV format for processing by US Army Research Labs.

import json, time, datetime, urllib2, sys

if len(sys.argv) != 2:
  print 'Usage: python csv_converter.py logURL'
  exit()

exp_name = sys.argv[1]

confirm_card_id = 11
nl_card_id = 10
tell_card_id = 7
ask_card_id = 8
gist_card_id = 9

def get_data():
  response = urllib2.urlopen('http://logger.cenode.io/cards/'+exp_name)
  return json.loads(response.read())

def get_value(card, val):
  for value in card['values']:
    if value['descriptor'] == val:
      return value['type_name'] 

def get_relationship(card, rel):
  for relationship in card['relationships']:
    if relationship['label'] == rel:
      return relationship['target_name'] 


def generate_csv(data):
  output = ',Exprun,asktell,uniqueid,expid,id,time,POSIXtime,content,location,pause,response,potentialscore,actualscore,timetorespond,keystrokes,\n'
  users_seen = []
  cards_seen = set()
  for i, card in enumerate(data):
    try:
      is_from = get_relationship(card, 'is from')
      content = get_value(card, 'content')
      if content is not None and is_from and not ' agent' in is_from and not 'Sherlock' in is_from and card['name'] not in cards_seen and not 'there is an agent named' in content:
        content = content.replace(',', '')
        timestamp = long(get_value(card, 'timestamp'))
        keystrokes = ''
        pause = ''
        reply = None
        reply_timestamp = ''
        reply_content = ''
        response_time = ''
        potential_score = ''
        score = ''
        location = ''

        for card2 in data:
          if get_relationship(card2, 'is in reply to') == card['name']:
            reply = card2
            reply_timestamp = long(get_value(reply, 'timestamp'))
            reply_content = get_value(reply, 'content')
            response_time = (float(reply_timestamp) - float(timestamp)) / 1000
            if reply['concept_id'] == confirm_card_id:
              potential_score = 1
            elif content == reply_content:
              reply_content = '[CE SAVED]'
              score = 1
            elif 'Un-parseable input' in reply_content:
              reply_content = '[NOT UNDERSTOOD]'
                
            break
        
        lat = get_value(card, 'latitude')
        lon = get_value(card, 'longitude')
        if lat and lon:
          location = '('+str(lat)+'; '+str(lon)+')'
         
        
        timePOSIX = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
        user_number = None

        if is_from.lower() in users_seen:
          user_number = users_seen.index(is_from.lower())
        else:
          users_seen.append(is_from.lower())
          user_number = len(users_seen) - 1

        if card['concept_id'] == tell_card_id:
          try:
            start_time = long(get_value(card, 'start time'))
            submit_time = long(get_value(card, 'submit time'))
            pause = (float(submit_time) - float(start_time)) / 1000
          except:
            pass
          try:
            keystrokes = int(get_value(card, 'number of keystrokes'))
          except:
            pass
        
        cards_seen.add(card['name'])
        output = output + str(i)+','+exp_name.replace('/', '-')+',0,'+str(user_number)+','+is_from+','+card['name']+','+time+','+timePOSIX+','+content+','+location+','+str(pause)+','+reply_content+','+str(potential_score)+','+str(score)+','+str(response_time)+','+str(keystrokes)+'\n'
    
    except Exception as e:
      print e
  return output

def write_csv(csv):
  f = open(exp_name.replace('/', '-')+'.csv', 'w')
  f.write(csv)
  f.close()

data = get_data()
csv = generate_csv(data)
write_csv(csv)
