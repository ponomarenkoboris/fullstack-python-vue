from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO доделать модель пользователя и пользовательских ответов

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    password = models.TextField()
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    # TODO add user avatar

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Quiz(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True, db_index=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    multiple = models.BooleanField(default=False)
    answer = models.CharField(max_length=30)

class Variant(models.Model):
    question = models.ForeignKey(Question, related_name='variants', on_delete=models.CASCADE, db_index=True)
    variant = models.CharField(max_length=30)
