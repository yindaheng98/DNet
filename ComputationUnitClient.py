import pika
import pickle
import json
import uuid


class ComputationUnitClient(object):
    def __init__(self, conn_params, queue_name='ComputationQueue'):
        if not isinstance(conn_params, pika.ConnectionParameters):
            raise TypeError("conn_params必须是pika.ConnectionParameters")
        self.conn = pika.BlockingConnection(conn_params)
        self.channel = self.conn.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = queue_name
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.__call_back,
            auto_ack=True)
        self.corr_ids = {}

    def __call_back(self, ch, method, props, body):
        print("[x] 收到计算结果%s" % props.correlation_id)
        if props.correlation_id in self.corr_ids:
            self.corr_ids[props.correlation_id] = body

    def call(self, x, start_layer):
        data = {"x": pickle.dumps(x), "start_layer": start_layer}
        req = json.dumps(data)
        corr_id = str(uuid.uuid4())
        self.corr_ids[corr_id] = ""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=corr_id,
            ),
            body=str(req))
        print("[x] 发送计算请求%s" % corr_id)

    def wait(self):
        finish = False
        while not finish:
            self.conn.process_data_events()
            finish = True
            for data in self.corr_ids.values():
                if data == '':
                    finish = False
                    break
        return self.corr_ids
