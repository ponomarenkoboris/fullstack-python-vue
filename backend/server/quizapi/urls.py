from django.urls import path
from .views import *

urlpatterns = [
    path('quiz-create/', QuizCreateView.as_view()),
    path('quiz-list/', QuizListView.as_view()),
    path('user-quiz-answer/', CheckingUserAnswersView.as_view())
]