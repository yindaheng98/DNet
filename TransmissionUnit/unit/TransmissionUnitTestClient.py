import pickle
import grpc
import ComputationMessage_pb2 as pb
import TransmissionMessage_pb2 as tpb
import TransmissionUnit_pb2_grpc as rpc

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
        self.channel = grpc.insecure_channel(addr)
        self.stub = rpc.DNetStub(self.channel)

    def Compute(self, x, start_layer):
        """
        向TransmissionUnit发送gRPC请求，并等待响应
        @params x
        @params start_layer
        """
        request = pb.ComputationRequest()
        request.start_layer = start_layer
        request.x = pickle.dumps(x)
        response = self.stub.Compute(request)
        return response

    def Qstatus(self):
        """
        向TransmissionUnit查询当前的队列长度
        """
        request = tpb.QstatusRequest()
        response = self.stub.Qstatus(request)
        return response
