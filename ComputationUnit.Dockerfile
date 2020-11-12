FROM python:3.7.9-slim-buster
RUN pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
COPY ComputationUnit /app/ComputationUnit
WORKDIR /app

CMD ["python", "ComputationUnit"]