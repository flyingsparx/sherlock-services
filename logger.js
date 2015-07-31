var http = require('http');
var PORT = 6666;
var MongoClient = require('mongodb').MongoClient;
MongoClient.connect('mongodb://127.0.0.1:27017/sherlock', function(dberr, db){
  var today = new Date();

  http.createServer(function(request, response){
      response.setHeader("Access-Control-Allow-Origin", "*");
      if(request.method == "GET" && request.url.indexOf("/cards") == 0){
        try{
          var components = request.url.split("/");
          var exp_name = components[2];
          var year = parseInt(components[3]);
          var month = parseInt(components[4])-1;
          var day = parseInt(components[5]);
          var collection = db.collection(exp_name+"-"+year+"-"+month+"-"+day);
          var cards = collection.find().toArray(function(err, docs){
            if(docs){
              response.end(JSON.stringify(docs));
            }   
          });
        }
        catch(err){
          console.log(err);
          response.end();
        }
      }
      else if(request.method == "POST" && request.url.indexOf("/cards") == 0){
          var body = "";
          request.on("data", function(chunk){
              body += chunk;
          });
          request.on("end", function(){
              try{
                var components = request.url.split("/");
                var exp_name = components[2];
                var collection = db.collection(exp_name+"-"+today.getFullYear()+"-"+today.getMonth()+"-"+today.getDate());
                collection.insert(JSON.parse(body));
              }
              catch(err){
                console.log(err); 
              }
              response.end();
          });
      }
  }).listen(PORT);

  console.log("Card-logger listening on port "+PORT+".");
});
