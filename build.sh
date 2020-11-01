PROTO_PATH=./grpc
PROTO_PYTHON_OUT=./ComputationUnit/unit
PROTO_JS_OUT=./TransmissionUnit/unit
PROTOC="protoc --proto_path=$PROTO_PATH"
$PROTOC --python_out=$PROTO_PYTHON_OUT $PROTO_PATH/ComputationMessage.proto
$PROTOC --js_out=import_style=commonjs,binary:$PROTO_JS_OUT $PROTO_PATH/ComputationMessage.proto

PROTOC_JS_PLUGIN=protoc-gen-grpc=grpc_tools_node_protoc_plugin
$PROTOC --js_out=import_style=commonjs,binary:$PROTO_JS_OUT --plugin=$PROTOC_JS_PLUGIN --grpc_out=$PROTO_JS_OUT $PROTO_PATH/TransmissionUnit.proto