import json

types = {
  11:'confirm',
  10:'nl',
  7:'tell',
  8:'ask',
  9:'gist'
}

f = open('sherlock_run1+2.json', 'r')
seen = []
for line in f.readlines():
  data = json.loads(line)
  if data['name'] not in seen:
    seen.append(data['name'])
    content = ''
    for value in data['values']:
      if value['descriptor'] == 'content':
        content = value['type_name']
    for relationship in data['relationships']:
      if relationship['label'] == 'is from' or relationship['label'] == 'is to':
        if relationship['target_name'] == 'B':
          print types[data['concept_id']],data['name'],relationship['label'],content
