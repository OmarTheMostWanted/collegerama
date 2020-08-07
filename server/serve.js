// this file is only used to create a standalone version of this application

const handler = require('serve-handler');
const http = require('http');
const child_process = require('child_process');
const path = require('path');




// starting static server

const server = http.createServer((request, response) => {
  return handler(request, response, {
      public: "build"
  });
})
 
server.listen(3000, () => {
    console.log('Running Static server at http://localhost:3000');

});

// checking for windows

let extension = "";

if (process.platform === "win32") {
    extension = ".exe";
}

// starting dynamic server

var serverExecPath = path.join(__dirname,'./index.js');

if (!serverExecPath.includes("server")) {
    serverExecPath = path.join(__dirname,'./server/index.js');
}

console.log(serverExecPath);

var child = child_process.spawn('./index' + extension);

child.stdout.on('data', function(data) {
    console.log(data.toString());
});

child.stderr.on('data', function(data) {
    console.log(data.toString());
});