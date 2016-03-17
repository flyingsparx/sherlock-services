/*
Generate transient states for each question at each X minute of an 
experiment (data for which produced by combined_cards.py).
Each state is unanswered, unconfident, answered, or contested.

Requires combined_cards.py to output in 1 minute granularities (<data_file> below).

Generates output in CSV format for each question against time in X minute intervals.

Example use:
node dashboard_reconstructor.js <data_file> > dashboard.csv
*/

// Config:
var X = 1; // Mins granularity
var model = './model.js' // Model to preload KB with (usually contains characters/questions etc.)

var lib = require('../CENode/cenode.js');
var models = require(model);
var components = require(process.argv[2]);
var node = new lib.CENode(lib.MODELS.CORE, models.SHERLOCK_CORE);

var questions = node.concepts.question.instances;

// Write CSV header
var names = 'MINS';
for(var i = 0; i < questions.length; i++){
  names = names + ',q' + (i+1);
}

for(var i = 0; i <= 50; i++){
  if(components[i]){
    for(var j = 0; j < components[i].length; j++){
      node.add_sentence(components[i][j].content);
    }
  }

  if (i % X == 0){
    var states = i;
    for(var j = 0; j < questions.length; j++){
      var q = questions[j];

      // Calculate all responses
      var concerns = node.instances[q.concerns.name.toLowerCase().replace(/ /, '_')];
      var property = q.relationship ? q.relationship : q.value;
      var properties = concerns.properties(property);
      var responses = {}; 
      for(var k = 0; k < properties.length; k++){
        var n = properties[k].name;
        if(!(n in responses)){
          responses[n] = 0;
        }
        responses[n]++;
      }

      // Calculate most frequent two responses
      var highest = 0;
      var highest_prop;
      var prev_highest = 0;
      for(key in responses){
        if(responses[key] > highest){
          highest = responses[key];
          highest_prop = key;
        }
      }
      for(key in responses){
        if(key != highest_prop && responses[key] > prev_highest){
          prev_highest = responses[key];
        }
      }

      // Calculate state
      if(highest == 0){
        q.state = 'unanswered';
      }
      else if(highest < 3){
        q.state = 'unconfident';
      }
      else if((highest - prev_highest) >=3 ){
        q.state = 'answered';
      }
      else{
        q.state = 'contested';
      }
      states = states + ',' + q.state;
    }
    console.log(states);
  }
}
process.exit();
