#!/usr/bin/python
#
# Script to convert JSON output from experiments into
# wide CSV format for processing by US Army Research Labs.

import json, time, datetime, urllib2, sys, os, re

if len(sys.argv) != 2:
  print 'Usage: python csv_converter.py logURL'
  exit()

exp_name = sys.argv[1]

types = {
  11:'confirm',
  10:'nl',
  7:'tell',
  8:'ask',
  9:'gist'
}

questions = {
  1:['pineapple', 'eat|like'],
  2:['finch', 'play'],
  3:['apple', 'eat|like'],
  4:['crane', 'wear|shirt'],
  6:['robin', 'in|room'],
  7:['stork', 'wear|shirt'],
  8:['stork', 'in|room'],
  9:['emerald', 'in', 'contents'],
  12:['banana', 'eat|like'],
  13:['sapphire', 'in'],
  17:['crane', 'play'],
  18:['red', 'wear|shirt'],
  19:['rugby', 'play'],
  20:['hawk', 'eat|like'],
  23:['robin', 'eat|like'],
  24:['finch', 'wear|shirt'],
  25:['apple', 'in|room'],
  26:['yellow', 'wear|shirt'],
  28:['silver', 'contains'],
  30:['black', 'wear|shirt'],
  31:['lemon', 'eat|like'],
  33:['crane', 'eat|like'],
  34:['baseball', 'play'],
  35:['soccer', 'play'],
  36:['stork', 'play'],
  37:['ruby', 'contents', 'in'],
  39:['golf', 'plays'],
  40:['orange', 'eat|like'],
  41:['falcon', 'wear|shirt'],
  45:['amber', 'contents', 'in'],
  47:['crane', 'in|room'],
  48:['pear', 'in|room'],
  50:['stork', 'eat|like'],
  52:['robin', 'play'],
  53:['falcon', 'in|room'],
  54:['falcon', 'play']
}

def get_data():
  if os.path.isfile(exp_name):
    exp_file = open(exp_name, 'r')
    data = []
    for line in exp_file.readlines():
      data.append(json.loads(line))
    exp_file.close()
    return data
  else:
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
  output = ',Exprun,asktell,uniqueid,expid,id,time,POSIXtime,type,aboutqs,content,location,pause,response,potentialscore,actualscore,timetorespond,keystrokes,Blank,Empty,Failed,Mimic,Not-understood,Question\n'
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
        blank = 0
        empty = 0
        failed = 0
        mimic = 0
        not_understood = 0
        question = 0
        
        if content == '':
          empty = 1
          blank = 1
      
        for card2 in data:
          if get_relationship(card2, 'is in reply to') == card['name']:
            reply = card2
            reply_timestamp = long(get_value(reply, 'timestamp'))
            reply_content = get_value(reply, 'content')
            response_time = (float(reply_timestamp) - float(timestamp)) / 1000
            if types[reply['concept_id']] == 'confirm':
              potential_score = 1
            elif content == reply_content:
              reply_content = '[CE SAVED]'
              score = 1
              if types[card['concept_id']] == 'nl':
                mimic = 1
            elif 'Un-parseable input' in reply_content:
              reply_content = '[NOT UNDERSTOOD]'
              failed = 1
              not_understood = 1
                
            break
        
        lat = get_value(card, 'latitude')
        lon = get_value(card, 'longitude')
        if lat and lon:
          location = '('+str(lat)+'; '+str(lon)+')'

        pertinences = []
        for q in questions: 
          confidence = 0
          for component in questions[q]:
            rx = re.compile(r'\b'+component)
            if rx.search(content.lower()):
            #if component in content.lower():
              confidence += 1
          if confidence >= 2 and questions[q][0] in content.lower():
            pertinences.append(str(q))
        
        timePOSIX = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
        user_number = None

        if is_from.lower() in users_seen:
          user_number = users_seen.index(is_from.lower())
        else:
          users_seen.append(is_from.lower())
          user_number = len(users_seen) - 1

        if types[card['concept_id']] == 'tell':
          score = 1
          tokens = content.split(' ')
          for token in tokens:
            if token.lower() == 'and':
              score += 1
          if not reply_content or reply_content == '':
            reply_content = '[CE SAVED]'
            
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

        if types[card['concept_id']] == 'ask':
          question = 1
        cards_seen.add(card['name'])
        output = output + str(i)+','+exp_name.replace('/', '-')+',0,'+str(user_number)+','+is_from+','+card['name']+','+time+','+timePOSIX+','+types[card['concept_id']]+','+' '.join(pertinences)+','+content+','+location+','+str(pause)+','+reply_content+','+str(potential_score)+','+str(score)+','+str(response_time)+','+str(keystrokes)+','+str(blank)+','+str(empty)+','+str(failed)+','+str(mimic)+','+str(not_understood)+','+str(question)+'\n'
    
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
