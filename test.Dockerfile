FROM yindaheng98/dnet-computationunit:amd64
COPY test /app/test
COPY TransmissionUnit /app/TransmissionUnit
WORKDIR /app/test
RUN python load_data.py
CMD ["python", "TransmissionUnit.test.py"]