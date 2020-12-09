var Computer = require("./Computer")
var Qstatuser = require("./Qstatuser")
var services = require('./TransmissionUnit_grpc_pb');
var grpc = require('grpc')
module.exports = async function (listen_addr, amqp_addr, queue_name, next_addr) {
    var server = new grpc.Server();
    server.addService(services.DNetService, {
        compute: await Computer(amqp_addr, queue_name, next_addr),
        qstatus: await Qstatuser(amqp_addr, queue_name)
    });
    server.bind(listen_addr, grpc.ServerCredentials.createInsecure());
    return server;
}