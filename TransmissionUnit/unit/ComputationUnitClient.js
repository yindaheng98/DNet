var pb = require("./ComputationMessage_pb")
var amqp = require('amqplib/callback_api');
var UUID = require('uuid');

/**
 * 生成一个ComputationUnit客户端
 * @param amqp_addr amqp系统的地址，如"amqp://username:password@localhost:5672"
 * @param queue_name 要发送的队列名
 * @return 返回ComputationUnit客户端调用函数，输入ComputationRequest，使用callback进行异步输出ComputationResponse
 */
module.exports = async function ComputationUnitClient(amqp_addr, queue_name) {
    var connection = await new Promise((resolve, reject) => {
        amqp.connect(amqp_addr, function (err, connection) {
            if (err) return reject(err);
            return resolve(connection);
        });
    });
    var channel = await new Promise((resolve, reject) => {
        connection.createChannel(function (err, channel) {
            if (err) return reject(err);
            return resolve(channel);
        });
    });
    var queue_res = await new Promise((resolve, reject) => {
        channel.assertQueue('', { exclusive: true }, function (err, queue) {
            if (err) return reject(err);
            return resolve(queue);
        })
    });

    var callbacks = {};

    channel.consume(queue_res.queue, function (msg) {
        var correlationId = msg.properties.correlationId;
        var callback = callbacks[correlationId];
        if (callback !== undefined) {
            console.log(' [.] Got %s', correlationId);
            callback(pb.ComputationResponse.deserializeBinary(msg.content));
        }
    });

    /**
     * 生成一个ComputationUnit客户端
     * @param request 输入ComputationRequest
     * @param callback 请求返回回调函数，输入为ComputationResponse
     */
    return function (request, callback) {
        var correlationId = UUID.v1();
        callbacks[correlationId] = callback;
        channel.sendToQueue(queue_name,
            Buffer.from(request.serializeBinary()), {
            correlationId: correlationId,
            replyTo: queue_res.queue
        });
        console.log(' [.] Sent %s', correlationId);
    }
}