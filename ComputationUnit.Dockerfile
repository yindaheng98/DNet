
FROM busybox AS downloader
ENV MODEL_URL=https://github.com/yindaheng98/torch-models/releases/download/multi-exit-inception-v3-cifar10-epoch53/multi-exit-inception-v3-cifar10-epoch53.pkl.gz
RUN cd / && \
    wget --no-check-certificate $MODEL_URL && \
    gzip -d multi-exit-inception-v3-cifar10-epoch53.pkl.gz






FROM python:3.7.9-slim-buster
COPY ComputationUnit /app/ComputationUnit
COPY --from=downloader /multi-exit-inception-v3-cifar10-epoch53.pkl /app/ComputationUnit
RUN pip install --no-cache-dir \
    torch==1.7.0+cpu \
    torchvision==0.8.1+cpu \
    torchaudio===0.7.0 \
    -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir pika==1.1.0 protobuf==3.13.0 grpcio==1.33.2
WORKDIR /app

CMD ["python", "ComputationUnit"]