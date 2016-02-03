#!/usr/bin/python
#
# Script to convert JSON output from experiments into
# wide CSV format for processing by US Army Research Labs.

import json, time, datetime, urllib2, sys, os, re

if len(sys.argv) != 2:
  print 'Usage: python csv_converter.py logURL'
  exit()

exp_name = sys.argv[1]

card_types = {
  11:'confirm card',
  10:'nl card',
  7:'tell card',
  8:'ask card',
  9:'gist card'
}

questions = {
  1:['pineapple', 'eat|like','falcon pineapple'], # what character eats pineapples
  2:['finch', 'play', 'finch cricket'], # what sport does dr finch play
  3:['apple', 'eat|like', "the apple is with doctor finch",'finch apples','finch apple'], # what character eats apples
  4:['crane', 'wear|shirt'], # what shirt does prof crane wear
  5:['robin', 'in|room'], # where is col robin
  6:['stork', 'wear|shirt', 'storm', 'stork blue'], # what shirt does sgt stork wear
  7:['stork', 'in|room','sork amber', 'stork amber'], # where is stork
  8:['emerald', 'in', 'contents', 'hawk emerald', 'hawk is at the'], # what char in emerald room
  9:['banana', 'eat|like', 'crane bananas', 'crane baanana', 'crane ears'], # who eats bananas
  10:['sapphire', 'in', 'the room sapphire room has the character col robin as contents'], # what char in sapphire room
  11:['crane', 'play', 'crane rugby'], # what sport does crane play
  12:['red', 'wear|shirt'], # who wears red shirt
  13:['rugby', 'play','robin rugby'], # who plays rugby
  14:['hawk', 'eat|like', 'hawk pear','hawk pears'], # what fruit does rev hawk eat
  15:['robin', 'eat|like', 'orange', 'robin apple'], # what fruit does robin eat
  16:['finch', 'wear|shirt', 'finch green', 'finch has a green top'], # what shirt does finch wear
  17:['apple', 'in|room|silver'], # where is apple
  18:['yellow', 'wear|shirt','robin yellow'], # who wears yellow
  19:['silver', 'in', 'apple is in', "the fruit apple is in the location silver room"], # what fruit in silver room
  20:['black', 'wear|shirt', 'falcon black'], # who wears black
  21:['lemon', 'eat|like|loves', 'stork lemons', 'syork', 'stalk lemon'], # who eats lemons
  22:['crane', 'eat|like', 'crane bananas', 'crane banana', 'crane ears'], # what does crane eat
  23:['baseball', 'play', 'basebal','hawk emerald baseball'], # who plays baseball
  24:['soccer', 'play'], # who plays soccer
  25:['stork', 'play', 'stalk likes golf', 'storm likes golf', 'stork golf'], # what sport does stork play
  26:['ruby', 'contents', 'in','robin rugby','crane rugby'], # what char in ruby room
  27:['golf', 'plays', 'likes golf', 'stork golf'], # who plays golf
  28:['orange', 'eat|like', 'robin'], # who eats oranges
  29:['falcon', 'wear|shirt','falcon dark','falcon black'], # what shirt does falcon wear 
  30:['amber', 'contents', 'in', 'sork amber', 'stork amber'], # what char in amber room
  31:['crane', 'in|room'], # where is crane
  32:['pear', 'in|room', 'pear emerald'], # where is pear
  33:['stork', 'eat|like|loves', 'storm', 'syork', 'stork lemon','stalk lemon'], # what fruit does stork eat
  34:['robin', 'play', 'robin rugby'], # what sport does robin play
  35:['falcon', 'in|room'], # where is falcon
  36:['falcon', 'play','falcon soccer'] # what sport does falcon play
}

question_nots = {
  1:['grape'],
  5:['named', 'orange'],
  19:['character','finch'],
  8:['pear'],
  26:['grape']
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
  if '_values' in card: # CENode 2
    for value in card['_values']:
      if value['label'] == val:
        return value['type_name'] 
  elif 'values' in card: # CENode 1
    for value in card['values']:
      if value['descriptor'] == val:
        return value['type_name'] 
  elif val in card:
    return card[val]
    

def get_relationship(card, rel):
  if '_relationships' in card: # CENode 2
    for relationship in card['_relationships']:
      if relationship['label'] == rel:
        return relationship['target_name'] 
  elif 'relationships' in card: # CENode 1
    for relationship in card['relationships']:
      if relationship['label'] == rel:
        return relationship['target_name'] 
  elif rel in card:
    return card[rel]

def get_type(card):
  if 'type_id' in card: # CENode 2
    return card_types[card['type_id']]
  elif 'concept_id' in card: # CENode 1
    return card_types[card['concept_id']]
  elif 'type' in card:
    return card['type']

def generate_csv(data):
  output = ',Exprun,asktell,uniqueid,expid,id,time,POSIXtime,type,aboutqs,content,location,pause,response,potentialscore,actualscore,timetorespond,keystrokes,Blank,Empty,Failed,Mimic,Not-understood,Question\n'
  users_seen = []
  cards_seen = set()
  all_ids = set()
  for card in data:
    all_ids.add(card['name'])
  for i, card in enumerate(data):
#    try:
      is_from = get_relationship(card, 'is from')
      content = get_value(card, 'content')
      seen_timestamp = get_value(card, 'timestamp')
      if content is not None and is_from and not ' agent' in is_from and not 'Sherlock' in is_from and (card['name'], seen_timestamp) not in cards_seen and not 'there is an agent named' in content:
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
            if get_type(reply) == 'confirm card':
              potential_score = 1
            elif content == reply_content:
              reply_content = '[CE SAVED]'
              score = 1
              if get_type(card) == 'nl card':
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
        stripped_content = content.lower().replace("'", "").replace(".", "")
        for q in questions: 
          confidence = 0
          for component in questions[q]:
            rx = re.compile(r'\b'+component)
            add = True
            if rx.search(stripped_content):
              if q in question_nots:
                for no in question_nots[q]:
                  if no in stripped_content:
                    add = False 
              if add: 
                confidence += 1
          if confidence >= 2 and questions[q][0] in stripped_content:
            pertinences.append(str(q))
        
        timePOSIX = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
        user_number = None

        if is_from.lower() in users_seen:
          user_number = users_seen.index(is_from.lower())
        else:
          users_seen.append(is_from.lower())
          user_number = len(users_seen) - 1

        if get_type(card) == 'tell card':
          score = 1
          tokens = content.split(' ')
          confirm_id = get_relationship(card, 'is in reply to')

          for token in tokens:
            if token.lower() == 'and':
              score += 1
          if not reply_content or reply_content == '':
            reply_content = '[CE SAVED]'

          # If we don't have a confirm card for this chain
          if not confirm_id in all_ids:
            # If we don't have an NL
            output = output + str(i)+'-NR'+','+exp_name.replace('/','-')+',0,'+str(user_number)+','+is_from+','+card['name']+'-NR,'+time+','+timePOSIX+','+'nl'+','+' '.join(pertinences)+','+'<assumed NL input>'+','+location+',,'+content+','+str(score)+',,,,0,0,0,0,0,0\n'
          # if we don't have an nl card for this chain
          else:
            confirm_card = None
            for card2 in data:
              if card2['name'] == confirm_id:
                confirm_card = card2
                break
            if card2:
              nl_id = get_relationship(confirm_card, 'is in reply to')
              if nl_id not in all_ids:
                output = output + str(i)+'-NR'+','+exp_name.replace('/','-')+',0,'+str(user_number)+','+is_from+','+card['name']+'-NR,'+time+','+timePOSIX+','+'nl'+','+' '.join(pertinences)+','+'<assumed NL input>'+','+location+',,'+content+','+str(score)+',,,,0,0,0,0,0,0\n'

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

        if get_type(card) == 'ask card':
          question = 1

        cards_seen.add((card['name'], seen_timestamp))
        output = output + str(i)+','+exp_name.replace('/', '-')+',0,'+str(user_number)+','+is_from+','+card['name']+','+time+','+timePOSIX+','+get_type(card)+','+' '.join(pertinences)+','+content+','+location+','+str(pause)+','+reply_content+','+str(potential_score)+','+str(score)+','+str(response_time)+','+str(keystrokes)+','+str(blank)+','+str(empty)+','+str(failed)+','+str(mimic)+','+str(not_understood)+','+str(question)+'\n'
    
    #except Exception as e:
    #   print e
  return output

def write_csv(csv):
  f = open(exp_name.replace('/', '-')+'.csv', 'w')
  f.write(csv)
  f.close()

data = get_data()
csv = generate_csv(data)
write_csv(csv)
