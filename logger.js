var http = require('http');
var PORT = 6666;
var MongoClient = require('mongodb').MongoClient;
MongoClient.connect('mongodb://127.0.0.1:27017/sherlock', function(dberr, db){

  http.createServer(function(request, response){
      response.setHeader("Access-Control-Allow-Origin", "*");
      if(request.method == "POST" && request.url.indexOf("/cards") == 0){
          console.log(new Date(), 'POST', request.url);
          var body = "";
          request.on("data", function(chunk){
              body += chunk;
          });
          request.on("end", function(){
              try{
                var today = new Date();
                var components = request.url.split("/");
                var exp_name = components[2];
                var collection = db.collection(exp_name+"-"+today.getFullYear()+"-"+today.getMonth()+"-"+today.getDate());
                collection.insert(JSON.parse(body));
              }
              catch(err){
                console.log(new Date(), err); 
              }
              response.end();
          });
      }
  }).listen(PORT);

  console.log(new Date(), "Card-logger listening on port "+PORT+".");
});
