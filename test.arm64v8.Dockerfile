FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM yindaheng98/dnet-computationunit:arm64v8
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY test /app/test
COPY TransmissionUnit /app/TransmissionUnit
WORKDIR /app/test
RUN python load_data.py
CMD ["python", "TransmissionUnit.test.py"]