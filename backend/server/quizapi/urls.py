from django.urls import path
from .views import *


urlpatterns = [

    path('user-grading/', GradingUser.as_view()), # Маршрут оценки пользователя

    path('questions-list/', QuestionListView.as_view()), # get - получение списка вопросов
    path('questions-group/', QuestionGroupView.as_view()), # get - получение списка групп вопросов, post - создание новой группы вопросов, put - изменение группы вопросов
    path('quiz-full-statistic/', StatisticView.as_view()),

    path('quiz-list/', QuizView.as_view()), # get - получение списка опросов, post - срздание нового опроса
    path('register/', RegisterView.as_view()), # post - регистрация пользователя
    path('login/', LoginView.as_view()), # post - логин пользователя
    path('auth/', UserView.as_view()), # post - авторизовация пользователя
    path('logout/', LogoutView.as_view()) # post - вызод пользователя
]
