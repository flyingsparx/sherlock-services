import json, time, datetime, urllib2, sys, os

# Config:
granularity = 5

input_file = sys.argv[1]

questions = {
  1:['pineapple', 'eat|like','falcon pineapple'], # what character eats pineapples
  2:['finch', 'play', 'finch cricket'], # what sport does dr finch play
  3:['apple', 'eat|like', "the apple is with doctor finch",'finch apples','finch apple'], # what character eats apples
  4:['crane', 'wear|shirt'], # what shirt does prof crane wear
  5:['robin', 'in|room'], # where is col robin
  6:['stork', 'wear|shirt', 'storm', 'stork blue'], # what shirt does sgt stork wear
 29   7:['stork', 'in|room','sork amber', 'stork amber'], # where is stork
  8:['emerald', 'in', 'contents', 'hawk emerald', 'hawk is at the'], # what char in emerald room
  9:['banana', 'eat|like', 'crane bananas', 'crane baanana', 'crane ears'], # who eats bananas
  10:['sapphire', 'in', 'the room sapphire room has the character col robin as contents'], # what char in sapphire room
  11:['crane', 'play', 'crane rugby'], # what sport does crane play
  12:['red', 'wear|shirt'], # who wears red shirt
  13:['rugby', 'play','robin rugby'], # who plays rugby
  14:['hawk', 'eat|like', 'hawk pear','hawk pears'], # what fruit does rev hawk eat
  15:['robin', 'eat|like', 'orange', 'robin apple'], # what fruit does robin eat
  16:['finch', 'wear|shirt', 'finch green', 'finch has a green top'], # what shirt does finch wear
  17:['apple', 'in|room|silver'], # where is apple
  18:['yellow', 'wear|shirt','robin yellow'], # who wears yellow
  19:['silver', 'in', 'apple is in', "the fruit apple is in the location silver room"], # what fruit in silver room
  20:['black', 'wear|shirt', 'falcon black'], # who wears black
  21:['lemon', 'eat|like|loves', 'stork lemons', 'syork', 'stalk lemon'], # who eats lemons
  22:['crane', 'eat|like', 'crane bananas', 'crane banana', 'crane ears'], # what does crane eat
  23:['baseball', 'play', 'basebal','hawk emerald baseball'], # who plays baseball
  24:['soccer', 'play'], # who plays soccer
  25:['stork', 'play', 'stalk likes golf', 'storm likes golf', 'stork golf'], # what sport does stork play
  26:['ruby', 'contents', 'in','robin rugby','crane rugby'], # what char in ruby room
  27:['golf', 'plays', 'likes golf', 'stork golf'], # who plays golf
  28:['orange', 'eat|like', 'robin'], # who eats oranges
  29:['falcon', 'wear|shirt','falcon dark','falcon black'], # what shirt does falcon wear 
  30:['amber', 'contents', 'in', 'sork amber', 'stork amber'], # what char in amber room
  31:['crane', 'in|room'], # where is crane
  32:['pear', 'in|room', 'pear emerald'], # where is pear
  33:['stork', 'eat|like|loves', 'storm', 'syork', 'stork lemon','stalk lemon'], # what fruit does stork eat
  34:['robin', 'play', 'robin rugby'], # what sport does robin play
'falcon', 'in|room'], # where is falcon
  36:['falcon', 'play','falcon soccer'] # what sport does falcon play
}

question_nots = {
  1:['grape'],
  5:['named', 'orange'],
  19:['character','finch'],
  8:['pear'],
  26:['grape']
}

def get_data():
  if os.path.isfile(input_file):
    exp_file = open(input_file, 'r')
    data = []
    for line in exp_file.readlines():
      data.append(json.loads(line))
    exp_file.close()
    return data

data = get_data()

in_plays = []

for minute in data:
  print minute
  exit()
  
  pertinences = []
  
  stripped_content = content.lower().replace("'", "").replace(".", "")
  for q in questions:
    confidence = 0
    for component in questions[q]:
      rx = re.compile(r'\b'+component)
      add = True
      if rx.search(stripped_content):
        if q in question_nots:
          for no in question_nots[q]:
            if no in stripped_content:
              add = False
        if add:
          confidence += 1
    if confidence >= 2 and questions[q][0] in stripped_content:
      pertinences.append(str(q))

  in_plays.append(pertinences)
