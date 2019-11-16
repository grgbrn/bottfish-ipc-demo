// assume there are two named pipes already created
// named 'input' and 'output'
// node will write json from the network to 'input'
// and then wait for another process to write a response
// to the 'output' pipe

const http = require('http')
const fs = require('fs');
const path = require('path');


const port = 3000

// XXX ok these names don't make a lot of sense
// from node's perspective

const inputPipe = fs.createWriteStream("input", {
    flags: fs.O_WRONLY | fs.O_APPEND

})
const outputPipe = fs.createReadStream("output")

/*
outputPipe.on('data', data => {
  // process data...
});
*/

let requestHandler = async (request, response) => {
    console.log(request.url)

    if (request.method == 'POST') {
        var body = '';

        request.on('data', function (data) {
            body += data;

            // Too much POST data, kill the connection!
            // 1e6 === 1 * Math.pow(10, 6) === 1 * 1000000 ~~~ 1MB
            if (body.length > 1e6)
                request.connection.destroy();
        });

        request.on('end', function () {
            console.log(`got a post of ${body.length} bytes`)
            var payload = JSON.parse(body)
            console.log(payload)

            const filename = "input"
            const mode = fs.constants.O_WRONLY | fs.constants.O_APPEND

            console.log(`trying to open ${filename} :: ${mode}`)
            fs.open(filename, mode, (err, fd) => {
                fs.write(fd, body, x => {
                    console.log("write complete?")
                    fs.close(fd, _ => {
                        console.log("and close?")
                    })
                })
            })
        });
    }

    response.end('Hello Node.js Server!')
}


const server = http.createServer(requestHandler)

server.listen(port, (err) => {
    if (err) {
        return console.log('something bad happened', err)
    }

    console.log(`server is listening on ${port}`)
})
