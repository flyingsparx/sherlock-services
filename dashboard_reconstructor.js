/*
Generate transient states for each question at each minute of an 
experiment (data for which produced by combined_cards.py).
Each state is unanswered, unconfident, answered, or contested.

Requires combined_cards.py to output in 1 minute granularities.

Generates output in CSV format for each question against time in X minute intervals.

Example use:
node dashboard_reconstructor.js > dashboard.csv
*/

var lib = require('../CENode/cenode.js');
var models = require('../model.js');
var states = require('../data.js').states;
var node = new lib.CENode(lib.MODELS.CORE, models.SHERLOCK_CORE);
var X = 5;

var exp = states.experiment0;

var questions = node.concepts.question.instances;

// Write CSV header
var names = 'MINS';
for(var i = 0; i < questions.length; i++){
  names = names + ',' + questions[i].name;
}
console.log(names);

for(var i = 0; i < 50; i++){
  node.add_sentences(exp[i]);
  if (i % X == 0){
    var instances = node.concepts.sherlock_thing.instances;
    var states = i + '-' + (i+(X-1));
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
