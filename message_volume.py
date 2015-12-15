import json, time, datetime, urllib2, sys, os, re, math
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
  print 'Usage: python csv_converter.py logURL'
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

def generate_card(name, timestamp):
  card = {}
  card['name'] = name
  card['values'] = []
  card['values'].append({'label':'timestamp', 'type_name':timestamp})
  return card

def get_bucket(earliest, timestamp, interval_secs):
  diff = timestamp - earliest
  return math.floor(diff / interval_secs)

data = get_data()

experiments = { # 08/10/15
  0: (1444309800, 1444312800, 'r-'),  # 14:10-15:00 (BST)
  1: (1444313400, 1444316400, 'b-')   # 15:10-16:00 (BST)
}

seen_ids = []
all_ids = set()
buckets = {}
granularity = 1

for card in data:
  all_ids.add(card['name'])

print len(data)

# add any 'missing' NR cards
missing = []
for card in data:
  is_from = get_relationship(card, 'is from')
  content = get_value(card, 'content')
  if is_from and not ' agent' in is_from and not 'Sherlock' in is_from and not 'there is an agent named' in content:
    if card['concept_id'] == 7:
      confirm_id = get_relationship(card, 'is in reply to')
      if not confirm_id:
        print card
        exit()

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
      experiment = -1
      for exp in experiments:
        if timestamp >= experiments[exp][0] and timestamp <= experiments[exp][1]:
          experiment = exp
          break
      if experiment != -1:
        if experiment not in buckets:
          buckets[experiment] = {}
        bucket = int(get_bucket(experiments[experiment][0], timestamp, 60*granularity))
        if bucket not in buckets[experiment]:
          buckets[experiment][bucket] = 0
        buckets[experiment][bucket] += 1

xs = []
ys = []
for experiment in buckets:
  xs.append([])
  ys.append([])
  for bucket in buckets[experiment]:
    xs[experiment].append(bucket*granularity)
    ys[experiment].append(buckets[experiment][bucket])

for y in ys[0]:
  print y

plt.plot(xs[0], ys[0], experiments[0][2], xs[1], ys[1], experiments[1][2])
plt.ylabel('Number of messages generated')
plt.xlabel('Minutes since experiment start')
plt.show()
    
    
