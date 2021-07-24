from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserSerializer, QuizSerializer
import jwt, datetime

# Регистрация пользователя
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Вход пользователя
class LoginView(APIView):
    def post(self, request):
        print(request.data)
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

# Проверка авторизации (аутентификация)
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Выход из приложения
class LogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Success'
        }

        return response

# Создание опроса
# class CreateQuizView(APIView):
#     def post(self, request):
#         serializer = QuizSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({
#             'message': 'Quiz was successfully created'
#         })

# Получение статистикик
# class StatisticLisView(APIView):
#     def get(self):
#         statistic_list = Quiz.objects.all()
#         return Response({
#             'statistic': statistic_list
#         })