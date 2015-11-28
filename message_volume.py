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
  for value in card['values']:
    if value['descriptor'] == val:
      return value['type_name'] 

def get_relationship(card, rel):
  for relationship in card['relationships']:
    if relationship['label'] == rel:
      return relationship['target_name'] 

def get_bucket(earliest, timestamp, interval_secs):
  diff = timestamp - earliest
  return math.floor(diff / interval_secs)

data = get_data()

experiments = { # 08/10/15
  0: (1444309800, 1444312800, 'r-'),  # 14:10-15:00 (BST)
  1: (1444313400, 1444316400, 'b-')   # 15:10-16:00 (BST)
}

seen_ids = []
buckets = {}
granularity = 1

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

# cumulative
#for y in ys:
#  for i, number in enumerate(y):
#    if i < len(y) - 1:
#      y[i+1] = y[i+1] + y[i]

plt.plot(xs[0], ys[0], experiments[0][2], xs[1], ys[1], experiments[1][2])
plt.ylabel('Number of messages generated')
plt.xlabel('Minutes since experiment start')
plt.show()
    
    
