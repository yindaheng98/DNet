var Computer = require("./Computer")
var services = require('./TransmissionUnit_grpc_pb');
var grpc = require('grpc')
module.exports = function (listen_addr, next_addr) {
    var server = new grpc.Server();
    server.addService(services.DNetService, { Compute: Computer(next_addr) });
    server.bind(listen_addr, grpc.ServerCredentials.createInsecure());
    return server;
}