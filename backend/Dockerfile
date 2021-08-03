FROM python:3.9

RUN mkdir -p /backend/
WORKDIR /backend/

COPY . /backend/

RUN pip install -r requirements.txt

CMD ["cd", "./server", "&","python", "manage.py", "runserver"]
