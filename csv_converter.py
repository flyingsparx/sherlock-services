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

def export(data):
  output = ',Exprun,asktell,uniqueid,expid,id,time,POSIXtime,content,location,pause,response,potentialscore,actualscore,timetorespond,keystrokes\n'
  users_seen = []
  for i, card in enumerate(data):
    try:
      timestamp = None
      is_from = None
      user_number = None
      for value in card['values']:
        if value['descriptor'] == 'timestamp':
          timestamp = int(value['type_name']) / 1000
      for rel in card['relationships']:
        if rel['label'] == 'is from':
          is_from = rel['target_name']
      
      if is_from.lower() in users_seen:
        user_number = users_seen.index(is_from.lower())
      else:
        users_seen.append(is_from.lower())
        user_number = len(users_seen) - 1

      output = output + str(i)+','+exp_name+',0,'+str(user_number)+','+is_from+'\n'
      
    except:
      pass
  f = open(exp_name+'.csv', 'w')
  f.write(output)
  f.close()

data = read_file()
export(data)
