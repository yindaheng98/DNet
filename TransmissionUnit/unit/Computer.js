var rpc_Client = require("./grpcClient")
var pb = require('./ComputationMessage_pb');
var cu_Client = require("./ComputationUnitClient");

/**
 * 返回一个Compute函数用于在gRPC server中处理请求
 * @param amqp_addr amqp系统的地址，如"amqp://username:password@localhost:5672"
 * @param queue_name 要发送的队列名
 * @param next_addr 如果返回“计算未完成”，应该向哪个服务发起进一步的请求
 * @return 一个函数，严格遵循gRPC的请求处理函数标准格式
 */
module.exports = async function Computer(amqp_addr, queue_name, next_addr, delay = 0) {
    var to_next = (typeof next_addr === "string" && next_addr.length > 0);//没有输入next_addr说明不需要发送到下一个
    var rpc_client = null;//不需要发送下一个所以也就不需要RPC客户端
    if (to_next) rpc_client = rpc_Client(next_addr);

    var cu_client = await cu_Client(amqp_addr, queue_name);
    /**
     * Compute函数用于在gRPC server中处理请求
     * 输入格式请参考gRPC的请求处理函数标准格式
     */
    return function Compute(call, callback) {
        console.log("[收到请求] " + call.request.toString().substring(0, 10) + "......");
        cu_client(call.request, (response) => {//向ComputationUnit发送请求获得响应
            console.log("[计算结果] " + response.toString().substring(0, 10) + "......");
            if (to_next && response.getStatus() === pb.ComputationResponse.StatusCode.NOT_SUCCESS) {
                //如果需要发到下一个且计算结果是“计算未完成”则发到下一个
                var request = response.getNextRequest();//取出去下一个边缘的请求
                console.log("[计算结果 status = StatusCode.NOT_SUCCESS, 发到" + next_addr + "] " + request.toString().substring(0, 10) + "......")
                rpc_client.compute(request, function (err, response) {//发到下一个边缘
                    if (err) console.error(err);
                    console.log("[计算结果来自" + next_addr + "] " + request.toString().substring(0, 10) + "......")
                    if (delay !== 0) {
                        console.log("[延迟" + delay + "毫秒]")
                        setTimeout(() => callback(null, response), delay)
                    }
                    else callback(null, response);
                })
                return;
            }
            console.log("[计算结果 status != StatusCode.NOT_SUCCESS, 返回] ")
            callback(null, response);
        })
    }
}
