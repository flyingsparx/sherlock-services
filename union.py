#!/usr/bin/python
#

import json, time, datetime, urllib2, sys, os, re

if len(sys.argv) != 4:
  print 'Usage: python union.py input1.json input2.json output.json'
  exit()

file1 = sys.argv[1]
file2 = sys.argv[2]
out_file = sys.argv[3]

def get_data(exp_name):
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

data1 = get_data(file1)
data2 = get_data(file2)

print file1,"length = ",len(data1)
print file2,"length = ",len(data2)

output = []

seen_ids = set()

added1 = 0
added2 = 0
conflict = 0
for entry in data1:
  if entry['name'] not in seen_ids:
    output.append(entry)
    added1+=1
  seen_ids.add(entry['name'])

for entry in data2:
  if entry['name'] not in seen_ids:
    output.append(entry)
    added2+=1
  else:
    conflict+=1
  seen_ids.add(entry['name'])

print "added",added1,"files from",file1
print "added",added2,"files from",file2
print "length of output file",len(output)
print conflict,"conflicting entries"

out_writer = open(out_file, 'w')
for entry in output:
  out_writer.write(json.dumps(entry))
out_writer.close()
