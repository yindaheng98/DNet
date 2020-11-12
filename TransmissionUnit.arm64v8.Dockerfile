FROM arm64v8/node:12-alpine

COPY TransmissionUnit /app
WORKDIR /app
RUN npm install

CMD ["npm", "run", "start"]