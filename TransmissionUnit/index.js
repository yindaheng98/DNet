var Server = require("./unit/server")
/**
 * Starts an RPC server that receives requests for the Greeter service at the
 * sample server port
 */
async function main() {
    var server = await Server("0.0.0.0:8080", 'amqp://192.168.1.2', 'ComputationQueue', '');
    server.start(function (err, data) {
        console.log(err);
        console.log(data);
    });
}

main();