FROM node:16-alpine

RUN mkdir /app
WORKDIR /app

COPY app/package-lock.json app/package.json /app/

RUN npm install

COPY app /app/

RUN npm run build && \
    npm run generate

CMD npm run start
