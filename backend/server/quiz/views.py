from django.shortcuts import render
from rest_framework import generics
from quiz.serializers import *
from quiz.models import Quiz

# Создание ворпоса
class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizDetailSerializer

# Просмотр всех вопросов
class QuizListView(generics.ListAPIView):
    serializer_class = QuizListSerializer
    queryset = Quiz.objects.all()

# Редактирование конкретного вопроса
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuizDetailSerializer
    queryset = Quiz.objects.all()

# Создание пользователя
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

# Список всех пользователей
class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
