var Server = require("./unit/grpcServer")
const { program } = require('commander');
program.version('0.0.1');
program
    .option('-l, --listen-address <listen-address>', 'gRPC服务器将要监听的IP地址和端口', '0.0.0.0:8080')
    .option('-a, --amqp-address <amqp-address>', '与计算层通讯的RabbitMQ服务器接口地址', 'amqp://localhost')
    .option('-q, --queue-name <queue-name>', '与计算层通讯的RabbitMQ队列名称', 'ComputationQueue')
    .option('-n, --next-address <next-address>', '如果此服务器运行在边缘，此处指定下一套模型（云端）的gRPC服务器位置', '');

async function main() {
    program.parse(process.argv);
    var listenAddress = program.listenAddress;
    console.log('gRPC接口监听于' + listenAddress);
    var amqpAddress = program.amqpAddress;
    console.log('使用位于' + amqpAddress + '的RabbitMQ');
    var queueName = program.queueName;
    console.log('使用名为' + queueName + '的队列传输计算请求');
    var nextAddress = program.nextAddress;
    console.log('下一个模型分块gRPC接口位于' + nextAddress);
    var server = await Server(listenAddress, amqpAddress, queueName, nextAddress);
    server.start(function (err, data) {
        console.log(err);
        console.log(data);
    });
}

main();