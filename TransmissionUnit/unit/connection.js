var amqp = require('amqplib/callback_api');

module.exports = async function ConnectChannel (amqp_addr) {
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
    return channel;
}
