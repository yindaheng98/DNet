import pika
import pickle
import json
import uuid
import base64

"""
本文件是用于测试中间层和计算层之间连接客户端类，不是项目的正式内容
其用途是按照ComputationUnit的格式向中间层RabbitMQ中发送数据，以测试其有效性
"""

class ComputationUnitClient(object):
    """用于测试中间层和计算层之间连接客户端类"""
    def __init__(self, conn_params, queue_name='ComputationQueue'):
        """
        初始化RabbitMQ RPC连接
        @params conn_params: RabbitMQ连接参数，是一个pika.ConnectionParameters
        @params queue_name: 用于RPC传输的队列名
        """
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
        """
        向RabbitMQ中发送一条数据，发送完即退出，无阻塞
        发送后相应的消息会计入一个列表
        @params x
        @params start_layer
        """
        data = {"x": str(base64.b64encode(pickle.dumps(x)), "utf8"),
                "start_layer": start_layer}
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
        """等待列表中的消息收到回应"""
        finish = False
        while not finish:
            self.conn.process_data_events()
            finish = True
            for data in self.corr_ids.values():
                if data == '':
                    finish = False
                    break
        return self.corr_ids
