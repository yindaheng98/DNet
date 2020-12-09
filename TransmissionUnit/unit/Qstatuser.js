var pb = require('./QstatusMessage_pb');
var Channel = require("./connection");

/**
 * 返回一个Qlength函数用于在gRPC server中处理请求
 * @param amqp_addr amqp系统的地址，如"amqp://username:password@localhost:5672"
 * @param queue_name 要发送的队列名
 * @return 一个函数，严格遵循gRPC的请求处理函数标准格式
 */
module.exports = async function Qstatuser(amqp_addr, queue_name) {
    var channel = await Channel(amqp_addr);
    /**
     * Qlength函数用于在gRPC server中处理请求
     * 输入格式请参考gRPC的请求处理函数标准格式
     */
    return function Qstatus(call, callback) {
        console.log("[查询队列信息] " + queue_name + "......");
        channel.checkQueue(queue_name, function (err, queue) {
            var response = new pb.QstatusResponse();
            if (err) return callback(err, response);
            response.setQlength(queue.messageCount);
            response.setConsumer(queue.consumerCount);
            console.log("[队列信息]" + queue_name + ": messageCount = " + queue.messageCount + ", consumerCount = " + queue.consumerCount);
            return callback(null, response);
        })
    }
}
