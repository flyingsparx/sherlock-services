var http = require('http');
var exec = require('child_process').exec

var PORT = 8888;

http.createServer(function(request, response){
    if(request.method != 'GET'){
      response.writeHead('405');
      response.end();
      return;
    }
    if(request.url == '/'){
      response.end('<html><body><h2>Mycroft</h2><a href="/restart-mycroft">Restart (or just start) Mycroft service</a><br /><a href="/stop-mycroft">Stop Mycroft</a><h2>Verity</h2><a href="/restart-verity">Restart (or just start) Verity service</a><br /><a href="/stop-verity">Stop Verity</a></body></html>');
    }
    else if(request.url == '/start-mycroft' || request.url == '/restart-mycroft'){
        console.log("Killing Mycroft");
        exec('tmux kill-session -t mycroft', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
            console.log(stdout1);
            console.log("Launching new Mycroft session.");
            exec('tmux new-session -s mycroft -d', {cwd: '/home/apps'}, function(err, stdout, stderr){
                console.log(stdout);
                console.log("Starting Mycroft.");
                exec('tmux send-keys -t mycroft "node CENode/cenode.js Mycroft" C-m', {cwd: '/home/apps'}, function(e3, st3, std3){
                    if(err){
                        console.log(err);
                    }
                    if(stderr){
                        console.log(stderr);
                    }
                    console.log(stdout);
                    response.end('<html><body>Mycroft is now running. Manage Mycroft at <a href="http://mycroft.cenode.io">mycroft.cenode.io</a>.</body></html>');
                });
            });
        });
    }
    else if(request.url == '/stop-mycroft'){
        console.log("Killing Mycroft");
        exec('tmux kill-session -t mycroft', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
           console.log('Killed'); 
           response.writeHead(301, {Location: '/'});
           response.end();
        });
    }
    else if(request.url == '/start-verity' || request.url == '/restart-verity'){
        console.log("Killing Verity");
        exec('tmux kill-session -t verity', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
            console.log(stdout1);
            console.log("Launching new Verity session.");
            exec('tmux new-session -s verity -d', {cwd: '/home/apps'}, function(err, stdout, stderr){
                console.log(stdout);
                console.log("Starting Verity.");
                exec('tmux send-keys -t verity "node CENode/cenode.js Verity 7654" C-m', {cwd: '/home/apps'}, function(e3, st3, std3){
                    if(err){
                        console.log(err);
                    }
                    if(stderr){
                        console.log(stderr);
                    }
                    console.log(stdout);
                    response.end('<html><body>Verity restarted. Manage Verity at <a href="http://verity.cenode.io">verity.cenode.io</a>.</body></html>');
                });
            });
        });
    }
    else if(request.url == '/stop-verity'){
        console.log("Killing Verity");
        exec('tmux kill-session -t verity', {cwd: '/home/apps'}, function(err1, stdout1, stderr1){
          console.log('Killed'); 
          response.writeHead(301, {Location: '/'});
          response.end();
        });
    }
}).listen(PORT);

console.log("Control listener running on port "+PORT+".");
