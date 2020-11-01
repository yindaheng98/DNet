import pickle
import grpc
from . import ComputationMessage_pb2 as pb
from . import TransmissionUnit_pb2_grpc as rpc

"""
本文件是用于测试与传输层之间连接客户端类，不是项目的正式内容
其用途是按照TransmissionUnit的格式调用gRPC接口，以测试其有效性
"""


class TransmissionUnitTestClient(object):
    """用于测试与传输层之间连接客户端类"""

    def __init__(self, addr="localhost:8080"):
        """
        初始化TransmissionUnit连接
        @params addr: TransmissionUnit的gRPC地址
        """

        # 连接 rpc 服务器
        self.channel = grpc.insecure_channel('localhost:8080')
        self.stub = rpc.DNetStub(self.channel)

    def call(self, x, start_layer):
        """
        向TransmissionUnit发送gRPC请求，并等待响应
        @params x
        @params start_layer
        """
        request = pb.ComputationRequest()
        request.start_layer = start_layer
        request.x = pickle.dumps(x)
        print("发送计算请求%s" % (str(request)[0:20]))
        response = self.stub.Compute(request)
        print("收到计算结果%s" % (str(response)[0:20]))
