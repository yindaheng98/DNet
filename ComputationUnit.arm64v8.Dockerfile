FROM yindaheng98/grpcio-1.33.2-cp37-aarch64 AS installer
FROM busybox AS downloader
ENV MODEL_URL=https://github.com/yindaheng98/torch-models/releases/download/multi-exit-inception-v3-cifar10-epoch53/multi-exit-inception-v3-cifar10-epoch53.pkl.gz
RUN cd / && \
    wget --no-check-certificate $MODEL_URL && \
    gzip -d multi-exit-inception-v3-cifar10-epoch53.pkl.gz
RUN mkdir /installer && cd /installer && \
    wget http://mathinf.com/pytorch/arm64/torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl && \
    wget http://mathinf.com/pytorch/arm64/torchvision-0.8.0a0+45f960c-cp37-cp37m-linux_aarch64.whl
COPY --from=installer /grpcio-install/* /installer/

FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM arm64v8/python:3.7.9-slim-buster
COPY ComputationUnit /app/ComputationUnit
COPY --from=downloader /multi-exit-inception-v3-cifar10-epoch53.pkl /app/ComputationUnit
COPY --from=downloader /installer /installer
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
RUN pip3 install /installer/* && \
    pip3 install --no-cache-dir pika==1.1.0 protobuf==3.13.0 && \
    rm -rf /installer && \
    apt-get update && \
    apt-get install -y libopenmpi-dev && \
    apt-get clean && \
    rm /usr/bin/qemu-aarch64-static
WORKDIR /app

CMD ["python", "ComputationUnit"]