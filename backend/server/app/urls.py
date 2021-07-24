from django.urls import path
from .views import *

urlpatterns = [
    path('auth/user/register', RegisterView.as_view()),
    path('auth/user/login', LoginView.as_view()),
    path('auth/user/user', UserView.as_view()),
    path('auth/user/logout', LogoutView.as_view()),
    # path('admin/show-statistic'),
    # path('admin/create-quiz', CreateQuizView.as_view())
]
