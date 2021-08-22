FROM node:16 as builder

WORKDIR quiz-client/
COPY package.json ./
RUN yarn

COPY . .
RUN yarn build

FROM nginx:alpine as production-build
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /quiz-client/dist /usr/share/nginx/html

EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]