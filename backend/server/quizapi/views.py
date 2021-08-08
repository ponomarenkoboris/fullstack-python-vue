from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import Quiz, User, Question
from . import serializers
import datetime, jwt

# TODO add jwt token checking for all routes

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

class QuestionListView(APIView):
    # TODO this logic can be done only if request was made by manager also create api for making questions groups

    def get(self, request):
        # token = request.COOKIES.get('jwt')
        # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        #
        # if payload['status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        questions_list = Question.objects.all()
        serialized_questions = serializers.QuestionSerializer(questions_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized_questions.data)

class CheckingUserAnswersView(APIView):
    def post(self, request):
        auth_token = request.COOKIES.get('jwt')

        payload = jwt.decode(auth_token, 'secret', algorithms=['HS256'])

        if not payload['status'] or payload['status'] != 'user':
           return Response(status=status.HTTP_401_UNAUTHORIZED, data={'Incorrect authorization'})

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
        is_manager = request.data['is_manager']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        if user.is_manager != is_manager:
            raise AuthenticationFailed('Incorrect authentication status')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'status': user.is_manager
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