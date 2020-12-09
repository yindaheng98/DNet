// GENERATED CODE -- DO NOT EDIT!

'use strict';
var grpc = require('grpc');
var ComputationMessage_pb = require('./ComputationMessage_pb.js');
var TransmissionMessage_pb = require('./TransmissionMessage_pb.js');

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

function serialize_unit_QlengthRequest(arg) {
  if (!(arg instanceof TransmissionMessage_pb.QlengthRequest)) {
    throw new Error('Expected argument of type unit.QlengthRequest');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_unit_QlengthRequest(buffer_arg) {
  return TransmissionMessage_pb.QlengthRequest.deserializeBinary(new Uint8Array(buffer_arg));
}

function serialize_unit_QlengthResponse(arg) {
  if (!(arg instanceof TransmissionMessage_pb.QlengthResponse)) {
    throw new Error('Expected argument of type unit.QlengthResponse');
  }
  return Buffer.from(arg.serializeBinary());
}

function deserialize_unit_QlengthResponse(buffer_arg) {
  return TransmissionMessage_pb.QlengthResponse.deserializeBinary(new Uint8Array(buffer_arg));
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
  qlength: {
    path: '/unit.DNet/Qlength',
    requestStream: false,
    responseStream: false,
    requestType: TransmissionMessage_pb.QlengthRequest,
    responseType: TransmissionMessage_pb.QlengthResponse,
    requestSerialize: serialize_unit_QlengthRequest,
    requestDeserialize: deserialize_unit_QlengthRequest,
    responseSerialize: serialize_unit_QlengthResponse,
    responseDeserialize: deserialize_unit_QlengthResponse,
  },
};

exports.DNetClient = grpc.makeGenericClientConstructor(DNetService);
