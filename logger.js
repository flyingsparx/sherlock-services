var http = require('http');
var PORT = 6666;
var MongoClient = require('mongodb').MongoClient;
MongoClient.connect('mongodb://127.0.0.1:27017/sherlock', function(err, db){
  var today = new Date();
  var collection = db.collection(today.getFullYear()+"-"+today.getMonth()+"-"+today.getDate());

  http.createServer(function(request, response){
      response.setHeader("Access-Control-Allow-Origin", "*");
      if(request.method == "POST" && request.url == "/cards"){
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
