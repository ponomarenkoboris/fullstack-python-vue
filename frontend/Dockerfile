FROM node:lts-alpine

WORKDIR quiz-client/
COPY package.json ./
RUN yarn install

COPY . .
RUN yarn build

EXPOSE 8080

CMD yarn start