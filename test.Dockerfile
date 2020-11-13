FROM yindaheng98/dnet-computationunit
COPY test /app
COPY TransmissionUnit /app
WORKDIR /app/test
RUN python load_data.py
CMD ["python", "TransmissionUnit.test.py"]