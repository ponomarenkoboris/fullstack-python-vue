# Проект для создания опросов [Frontend]

## Скачивание папки проекта из репозитория:
```shell
git clone https://github.com/ponomarenkoboris/fullstack-python-vue.git
cd frontend
```
## Запуск преокта с помощью Docker:
### Создание образа контейнера
```shell
docker build -t quiz-frontend-root .
```
### Запуск контейнера
```shell
docker run -it -p 8080:8080 --rm --name quiz-client quiz-frontend-root
```

## Локально: 
#### Установка зависимостей
```
yarn install
```
#### Запуск на локальном сервере
```
yarn serve
```
#### Создание production версии
```
yarn build
```
