import ComputationMessage_pb2 as pb
request = pb.ComputationRequest()
request.start_layer = 1
request.x = b'\x08\x01'
reqs = request.SerializeToString()
print(reqs)
print(request.x)

response = pb.ComputationResponse()
response.status = pb.ComputationResponse.StatusCode.SUCCESS
response.result = b"\x08\x01"
response.error_message = "123123"
ress = response.SerializeToString()
print(ress)
