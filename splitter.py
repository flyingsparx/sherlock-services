# Split datasets by time (also removes cards sent from certain users)
#
# This is mostly useful for handling multiple Sherlock runs on the same day.

import json, sys, datetime

f = sys.argv[1]

startTime1 = datetime.datetime(2015, 12, 16, 11, 40)
endTime1 = datetime.datetime(2015, 12, 16, 12, 40)
startTime2 = datetime.datetime(2015, 12, 16, 12, 50)
endTime2 = datetime.datetime(2015, 12, 16, 13, 50)

ignore = ['alun']

exp_file = open(f, 'r')
data = []
for line in exp_file.readlines():
  data.append(json.loads(line))
exp_file.close()

def get_time(time):
  return (time - datetime.datetime(1970, 1, 1)).total_seconds()
startTime1 = get_time(startTime1)
startTime2 = get_time(startTime2)
endTime1 = get_time(endTime1)
endTime2 = get_time(endTime2)

def get_value(card, val):
  for value in card['_values']:
    if value['label'] == val:
      return value['type_name']

output1 = ''
output2 = ''

for card in data:
  timestamp = get_value(card, 'timestamp')
  if timestamp:
    timestamp = int(timestamp) / 1000
    if timestamp >= startTime1 and timestamp <= endTime1:
      output1 = output1 + json.dumps(card)+'\n'
    if timestamp >= startTime2 and timestamp <= endTime2:
      output2 = output2 + json.dumps(card)+'\n'

f1 = open('run1.json', 'w')
f1.write(output1)
f1.close()
f2 = open('run2.json', 'w')
f2.write(output2)
f2.close()
