from django.urls import path
from quiz.views import *

app_name = 'question'
urlpatterns = [
    path('question/create', QuizCreateView.as_view()),
    path('question/all', QuizListView.as_view()),
    path('question/detail/<int:pk>', QuizDetailView.as_view()),
    path('user/create', UserCreateView.as_view()),
    path('user/all', UserListView.as_view()),
]
