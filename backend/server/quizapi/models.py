from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    password = models.TextField()
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Quiz(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True, db_index=True)
    # TODO у опросов должна быть дата публикации, до наступления которой опрос пройти нельзя
    # available_date = models.DateTimeField(blank=True, default=datetime.datetime.now())

class QuestionGroup(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now=True, db_index=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=250)
    question_group = models.ForeignKey(QuestionGroup, related_name='questions', on_delete=models.CASCADE, null=True)
    multiple = models.BooleanField(default=False)
    question_photo = models.TextField(blank=True, default='')
    answer = models.TextField(blank=False)

class Variant(models.Model):
    question = models.ForeignKey(Question, related_name='variants', on_delete=models.CASCADE, db_index=True)
    variant = models.CharField(max_length=30)
