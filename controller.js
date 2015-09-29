var http = require('http');
var exec = require('child_process').exec

var PORT = 8888;

http.createServer(function(request, response){
    if(request.url == '/' && request.method == 'GET'){
      response.end('<html><body><h2>Mycroft</h2><a href="/restart-mycroft">Restart (or just start) Mycroft service</a><h2>Verity</h2><a href="/restart-verity">Restart (or just start) Verity service</a></body></html>');
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
                    response.end('<html><body>Mycroft restarted. Manage Mycroft at <a href="http://mycroft.cenode.io">mycroft.cenode.io</a>.</body></html>');
                });
            });
        });
    }
    else if(request.url == '/restart-verity' && request.method == 'GET'){
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
}).listen(PORT);

console.log("Control listener running on port "+PORT+".");
