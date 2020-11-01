# -*- coding: utf-8 -*-
# @Author  : Yin Daheng

"""
本文件定义了在分支网络组成单元中的计算层
计算层从RabbitMQ中的指定队列中取出数据，进行处理，返回结果
数据存取方式参考RabbitMQ RPC模式
数据格式为ProtoBuf，见ComputationMessage.proto
"""
import pika
import pickle
from . ComputationCore import ComputationCore
from . import ComputationMessage_pb2 as pb


class ComputationUnit(object):
    """
    实际上就是一个向ComputationCore传输计算请求的队列
    """

    def __init__(self, cc, conn_params, queue_name='ComputationQueue'):
        """
        初始化RabbitMQ RPC连接
        @params conn_params: RabbitMQ连接参数，是一个pika.ConnectionParameters
        @params queue_name: 用于传输RPC请求的队列名
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
        """
        处理请求的回调函数
        接收队列中传来的请求protobuf数据，进行处理，返回结果protobuf数据
        其输入参数定义见pika.channel.basic_consume中的回调函数文档
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 立即回复收到
        request, response = pb.ComputationRequest(), pb.ComputationResponse()
        try:
            print("[x] 收到计算请求%s" % props.correlation_id)
            request.ParseFromString(body)  # 加载数据
            x = pickle.loads(request.x)  # 加载x
            ok, result = self.cc.compute(x, request.start_layer)  # 执行计算
            print("[x] 完成计算请求%s" % props.correlation_id)
            if ok:  # 成功退出
                response.status = pb.ComputationResponse.StatusCode.SUCCESS
                response.result = pickle.dumps(result)
            else:  # 还需要进一步计算
                response.status = pb.ComputationResponse.StatusCode.NOT_SUCCESS
                x, start_layer = result
                response.next_request.start_layer = start_layer
                response.next_request.x = pickle.dumps(x)
        except BaseException as e:
            response.status = pb.ComputationResponse.StatusCode.ERROR
            response.error_message = str(e)
            print("[x] 出现错误%s" % str(e))
        finally:
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(
                                 correlation_id=props.correlation_id),
                             body=response.SerializeToString())
            print("[x] 返回计算结果%s" % props.correlation_id)

    def start(self):
        """启动队列的运行"""
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.__callback)
        print(" [x] Awaiting RPC requests on %s" % self.queue_name)
        self.channel.start_consuming()
