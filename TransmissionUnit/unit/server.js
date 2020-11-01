var Compute = require("./Compute")
var services = require('./TransmissionUnit_grpc_pb');
var grpc = require('grpc')
module.exports = function (addr) {
    var server = new grpc.Server();
    server.addService(services.DNetService, { Compute: Compute });
    server.bind(addr, grpc.ServerCredentials.createInsecure());
    return server;
}