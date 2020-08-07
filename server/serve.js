// this file is only used to create a standalone version of this application

const handler = require('serve-handler');
const http = require('http');
const child_process = require('child_process');
const path = require('path');


// welcome text
console.log("xx================================xx")
console.log("xx                                xx")
console.log("xx  Collegerama Offline Viewer    xx")
console.log("xx       made by djosh34          xx")
console.log("xx                                xx")
console.log("xx================================xx")
console.log("                          ")
console.log("Please go to http://localhost:3000")
console.log("                          ")



// starting static server

const server = http.createServer((request, response) => {
  return handler(request, response, {
      public: "build"
  });
})
 
server.listen(3000, () => {
    console.log('Running static server');

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

// console.log(serverExecPath);

var child = child_process.spawn('./index' + extension);

child.stdout.on('data', function(data) {
    console.log(data.toString());
});

child.stderr.on('data', function(data) {
    console.log(data.toString());
});