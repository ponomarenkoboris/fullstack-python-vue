from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('auth/user/register', RegisterView.as_view()),
    path('auth/user/login', LoginView.as_view()),
    path('auth/user/user', UserView.as_view()),
    path('auth/user/logout', LogoutView.as_view()),
]
