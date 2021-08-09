from django.urls import path
from .views import *

urlpatterns = [
    path('quiz-create/', QuizCreateView.as_view()),
    path('quiz-list/', QuizListView.as_view()),
    path('user-quiz-answer/', CheckingUserAnswersView.as_view()),
    path('questions-list/', QuestionListView.as_view()),

    path('questions-group/', QuestionGroupView.as_view()),

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('auth/', UserView.as_view()),
    path('logout/', LogoutView.as_view())
]