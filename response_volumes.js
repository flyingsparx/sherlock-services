/*
Generate transient ANSWERS for each question at each X minute of an 
experiment (data for which produced by combined_cards.py).

Requires combined_cards.py to output in 1 minute granularities (<data_file> below).

Generates output in CSV format for each question against time in X minute intervals.

Example use:
node response_volumes.js input.json > output.csv
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
  names = names + ',q' + (i+1) + ' '+ questions[i].text;
}
console.log(names);

for(var i = 0; i <= 60; i++){
  
  if(components[i]){
    for(var j = 0; j < components[i].length; j++){
      node.add_sentence(components[i][j].content, components[i][j].author);
    }
  }

  if (i % X == 0){
    var states = i+',';
    for(var j = 0; j < questions.length; j++){
      var q = questions[j];

      // Calculate all responses
      var concerns = node.instances[q.concerns.name.toLowerCase().replace(/ /, '_')];
      var property = q.relationship ? q.relationship : q.value;
      var properties = concerns.properties(property, false, true);
      var responses = {}; 
      for(var k = 0; k < properties.length; k++){
        var name = properties[k].instance.name;
        if(!(name in responses)){
          responses[name] = {};
          responses[name].count = 0;
          responses[name].blame = [];
        }
        responses[name].count++;
        responses[name].blame.push(properties[k].blame);
      }
      for(response in responses){
        states += response+' ('+responses[response].count+')' +'['+ responses[response].blame.join(';')+'] '
      }
      states += ','
    }
    console.log(states);
  }
}
process.exit();
