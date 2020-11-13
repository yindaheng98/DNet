FROM busybox AS downloader
RUN mkdir /torch && cd /torch && \
    wget http://mathinf.com/pytorch/arm64/torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl && \
    wget http://mathinf.com/pytorch/arm64/torchvision-0.8.0a0+45f960c-cp37-cp37m-linux_aarch64.whl

FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM arm64v8/python:3.7.9-slim-buster
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY --from=downloader /torch /torch
RUN pip3 install /torch/torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl && \
    pip3 install /torch/torchvision-0.8.0a0+45f960c-cp37-cp37m-linux_aarch64.whl && \
    pip3 install --no-cache-dir pika==1.1.0 protobuf==3.13.0 grpcio==1.33.2 && \
    rm -rf /torch && \
    apt-get update && \
    apt-get install -y libopenmpi-dev && \
    apt-get clean && \
    rm /usr/bin/qemu-aarch64-static

COPY ComputationUnit /app/ComputationUnit
WORKDIR /app

CMD ["python", "ComputationUnit"]