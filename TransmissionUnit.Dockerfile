FROM node:12-alpine

RUN mv TransmissionUnit /app && cd /app && npm install
WORKDIR /app

CMD ["npm", "run", "start"]