from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import Quiz, User, Question, QuestionGroup
from . import serializers
import datetime, jwt

# TODO add jwt token checking for all routes
# def check_manager_access(cookies = None):
#     if cookies is None:
#         return False
#
#     token = cookies.get('jwt')
#     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#
#     if payload['status'] != 'manager':
#         return False
#     return True

class QuizView(APIView):
    def post(self, request):
        """
        Создание опроса
        """
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

    def get(self, request):
        """
        Получение списка всех опросов
        """
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
    """
    Оцека ответов на опрос
    """
    def post(self, request):
        quiz_id = request.data.pop('quizId')
        answers = request.data.pop('answers')

        for answer in answers:
            question_id = answer.pop('questionId')
            question = Question.objects.all().filter(id=question_id).first()
            serialized_question = serializers.QuestionSerializer(question)
            # TODO поиск подстроки ответа пользователя в строке ответа на вопрос
            # TODO формирование словаря
            # { "id_вопроса": id, "question": вопрос, "user_answer": ответ_пользователя, "user_grade": баллы_за_вопрос, "max_grade": максимальный_балл }
            pass

        return Response()

class RegisterView(APIView):
    def post(self, request):
        new_user = serializers.UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()
        return Response(status=status.HTTP_201_CREATED, data=new_user.data)

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

class LogoutView(APIView):
    def post(self):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# Question Group
class QuestionGroupView(APIView):
    def get(self, request):
        groups = QuestionGroup.objects.all()
        serialized_groups = serializers.QuestionGroupSerializer(groups, many=True)
        return Response(data=serialized_groups.data)

    def post(self, request):
        """
        Создание новой группы вопросов
        """
        new_group = serializers.QuestionGroupSerializer(data=request.data)
        new_group.is_valid(raise_exception=True)
        new_group.save()
        return Response(status=status.HTTP_201_CREATED, data=new_group.data)

    def put(self, request):
        """
        Добавление вопросов в группу
        """
        group_name = request.data['group_name']
        group = QuestionGroup.objects.all().filter(group_name=group_name).first()
        updated_group = serializers.QuestionGroupSerializer(instance=group, data=request.data)
        updated_group.is_valid(raise_exception=True)
        updated_group.save()

        return Response(data=updated_group.data)

    def delete(self, request):
        """
        Удаление группы вопросов
        """
        QuestionGroup.objects.filter(id=request.data.pop('group_id')).delete()
        groups = QuestionGroup.objects.all()
        serialized_group = serializers.QuestionGroupSerializer(groups, many=True)
        return Response(data=serialized_group.data)
