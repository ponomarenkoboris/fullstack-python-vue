from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import Quiz, User
from . import serializers
import datetime, jwt

class QuizCreateView(APIView):
    def post(self, request):
        serialized_quiz = serializers.QuizSerializer(data=request.data)
        if serialized_quiz.is_valid():
            serialized_quiz.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Quiz created successfully"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serialized_quiz.errors
        })

class QuizListView(APIView):
    def get(self, request):
        quiz_list = Quiz.objects.all()
        serialized_quiz = serializers.QuizSerializer(quiz_list, many=True)
        serialized_quiz_copy = list(serialized_quiz.data).copy()

        # TODO try to change this algorithm
        for quiz in serialized_quiz_copy:
            for key in quiz:
                if key == 'questions':
                    for question in quiz['questions']:
                        for answer in list(question):
                            if answer == 'answer':
                                del question[answer]

        return Response(serialized_quiz_copy)


class CheckingUserAnswersView(APIView):
    def post(self, request):
        quiz = Quiz.objects.filter(id=request.data.pop('quizId')).first()
        serialized_quiz = serializers.QuizSerializer(quiz, many=True)
        needed_quiz = list(serialized_quiz.data).copy()

        # TODO сделать проверку ответов на вопросы
        print(needed_quiz)

        return Response()

class RegisterView(APIView):
    def post(self, request):
        new_user = serializers.UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        return Response(status=status.HTTP_201_CREATED, data=new_user.data)

class LoginView(APIView):
    def post(self, request):
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
            'jwt': token,
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
           payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serialized_user = serializers.UserSerializer(user)
        return Response(serialized_user.data)

class LogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response