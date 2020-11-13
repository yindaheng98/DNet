FROM node:12-stretch-slim

COPY TransmissionUnit /app
WORKDIR /app
RUN npm install

CMD ["npm", "run", "start"]