var http = require('http');
var PORT = 6666;
var MongoClient = require('mongodb').MongoClient;
MongoClient.connect('mongodb://127.0.0.1:27017/sherlock', function(dberr, db){
  var today = new Date();
  var collection = db.collection(today.getFullYear()+"-"+today.getMonth()+"-"+today.getDate());

  http.createServer(function(request, response){
      response.setHeader("Access-Control-Allow-Origin", "*");
      if(request.method == "GET" && request.url.indexOf("/cards") == 0){
        try{
          var components = request.url.split("/");
          var year = parseInt(components[2]);
          var month = parseInt(components[3])-1;
          var day = parseInt(components[4]);
          var collection2 = db.collection(year+"-"+month+"-"+day);
          console.log("Connected to "+year+"-"+month+"-"+day); 
          var cards = collection2.find().toArray(function(err, docs){
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
      else if(request.method == "POST" && request.url == "/cards"){
          var body = "";
          request.on("data", function(chunk){
              body += chunk;
          });
          request.on("end", function(){
              try{
                console.log(body);
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
