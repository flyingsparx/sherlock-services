# Combine all tell cards from each experiment (separated by time)
# into distinct buckets (e.g. these are all the tell cards sent at
# 13 minutes). Assumes all valid inputs to node are made through
# tell cards (which seems to be the case).
#
# Example use:
# python combined_cards.py <exp> > data.js

import json, time, datetime, urllib2, sys, os, re, math

if len(sys.argv) != 2:
  print 'Usage: python combined_cards.py logURL'
  exit()
exp_name = sys.argv[1]

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
  for value in card['_values']:
    if value['label'] == val:
      return value['type_name'] 

def get_relationship(card, rel):
  for relationship in card['_relationships']:
    if relationship['label'] == rel:
      return relationship['target_name'] 

def get_bucket(earliest, timestamp, interval_secs):
  diff = timestamp - earliest
  return math.floor(diff / interval_secs)

data = get_data()
seen_ids = []
buckets = {}
granularity = 1

earliest_time = 1450098000

for card in data:
  timestamp = get_value(card, 'timestamp')
  if (card['name'], timestamp) not in seen_ids and card['type_id'] == 7:
    seen_ids.append((card['name'], timestamp))
    if timestamp:
      timestamp = int(timestamp)/1000
      bucket = int(get_bucket(earliest_time, timestamp, 60*granularity))
      if bucket not in buckets:
        buckets[bucket] = []
      buckets[bucket].append(get_value(card, 'content'))

print 'exports.states = {'
for i in range(50):
  print '  ',i,': ['
  if i in buckets:
    for card in buckets[i]:
      print '    "',card+'",'
  print '    ],'
print '  },'
