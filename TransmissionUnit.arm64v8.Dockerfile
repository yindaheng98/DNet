FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM arm64v8/node:12-alpine
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY TransmissionUnit /app
WORKDIR /app
RUN npm install

CMD ["npm", "run", "start"]