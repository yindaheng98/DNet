var amqp = require('amqplib/callback_api');
var UUID = require('uuid');

/**
 * 生成一个ComputationUnit客户端
 * @param amqp_addr amqp系统的地址，如"amqp://username:password@localhost:5672"
 * @param queue_name 要发送的队列名
 * @return 一个函数，输入ComputationRequest、异步输出
 */
module.exports = async function ComputationUnitClient(amqp_addr, queue_name) {
    var connection = await new Promise((resolve, reject) => {
        amqp.connect(amqp_addr, function (err, connection) {
            if (err) return reject(err);
            return resolve(connection);
        });
    });
    var channel = await new Promise((resolve, reject) => {
        conn.createChannel(function (err, channel) {
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
        var callback = callback[correlationId];
        if (callback !== undefined) {
            console.log(' [.] Got %s', correlationId);
            callback(msg.content);
        }
    });

    return function (request, callback) {
        var correlationId = UUID.v1();
        callbacks[correlationId] = callback;
        channel.sendToQueue(queue_name,
            request.serializeBinary(), {
            correlationId: correlationId,
            replyTo: queue_res.queue
        });
        console.log(' [.] Sent %s', correlationId);
    }
}