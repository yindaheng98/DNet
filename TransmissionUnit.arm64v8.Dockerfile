FROM multiarch/qemu-user-static:x86_64-aarch64 as qemu
FROM arm64v8/node:12-alpine AS builder
COPY --from=qemu /usr/bin/qemu-aarch64-static /usr/bin
COPY TransmissionUnit /app
WORKDIR /app
RUN  npm install

FROM arm64v8/node:12-alpine
COPY TransmissionUnit /app
COPY --from=builder /app/node_modules /app/node_modules
WORKDIR /app

CMD ["npm", "run", "start"]