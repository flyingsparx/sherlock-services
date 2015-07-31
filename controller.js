var http = require('http');
var exec = require('child_process').exec

var PORT = 8888;

http.createServer(function(request, response){
    if(request.url == '/' && request.method == 'GET'){
      response.end('<html><body><h2>Mycroft</h2><a href="/restart-mycroft">Restart (or just start) Mycroft service</a></body></html>');
    }
    else if(request.url == '/restart-mycroft' && request.method == 'GET'){
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
                    response.end('Mycroft restarted. Manage Mycroft at <a href="http://mycroft.cenode.io">mycroft.cenode.io</a>.');
                });
            });
        });
    }
}).listen(PORT);

console.log("Control listener running on port "+PORT+".");
