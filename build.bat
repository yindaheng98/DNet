set PROTO_PATH=".\TransmissionUnit\grpc"
set PROTO_PYTHON_OUT=.\ComputationUnit\unit
protoc --proto_path=%PROTO_PATH% --python_out=%PROTO_PYTHON_OUT% %PROTO_PATH%\ComputationMessage.proto