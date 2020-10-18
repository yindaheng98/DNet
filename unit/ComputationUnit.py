# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了在分支网络组成单元中的计算层
"""
import pika
import pickle
from .ComputationCore import ComputationCore


class ComputationUnit(object):
    """
    实际上就是一个向ComputationCore传输计算请求的队列
    """

    def __init__(self, cc, conn_params, queue_name='ComputationQueue'):
        """
        初始化RabbitMQ RPC连接
        @params conn_params: RabbitMQ连接参数，是一个pika.ConnectionParameters
        @params queue_name: 用于RPC传输的队列名
        """
        if not isinstance(cc, ComputationCore):
            raise TypeError("cc必须是ComputationCore")
        self.cc = cc
        if not isinstance(conn_params, pika.ConnectionParameters):
            raise TypeError("conn_params必须是pika.ConnectionParameters")
        self.conn = pika.BlockingConnection(conn_params)
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name

    def __callback(self, ch, method, props, body):
        """处理请求的回调函数"""
        ch.basic_ack(delivery_tag=method.delivery_tag)
        req = pickle.loads(body)
        print("[x] 收到计算请求%s" % props.correlation_id)
        ok, result = self.cc.compute(req.x, req.start_layer, req.exit_layer)
        data = pickle.dumps({"ok": ok, "result": result})
        print("[x] 完成计算请求%s" % props.correlation_id)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(data))
        print("[x] 返回计算结果%s" % props.correlation_id)

    def start(self):
        """启动队列的运行"""
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.__callback)
        print(" [x] Awaiting RPC requests on %s" % self.queue_name)
        self.channel.start_consuming()
