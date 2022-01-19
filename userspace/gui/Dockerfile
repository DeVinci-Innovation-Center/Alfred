FROM node:16-alpine

RUN mkdir /app
WORKDIR /app

COPY app/package-lock.json app/package.json /app/

RUN npm install

COPY app /app/

ARG NUXT_ENV_HOST_IP=0.0.0.0
ENV NUXT_ENV_HOST_IP=$NUXT_ENV_HOST_IP

RUN npm run build && \
    npm run generate

CMD npm run start
