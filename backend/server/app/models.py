from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель пользователя
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# class QuestionVariant(models.Model):
#     id = models.IntegerField(unique=True)
#     answer = models.CharField(max_length=40)

# class Questions(models.Model):
#     question = models.CharField(max_length=True, db_index=True)
#     variant = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
#     multiple = models.BooleanField(default=False)
#
#
# class Quiz(models.Model):
#     name = models.CharField(max_length=255, unique=True, db_index=True)
#     description = models.TextField()
#     questions = models.ForeignKey(Questions, on_delete=models.CASCADE)