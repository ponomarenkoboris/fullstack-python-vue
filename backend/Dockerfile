FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend

WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt

COPY . /backend

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8080
CMD ["python", "manage.py", "runserver"]