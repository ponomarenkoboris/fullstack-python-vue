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
docker run -p 8000:8000 --rm --name quiz-server quiz-backend-root
```

## Локально: 
#### Установка зависимостей
```shell
pip install -r requirements.txt
```
#### Запуск на локально
```shell
python manage.py runserver 127.0.0.1:5555
```