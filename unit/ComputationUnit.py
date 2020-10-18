# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了在分支网络组成单元中的计算层
"""
import pika
import pickle
from ComputationCore import ComputationCore


class ComputationRequest(object):
    """
    此类表示一个由传输层输入到计算层的计算请求接口
    此类是一个抽象类，使用前请先实现push_result方法
    """

    def __init__(self, x, start_layer, exit_layer):
        self.x = x
        self.start_layer = start_layer
        self.exit_layer = exit_layer

    def push_result(self, ok, result):
        """
        此方法在ComputationUnit.start的循环中被调用
        用于将ComputationUnit.compute的输出结果传回传输层
        输入参数同ComputationUnit.compute的返回值
        """
        pass


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
        self.conn = pika.adapters.asyncio_connection.AsyncioConnection(
            conn_params)
        self.channel = self.conn.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name

    def __callback(self, ch, method, props, body):
        """处理请求的回调函数"""
        ch.basic_ack(delivery_tag=method.delivery_tag)
        req = pickle.loads(body)
        ok, result = self.cc.compute(req.x, req.start_layer, req.exit_layer)
        data = pickle.dumps({"ok": ok, "result": result})
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=str(data))

    def start(self):
        """启动队列的运行"""
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.__callback)
        print(" [x] Awaiting RPC requests on %s" % self.queue_name)
        self.channel.start_consuming()
