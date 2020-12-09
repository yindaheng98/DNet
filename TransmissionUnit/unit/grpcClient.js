var services = require('./TransmissionUnit_grpc_pb');
var grpc = require('grpc')

module.exports = function (to_addr) {
    var client = new services.DNetClient(
        to_addr,
        grpc.credentials.createInsecure()
    );
    return client;
}