var messages = require('./ComputationMessage_pb');
var services = require('./TransmissionUnit_grpc_pb');

module.exports = function (addr) {
    var client = new services.DNetServiceClient(
        addr,
        grpc.credentials.createInsecure()
    );
    return client;
}