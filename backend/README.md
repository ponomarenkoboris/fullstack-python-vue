# Проект создания опросов [Backend]

## Скачивание папки проекта из репозитория 
```
git clone https://github.com/ponomarenkoboris/fullstack-python-vue.git
```
## Docker:
### Создание образа контейнера
```shell
docker build -t quiz-backend-root .
```
### Запуск контейнера
```shell
docker run -it -p 8080:5555 --rm --name quiz-server quiz-backend-root
```

## Локально: 
#### Установка зависимостей
```shell
pip install -r requirements.txt
```
#### Запуск на локально
```shell
python manage.py runserver 0.0.0.0:5555
```