# Split datasets by time (also removes cards sent from certain users)
#
# This is mostly useful for extracting a handling multiple Sherlock runs on the same day and extracts only the cards for a specific run by time.
#
# usage:
# python splitter.py input.json output.json

import json, sys, datetime

f = sys.argv[1]
out = sys.argv[2]

#run 3: 14/12/2015 13:00-14:00
#run 4: 16/12/2015 11:40-12:40
#run 5: 16/12/2015 12:50-13:50
startTime1 = datetime.datetime(2015, 12, 16, 12, 50)
endTime1 = datetime.datetime(2015, 12, 16, 13, 50)

ignore = ['alun', 'cat', 'cat2', 'cat3', 'egg', 'dove', 'bug', 'goa']

exp_file = open(f, 'r')
data = []
for line in exp_file.readlines():
  data.append(json.loads(line))
exp_file.close()

def get_time(time):
  return (time - datetime.datetime(1970, 1, 1)).total_seconds()
startTime1 = get_time(startTime1)
endTime1 = get_time(endTime1)

def get_value(card, val):
  for value in card['_values']:
    if value['label'] == val:
      return value['type_name']
def get_relationship(card, relationship):
  for rel in card['_relationships']:
    if rel['label'] == relationship:
      return rel['target_name']

output1 = ''

for card in data:
  is_from = get_relationship(card, 'is from')
  if is_from and is_from.lower() in ignore:
    continue
  timestamp = get_value(card, 'timestamp')
  if timestamp:
    timestamp = int(timestamp) / 1000
    if timestamp >= startTime1 and timestamp <= endTime1:
      output1 = output1 + json.dumps(card)+'\n'

f1 = open(out, 'w')
f1.write(output1)
f1.close()
