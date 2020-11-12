FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM busybox AS downloader
RUN wget http://mathinf.com/pytorch/arm64/torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl -O /torch.whl
FROM arm64v8/python:3.7.9-slim-buster
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY --from=downloader /torch.whl /torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl
#COPY ./torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl /torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl
RUN pip3 install /torch-1.7.0a0-cp37-cp37m-linux_aarch64.whl && \
    pip3 install torchvision && \
    apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y libopenmpi-dev
COPY ComputationUnit /app/ComputationUnit
WORKDIR /app

CMD ["python", "ComputationUnit"]