#将proto文件编译为Python和JS源代码
PROTO_PATH=./grpc
PROTO_PYTHON_OUT=./ComputationUnit/unit
PROTO_JS_OUT=./TransmissionUnit/unit
PROTOC="protoc --proto_path=$PROTO_PATH"
$PROTOC --python_out=$PROTO_PYTHON_OUT $PROTO_PATH/ComputationMessage.proto
$PROTOC --js_out=import_style=commonjs,binary:$PROTO_JS_OUT $PROTO_PATH/ComputationMessage.proto

PROTOC_JS_PLUGIN=protoc-gen-grpc=grpc_tools_node_protoc_plugin
$PROTOC --plugin=$PROTOC_JS_PLUGIN --grpc_out=$PROTO_JS_OUT $PROTO_PATH/TransmissionUnit.proto

#编译用于测试传输层的proto
PROTO_JS_TEST_OUT=./TransmissionUnit/unit
$PROTOC --python_out=$PROTO_JS_TEST_OUT $PROTO_PATH/ComputationMessage.proto
python -m grpc_tools.protoc --proto_path=$PROTO_PATH --grpc_python_out=$PROTO_JS_TEST_OUT $PROTO_PATH/TransmissionUnit.proto