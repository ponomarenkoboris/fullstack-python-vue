FROM python:3.9
ENV PYTHONUNBUFFERED 1

RUN mkdir /backend

WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt

COPY . /backend

RUN python ./server/manage.py makemigrations
RUN python ./server/manage.py migrate

CMD ["python", "./server/manage.py", "runserver runserver 0.0.0.0:8000"]