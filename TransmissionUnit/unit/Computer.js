var Client = require("./client")
var messages = require('./ComputationMessage_pb');
module.exports = function Computer(next_addr) {//此函数返回一个Compute函数用于在server中执行计算
    var client = Client()
    function Compute(call, callback) {
        //TODO: 向ComputationUnit发送请求

        //TODO: 如果回复“计算完成”就返回结果
        var response = new messages.ComputationResponse();

        //TODO: 如果不是“计算完成”则发到下一个
        var request = new messages.ComputationRequest();
        request.setName('world');//TODO: 构造请求
        client.Compute(request, function (err, data) {
            if (err) console.error(err);
            else console.log(data);
            callback(err, response);
        })
    }

}
