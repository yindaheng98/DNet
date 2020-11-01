import sys
import os
sys.path.append(os.path.split(os.path.abspath(__file__))[0])
import ComputationMessage_pb2 as pb
import TransmissionUnit_pb2_grpc as rpc
from TransmissionUnitTestClient import TransmissionUnitTestClient