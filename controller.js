var http = require('http');
var exec = require('child_process').exec
var url = require('url');

var PORT = 8888;

http.createServer(function(request, response){
    if(request.method != 'GET'){
      response.writeHead('405');
      response.end();
      return;
    }
    if(request.url == '/' || request.url.indexOf('/?') == 0){
      console.log(new Date(), 'Homepage');
      var status = url.parse(request.url, true).query.status;
      var html = '<html><body><h2>Mycroft</h2><a href="/restart-mycroft">Restart (or just start) Mycroft service</a><br /><a href="/stop-mycroft">Stop Mycroft</a><h2>Verity</h2><a href="/restart-verity">Restart (or just start) Verity service</a><br /><a href="/stop-verity">Stop Verity</a></body>';
      if(status && status != ''){
        html += '<script>window.alert("'+status+'");</script>';
      }
      response.end(html+'</html>');
    }
    else if(request.url.indexOf('/start-mycroft') == 0 || request.url.indexOf('/restart-mycroft') == 0){
        console.log(new Date(), "Killing Mycroft");
        exec('tmux kill-session -t mycroft', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
            console.log(new Date(), stdout1);
            console.log(new Date(), "Launching new Mycroft session.");
            exec('tmux new-session -s mycroft -d', {cwd: '/home/apps'}, function(err, stdout, stderr){
                console.log(new Date(), stdout);
                console.log(new Date(), "Starting Mycroft.");
                exec('tmux send-keys -t mycroft "node CENode/cenode.js Mycroft" C-m', {cwd: '/home/apps'}, function(e3, st3, std3){
                    if(err){
                        console.log(new Date(), err);
                    }
                    if(stderr){
                        console.log(new Date(), stderr);
                    }
                    console.log(new Date(), stdout);
                    response.writeHead(301, {Location: '/?status=Mycroft is now running.'});
                    response.end();
                });
            });
        });
    }
    else if(request.url.indexOf('/stop-mycroft') == 0){
        console.log(new Date(), "Killing Mycroft");
        exec('tmux kill-session -t mycroft', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
           console.log(new Date(), 'Killed'); 
           response.writeHead(301, {Location: '/?status=Stopped Mycroft'});
           response.end();
        });
    }
    else if(request.url.indexOf('/start-verity') == 0 || request.url.indexOf('/restart-verity') == 0){
        console.log(new Date(), "Killing Verity");
        exec('tmux kill-session -t verity', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
            console.log(new Date(), stdout1);
            console.log(new Date(), "Launching new Verity session.");
            exec('tmux new-session -s verity -d', {cwd: '/home/apps'}, function(err, stdout, stderr){
                console.log(new Date(), stdout);
                console.log(new Date(), "Starting Verity.");
                exec('tmux send-keys -t verity "node CENode/cenode.js Verity 7654" C-m', {cwd: '/home/apps'}, function(e3, st3, std3){
                    if(err){
                        console.log(new Date(), err);
                    }
                    if(stderr){
                        console.log(new Date(), stderr);
                    }
                    console.log(new Date(), stdout);
                    response.writeHead(301, {Location: '/?status=Verity is now running.'});
                    response.end();
                });
            });
        });
    }
    else if(request.url.indexOf('/stop-verity') == 0){
        console.log(new Date(), "Killing Verity");
        exec('tmux kill-session -t verity', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
          console.log(new Date(), 'Killed'); 
          response.writeHead(301, {Location: '/?status=Stopped Verity'});
          response.end();
        });
    }
}).listen(PORT);

console.log(new Date(), "Control listener running on port "+PORT+".");
