from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import Quiz, User, Question, QuestionGroup, UserAnswers, QuizStatistic
from . import serializers
import json, jwt
from .jwt_methods import get_data_from_jwt, set_jwt

class QuizView(APIView):
    def post(self, request):
        """
        Создание опроса
        """
        # payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

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
        :return: Объект из двух списокв:
                quiz_list - список не пройденных опросов,
                done_quiz_list - список пройденных вопросов
        """

        payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['status'] != 'worker':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        user_answers = UserAnswers.objects.filter(user_id=payload['id'])
        serialized_answers = serializers.UserAnswersSerializer(user_answers, many=True)
        user_answers = json.loads(json.dumps(serialized_answers.data))

        quiz_ids = []
        for answer in user_answers:
            quiz_ids.append(answer['quiz_id'])

        quiz_list = Quiz.objects.exclude(id__in=quiz_ids)
        serialized_quiz = serializers.QuizSerializer(quiz_list, many=True)
        quiz_list = json.loads(json.dumps(serialized_quiz.data))

        if len(quiz_list) != 0:
            for quiz in quiz_list:
                del quiz['quiz_max_grade']
                for question in quiz['questions']:
                    del question['answer']
                    del question['question_max_grade']

                    for variant in question['variants']:
                        del variant['score']

        return Response(status=status.HTTP_200_OK, data={
            "quiz_list": quiz_list,
            "done_quiz_list": user_answers
        })

class QuestionListView(APIView):

    def get(self, request):
        # payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        questions_list = Question.objects.all()
        serialized_questions = serializers.QuestionSerializer(questions_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized_questions.data)

class RegisterView(APIView):
    def post(self, request):
        """
        Регистрайия пользователя
        """
        new_user = serializers.UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()

        token = set_jwt(new_user.data['id'], request.data['auth_status'])

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = new_user.data

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
           payload = get_data_from_jwt(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serialized_user = serializers.UserSerializer(user)
        return Response(serialized_user.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        auth_status = request.data['auth_status']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        if user.auth_status != auth_status:
            raise AuthenticationFailed('Incorrect authentication status')

        token = set_jwt(user.id, user.auth_status)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
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
        # payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['auth_status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        groups = QuestionGroup.objects.all()
        serialized_groups = serializers.QuestionGroupSerializer(groups, many=True)
        return Response(data=serialized_groups.data)

    def post(self, request):
        """
        Создание новой группы вопросов
        """
        # payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['auth_status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        new_group = serializers.QuestionGroupSerializer(data=request.data)
        new_group.is_valid(raise_exception=True)
        new_group.save()
        return Response(status=status.HTTP_201_CREATED, data=new_group.data)

    def put(self, request):
        """
        Добавление вопросов в группу
        """
        # payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['auth_status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

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
        payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        if payload is False or payload['auth_status'] != 'manager':
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        QuestionGroup.objects.filter(id=request.data.pop('group_id')).delete()
        groups = QuestionGroup.objects.all()
        serialized_group = serializers.QuestionGroupSerializer(groups, many=True)
        return Response(data=serialized_group.data)

# Оценка прохождения опроса и формирование статистики
class GradingUser(APIView):
    def post(self, request):
        quiz_id = request.data['quizId']
        answers = request.data['answers']

        payload = get_data_from_jwt(request.COOKIES.get('jwt'))

        # if payload is False or payload['status'] != 'worker':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        quiz_statistic = {}

        quiz_instance = Quiz.objects.all().filter(id=quiz_id).first()
        serialized_quiz = serializers.QuizSerializer(quiz_instance)
        quiz_instance = json.loads(json.dumps(serialized_quiz.data))
        quiz_statistic['quiz_name'] = quiz_instance['quiz_name']

        user_instance = User.objects.filter(id=payload['id']).first()
        serialized_user = serializers.UserSerializer(user_instance)
        quiz_statistic['user_email'] = serialized_user.data['email']

        quiz_name = quiz_instance['quiz_name']
        quiz_max_grade = quiz_instance['quiz_max_grade']
        quiz_statistic['quiz_max_grade'] = quiz_max_grade
        user_score = 0

        def searchEl(variant, variant_instance):
            for item in variant_instance:
                if item['variant'] == variant:
                    return item['score']

        question_statistic = []

        for answer in answers:
            question_id = answer.pop('questionId')
            question_instance = Question.objects.all().filter(id=question_id).first()
            serialized_question = serializers.QuestionSerializer(question_instance)
            question_instance = json.loads(json.dumps(serialized_question.data))
            question_user_grade = 0

            for user_answer in answer['answer'].split(','):
                exist = question_instance['answer'].find(user_answer)

                if exist != -1:
                    user_score += searchEl(user_answer, question_instance['variants'])
                    question_user_grade += searchEl(user_answer, question_instance['variants'])

            question_statistic.append({
                "question_name": question_instance['question'],
                "user_answer": answer['answer'],
                "correct_answer": question_instance['answer'],
                "user_grade": question_user_grade,
                "question_max_grade": question_instance['question_max_grade'],
            })

            question_user_grade = 0

        quiz_statistic['questions_statistic'] = question_statistic
        quiz_statistic['user_grade'] = user_score

        quiz_statistic_instance = serializers.QuizStatisticSerializer(data=quiz_statistic)
        quiz_statistic_instance.is_valid(raise_exception=True)
        quiz_statistic_instance.save()

        user_answer = {
            "user_id": payload['id'],
            "quiz_id": quiz_id,
            "quiz_name": quiz_name,
            "user_grade": user_score,
            "max_grade": quiz_max_grade
        }

        user_answer_instance = serializers.UserAnswersSerializer(data=user_answer)
        user_answer_instance.is_valid(raise_exception=True)
        user_answer_instance.save()

        return Response(status=status.HTTP_201_CREATED, data={
            "message": "Replies saved successfully",
            "statistic": quiz_statistic
        })


# Отправка менеджеру полной статистики прохождения опросов
class StatisticView(APIView):
    def get(self, request):
        # payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        # if payload is False or payload['auth_status'] != 'manager':
        #     return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})

        quiz_statistic_instance = QuizStatistic.objects.all()
        serialized_statistic = serializers.QuizStatisticSerializer(quiz_statistic_instance, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized_statistic.data)