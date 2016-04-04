# Split datasets by time (also removes cards sent from certain users)
#
# This is mostly useful for extracting a handling multiple Sherlock runs on the same day and extracts only the cards for a specific run by time.
#
# usage:
# python splitter.py input.json output.json

import json, sys, datetime

f = sys.argv[1]
out = sys.argv[2]

#run 1: 08/10/2015 14:00-15:00 (consider BST - use an hour earlier)
#run 2: 08/10/2015 15:10-16:00 (consider BST - use an hour earlier)
#run 3: 14/12/2015 13:00-14:00
#run 4: 16/12/2015 11:40-12:40
#run 5: 16/12/2015 12:50-13:50
#run 6: 04/02/2016 15:10-16:10
#run 7: 04/02/2016 16:11-17:10
#run 8: 10/02/2016 11:55-12:45
#cwrun1: 02/03/2016 10:00-11:00
start = datetime.datetime(2016, 2, 4, 15, 10)
end = datetime.datetime(2016, 2, 4, 16, 10)

ignore = [] # List of users to exclude

exp_file = open(f, 'r')
data = []
for line in exp_file.readlines():
  data.append(json.loads(line))
exp_file.close()

def get_time(time):
  return (time - datetime.datetime(1970, 1, 1)).total_seconds()
start = get_time(start)
end = get_time(end)

def get_value(card, val):
  if '_values' in card:
    for value in card['_values']:
      if value['label'] == val:
        return value['type_name']
  elif 'values' in card:
    for value in card['values']:
      if value['descriptor'] == val:
        return value['type_name']
  elif val in card:
    return card[val]

def put_timestamp(card, val):
  try:
    for value in card['values']:
      if value['descriptor'] == 'timestamp':
        value['type_name'] = str(val)
  except:
    pass

def get_relationship(card, relationship):
  if '_relationships' in card:
    for rel in card['_relationships']:
      if rel['label'] == relationship:
        return rel['target_name']
  elif 'relationships' in card:
    for rel in card['relationships']:
      if rel['label'] == relationship:
        return rel['target_name']
  elif relationship in card:
    return card[relationship]


output1 = ''

for card in data:
  is_from = get_relationship(card, 'is from')
  timestamp = get_value(card, 'timestamp')
  #if timestamp and is_from and is_from.lower() == 'doe':
  #  timestamp = int(timestamp) - 1000 * 60 * 60
  #  put_timestamp(card, timestamp)
  #if timestamp and is_from and is_from.lower() == 'snow':
  #  timestamp = int(timestamp) + 1000 * 60 * 60 * 7
  #  put_timestamp(card, timestamp)

  if timestamp:
    timestamp = int(timestamp) / 1000
    if timestamp >= start and timestamp <= end:
      output1 = output1 + json.dumps(card)+'\n'

f1 = open(out, 'w')
f1.write(output1)
f1.close()
