var messages = require('./ComputationMessage_pb');
var services = require('./TransmissionUnit_grpc_pb');

module.exports = function (to_addr) {
    var client = new services.DNetServiceClient(
        to_addr,
        grpc.credentials.createInsecure()
    );
    return client;
}