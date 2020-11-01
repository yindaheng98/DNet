set PROTO_PATH=.\grpc
set PROTO_PYTHON_OUT=.\ComputationUnit\unit
set PROTO_JS_OUT=.\TransmissionUnit
set PROTOC=protoc --proto_path=%PROTO_PATH%
%PROTOC% --python_out=%PROTO_PYTHON_OUT% %PROTO_PATH%\ComputationMessage.proto
%PROTOC% --js_out=import_style=commonjs,binary:%PROTO_JS_OUT% %PROTO_PATH%\ComputationMessage.proto

set PROTOC_JS_PLUGIN=protoc-gen-grpc=.\TransmissionUnit\node_modules\.bin\grpc_tools_node_protoc_plugin.cmd
%PROTOC% --js_out=import_style=commonjs,binary:%PROTO_JS_OUT% --plugin=%PROTOC_JS_PLUGIN% --grpc_out=%PROTO_JS_OUT% %PROTO_PATH%\TransmissionUnit.proto
