from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Модель пользователя

    email: электронная почта
    password: парольпользователя
    name: имя пользователя
    surname: фамилия пользователя
    is_manger: является пользоватялль менеджером, где True - является, False - неявляется (для предоставления
    доступа к созданию, изменению и удалению существующих моделей опроса, групп вопросов)
    """
    username = None
    email = models.EmailField(unique=True, max_length=255)
    password = models.TextField()
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    auth_status = models.CharField(max_length=7, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Quiz(models.Model):
    """
    Модель опроса

    name: Название опроса
    description: Описание пороса
    date_created: Дата создания опроса
    quiz_max_grade: Максимальный балл за опрос
    """
    quiz_name = models.CharField(max_length=250)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now=True, db_index=True)
    quiz_max_grade = models.IntegerField()
    # TODO у опросов должна быть дата публикации, до наступления которой опрос пройти нельзя

class QuestionGroup(models.Model):
    """
    Модель группы вопросов
    group_name: название группы
    date_created: дата создания группы (автоматически)
    """
    group_name = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now=True, db_index=True)

class Question(models.Model):
    """
    Модель вопроса

    quiz: внешний ключ на моель опроса
    question: вопрос
    question_group: внешний ключ на модель группы вопросов
    multiple: определеяет возможное колличестов ответов на вопрос, где True - несколько ответов, False - один вариант ответа
    question_photo: картинка к вопросу в формате Text
    answer: ответ на вопрос в формате Text
    question_max_grade: максимальный балл за вопрос
    """
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=250)
    question_group = models.ForeignKey(QuestionGroup, related_name='questions', on_delete=models.CASCADE, null=True)
    multiple = models.BooleanField(default=False)
    question_photo = models.TextField(blank=True, default='')
    answer = models.TextField(blank=False)
    question_max_grade = models.IntegerField()

class Variant(models.Model):
    """
    Модель ваоианта ответа

    question: внешний ключ на модель вопроса
    variant: вариант ответа на вопрос
    score: оценка за вариант ответа
    """
    question = models.ForeignKey(Question, related_name='variants', on_delete=models.CASCADE, db_index=True)
    variant = models.CharField(max_length=30)
    score = models.IntegerField()

class UserAnswers(models.Model):
    """
    Модель пройденных опросов пользователя
    user_id: id пользователя, который заврешил опрос
    quiz_id: id опроса, который прошел пользователь
    quiz_name: название опроса, котрый прошел пользователь
    user_grade: оценка пользователя
    max_grade: максимальный балл за прозождение опроса
    """
    user_id = models.IntegerField()
    quiz_id = models.IntegerField()
    quiz_name = models.CharField(max_length=250)
    user_grade = models.IntegerField()
    max_grade = models.IntegerField()

class QuizStatistic(models.Model):
    """
    Молдель статистики опроса

    user_email: email пользователя
    quiz_name: название опроса
    user_grade: оценка пользователя за пройденный опрос
    quiz_max_grade: максимальный балл за опрос
    """
    user_email = models.EmailField(max_length=255)
    user_name = models.CharField(max_length=255, default='None')
    user_surname = models.CharField(max_length=255, default='None')
    quiz_name = models.CharField(max_length=250)
    date_of_completion = models.DateTimeField(auto_now=True, db_index=True)
    user_grade = models.IntegerField()
    quiz_max_grade = models.IntegerField()

class QuestionStatistic(models.Model):
    """
    Модель статистики вопроса

    quiz_statistic: внещний ключ на модель статистики опроса
    question_name: вопрос
    user_answer: ответ польщователя
    correct_answer: правлильный ответ
    user_grade: оценки пользователя
    question_max_grade: макимальный балл за вопрос
    """
    quiz_statistic = models.ForeignKey(QuizStatistic, related_name='questions_statistic', on_delete=models.CASCADE)
    question_name = models.CharField(max_length=250)
    user_answer = models.TextField()
    correct_answer = models.TextField()
    user_grade = models.IntegerField()
    question_max_grade = models.IntegerField()