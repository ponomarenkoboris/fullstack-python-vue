from django.urls import path
from . import views

urlpatterns = [
    path('quiz-create/', views.QuizCreateView.as_view()),
    path('quiz-list/', views.QuizListView.as_view())
]