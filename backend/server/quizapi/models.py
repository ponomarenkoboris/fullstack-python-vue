from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO модель группы вопросов

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

# class QuestionGroup(models.Model):
#     group_name = models.CharField(max_length=255)
#     date_created = models.DateTimeField(auto_now=True, db_index=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    # question_group = models.ForeignKey(QuestionGroup, related_name='question group', on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    multiple = models.BooleanField(default=False)
    question_photo = models.TextField(blank=True, default='')
    answer = models.TextField(blank=False)

class Variant(models.Model):
    question = models.ForeignKey(Question, related_name='variants', on_delete=models.CASCADE, db_index=True)
    variant = models.CharField(max_length=30)
