FROM python:3.7.9-slim-buster
RUN pip install --no-cache-dir \
    torch==1.7.0+cpu \
    torchvision==0.8.1+cpu \
    torchaudio===0.7.0 \
    -f https://download.pytorch.org/whl/torch_stable.html && \
    pip install --no-cache-dir pika==1.1.0 protobuf==3.13.0 grpcio==1.33.2
COPY ComputationUnit /app/ComputationUnit
WORKDIR /app

CMD ["python", "ComputationUnit"]