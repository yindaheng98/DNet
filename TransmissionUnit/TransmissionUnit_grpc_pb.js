// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var ComputationMessage_pb = require('./ComputationMessage_pb.js');

function serialize_unit_ComputationRequest(arg) {
  if (!(arg instanceof ComputationMessage_pb.ComputationRequest)) {
    throw new Error('Expected argument of type unit.ComputationRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_unit_ComputationRequest(buffer_arg) {
  return ComputationMessage_pb.ComputationRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_unit_ComputationResponse(arg) {
  if (!(arg instanceof ComputationMessage_pb.ComputationResponse)) {
    throw new Error('Expected argument of type unit.ComputationResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_unit_ComputationResponse(buffer_arg) {
  return ComputationMessage_pb.ComputationResponse.deserializeBinary(new Uint8Array(buffer_arg));
}


var DNetService = exports.DNetService = {
  compute: {
    path: '/unit.DNet/Compute',
    requestStream: false,
    responseStream: false,
    requestType: ComputationMessage_pb.ComputationRequest,
    responseType: ComputationMessage_pb.ComputationResponse,
    requestSerialize: serialize_unit_ComputationRequest,
    requestDeserialize: deserialize_unit_ComputationRequest,
    responseSerialize: serialize_unit_ComputationResponse,
    responseDeserialize: deserialize_unit_ComputationResponse,
  },
};

exports.DNetClient = grpc.makeGenericClientConstructor(DNetService);
