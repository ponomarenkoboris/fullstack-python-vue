# Проект для создания опросов [Frontend]

## Скачивание папки проекта из репозитория:
```shell
git clone https://github.com/ponomarenkoboris/fullstack-python-vue.git
cd fullstack-python-vue.git/frontend
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

### Для того, чтобы запустить проект локально, необходимо установить пакетный менеджер **yarn**:
```shell
npm i -g yarn
```
#### Установка зависимостей
```
yarn install
```
#### Запуск на локальном сервере в режие разработки
```
yarn serve
```
#### Сборка проекта 
```
yarn build
```
