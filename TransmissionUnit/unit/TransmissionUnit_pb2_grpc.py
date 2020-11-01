# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import ComputationMessage_pb2 as ComputationMessage__pb2


class DNetStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Compute = channel.unary_unary(
                '/unit.DNet/Compute',
                request_serializer=ComputationMessage__pb2.ComputationRequest.SerializeToString,
                response_deserializer=ComputationMessage__pb2.ComputationResponse.FromString,
                )


class DNetServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Compute(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DNetServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Compute': grpc.unary_unary_rpc_method_handler(
                    servicer.Compute,
                    request_deserializer=ComputationMessage__pb2.ComputationRequest.FromString,
                    response_serializer=ComputationMessage__pb2.ComputationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'unit.DNet', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DNet(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Compute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/unit.DNet/Compute',
            ComputationMessage__pb2.ComputationRequest.SerializeToString,
            ComputationMessage__pb2.ComputationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)