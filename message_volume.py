import json, time, datetime, urllib2, sys, os, re, math
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
  print 'Usage: python message_volume.py input.json'
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

def get_relationship(card, rel):
  if '_relationships' in card:
    for relationship in card['_relationships']:
      if relationship['label'] == rel:
        return relationship['target_name'] 
  elif 'relationships' in card:
    for relationship in card['relationships']:
      if relationship['label'] == rel:
        return relationship['target_name'] 
  elif rel in card:
    return card[rel]

def get_type(card):
  types = {
    11:'confirm card',
    10:'nl card',
    7:'tell card',
    8:'ask card',
    9:'gist card'
  }
  if 'type_id' in card:
    return types[card['type_id']]
  elif 'type' in card:
    return card['type']

def generate_card(name, timestamp):
  card = {}
  card['name'] = name
  card['timestamp'] = timestamp
  return card

def get_bucket(earliest, timestamp, interval_secs):
  diff = timestamp - earliest
  return math.floor(diff / interval_secs)

data = get_data()

earliest_time = None

seen_ids = []
all_ids = set()
buckets = {}
granularity = 5

for card in data:
  all_ids.add(card['name'])
  timestamp = get_value(card, 'timestamp')
  if timestamp and (earliest_time is None or ((int(timestamp) / 1000) < earliest_time)):
    earliest_time = int(timestamp) / 1000

# add any 'missing' NR cards
missing = []
for card in data:
  is_from = get_relationship(card, 'is from')
  content = get_value(card, 'content')
  if content is not None and is_from is not None and not ' agent' in is_from and not 'Sherlock' in is_from and not 'there is an agent named' in content:
    if get_type(card) == 'tell card':
      confirm_id = get_relationship(card, 'is in reply to')
      if confirm_id:
        timestamp = get_value(card, 'timestamp')
        if confirm_id not in all_ids:
          missing.append(generate_card(confirm_id, timestamp))
          missing.append(generate_card(confirm_id+'NR', timestamp))
        else:
          confirm_card = None
          for card2 in data:
            if card2['name'] == confirm_id:
              confirm_card = card2
              break
          nl_id = get_relationship(confirm_card, 'is in reply to')
          if nl_id not in all_ids:
            missing.append(generate_card(nl_id, timestamp))
for card in missing:
  data.append(card)

for card in data:
  timestamp = get_value(card, 'timestamp')
  if (card['name'], timestamp) not in seen_ids:
    seen_ids.append((card['name'], timestamp))
    if timestamp:
      timestamp = int(timestamp)/1000
      bucket = int(get_bucket(earliest_time, timestamp, 60*granularity))
      if bucket >= 0:
        if bucket not in buckets:
          buckets[bucket] = 0
        buckets[bucket] += 1
      else:
        print datetime.datetime.fromtimestamp(timestamp),
        print get_relationship(card, 'is from')

xs = []
ys = []
for bucket in buckets:
  xs.append(bucket*granularity)
  ys.append(buckets[bucket])

plt.plot(xs, ys, 'r-')
plt.ylabel('Number of messages generated')
plt.xlabel('Minutes since experiment start')
plt.show()
    
    
