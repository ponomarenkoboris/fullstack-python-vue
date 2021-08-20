FROM node:lts-alpine AS build

WORKDIR /app
COPY package.json ./
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:1.19.0-alpine AS prod-stage
COPY --from=build /app/dist usr/share/nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /ect/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]