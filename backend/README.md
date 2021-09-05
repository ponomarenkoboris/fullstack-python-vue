# Проект создания опросов [Backend]

## Скачивание папки проекта из репозитория 
```shell
git clone https://github.com/ponomarenkoboris/fullstack-python-vue.git
cd fullstack-python-vue/backend
```
## Запуск проекта с помощью Docker:
### Создание образа контейнера
```shell
docker build -t quiz-backend-root .
```
### Запуск контейнера
```shell
docker run -p 8000:8000 --rm --name quiz-server quiz-backend-root
```

## Запуск проекта локально: 
### Установка и активация виртульного окружения: 
```shell
python -m venv venv
cd venv/Scritps/activate.bat
```
### Установка зависимостей
```shell
pip install -r requirements.txt
```
### Подготовка к миграции данных
```shell
python manage.py makemigrations
```

### Миграция моделей данных
```shell
python manage.py migrate
```
### Загрузка фикстур
```shell
python manage.py loaddata fixtures/initial_data.json
```
### Запуск
```shell
python manage.py runserver
```