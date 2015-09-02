# Script to convert JSON output from experiments into
# wide CSV format for processing by US Army Research Labs.

import json, time, datetime

exp_name = 'mid-150830'

nl_card_id = 10
tell_card_id = 7
ask_card_id = 8
gist_card_id = 9

def read_file():
  f = open(exp_name+'.json', 'r')
  data = f.read()
  f.close()
  return json.loads(data)

def get_value(card, val):
  for value in card['values']:
    if value['descriptor'] == val:
      return value['type_name'] 

def get_relationship(card, rel):
  for relationship in card['relationships']:
    if relationship['label'] == rel:
      return relationship['target_name'] 


def export(data):
  output = ',Exprun,asktell,uniqueid,expid,id,time,POSIXtime,content,location,pause,response,potentialscore,actualscore,timetorespond,keystrokes,\n'
  users_seen = []
  for i, card in enumerate(data):
    try:
      is_from = get_relationship(card, 'is from')
      if is_from and not ' agent' in is_from and not 'Sherlock' in is_from:
        # since in-reply_to not yet implemented, assuming response is the next card.
        reply = data[i+1]
        reply_timestamp = long(get_value(reply, 'timestamp'))
        reply_content = get_value(reply, 'content')
        timestamp = long(get_value(card, 'timestamp'))
        content = get_value(card, 'content').replace(',', '')
        keystrokes = ''
        pause = ''
        
        timePOSIX = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        time = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
        user_number = None
        score = 0
        if is_from.lower() in users_seen:
          user_number = users_seen.index(is_from.lower())
        else:
          users_seen.append(is_from.lower())
          user_number = len(users_seen) - 1
        if card['concept_id'] == tell_card_id:
          score = 1
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

        response_time = (float(reply_timestamp) - float(timestamp)) / 1000
        if content == reply_content:
          reply_content = '[CE SAVED]'
        

        output = output + str(i)+','+exp_name+',0,'+str(user_number)+','+is_from+','+card['name']+','+time+','+timePOSIX+','+content+',,'+str(pause)+','+reply_content+',,'+str(score)+','+','+str(response_time)+','+str(keystrokes)+'\n'
    
        #print output 
        #return
    except Exception as e:
      print e
  f = open(exp_name+'.csv', 'w')
  f.write(output)
  f.close()

data = read_file()
export(data)
