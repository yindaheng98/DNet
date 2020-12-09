::将proto文件编译为Python和JS源代码
set PROTO_PATH=.\grpc
set PROTO_PYTHON_OUT=.\ComputationUnit\unit
set PROTO_JS_OUT=.\TransmissionUnit\unit
set PROTOC=protoc --proto_path=%PROTO_PATH%
%PROTOC% --python_out=%PROTO_PYTHON_OUT% %PROTO_PATH%\ComputationMessage.proto
%PROTOC% --js_out=import_style=commonjs,binary:%PROTO_JS_OUT% %PROTO_PATH%\ComputationMessage.proto
%PROTOC% --js_out=import_style=commonjs,binary:%PROTO_JS_OUT% %PROTO_PATH%\TransmissionMessage.proto

set PROTOC_JS_PLUGIN=protoc-gen-grpc=C:\Users\yinda\AppData\Roaming\npm\grpc_tools_node_protoc_plugin.cmd
%PROTOC% --plugin=%PROTOC_JS_PLUGIN% --grpc_out=%PROTO_JS_OUT% %PROTO_PATH%\TransmissionUnit.proto

::编译用于测试传输层的proto
set PROTO_JS_TEST_OUT=.\TransmissionUnit\unit
%PROTOC% --python_out=%PROTO_JS_TEST_OUT% %PROTO_PATH%\ComputationMessage.proto
%PROTOC% --python_out=%PROTO_JS_TEST_OUT% %PROTO_PATH%\TransmissionMessage.proto
python -m grpc_tools.protoc --proto_path=%PROTO_PATH% --grpc_python_out=%PROTO_JS_TEST_OUT% %PROTO_PATH%\TransmissionUnit.proto