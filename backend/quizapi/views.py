from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .models import Quiz, User, Question, QuestionGroup, UserAnswers, QuizStatistic
from .jwt_methods import get_data_from_jwt, set_jwt
from . import serializers
import json, time, jwt

class QuizView(APIView):
    """
    API для взаимодействия с опросами
    """
    def post(self, request):
        """
        Создание опроса
        
        expect:
            request COOKIE: csrf token and jwt token
            request data: dict({ models.Quiz })

        return:
            response COOKIE: csrf token and jwt token
            data: dict({ status: int, message: str })
        """
        token = request.COOKIES.get('jwt')
        try:
            payload = get_data_from_jwt(token)
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

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

        expect:
            request COOKIE: csrf token and jwt token

        return:
            data: dict({ models.Quiz })
        """

        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'worker':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        user_answers = UserAnswers.objects.filter(user_id=payload['id'])
        serialized_answers = serializers.UserAnswersSerializer(user_answers, many=True)
        user_answers = json.loads(json.dumps(serialized_answers.data))

        quiz_ids = [answer['quiz_id'] for answer in user_answers]

        quiz_list = Quiz.objects.exclude(id__in=quiz_ids)
        serialized_quiz = serializers.QuizSerializer(quiz_list, many=True)
        quiz_list = json.loads(json.dumps(serialized_quiz.data))
        current_time = round(time.time())
        avaliable_list = [quiz for quiz in quiz_list if quiz['publish_date'] <= current_time]

        if len(avaliable_list) != 0:
            for quiz in avaliable_list:

                del quiz['quiz_max_grade']
                for question in quiz['questions']:
                    del question['answer']
                    del question['question_max_grade']

                    for variant in question['variants']:
                        del variant['score']

        return Response(status=status.HTTP_200_OK, data={
            "quiz_list": avaliable_list,
            "done_quiz_list": user_answers
        })

class QuestionListView(APIView):
    """
    API для получения списка вопросов
    """
    def get(self, request):
        """
        Получение списка вопросов

        expect:
            request COOKIE: csrf token and jwt token

        return:
            response COOKIE: csrf token and jwt token
            data: dict({ models.User })
        """
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        questions_list = Question.objects.all()
        serialized_questions = serializers.QuestionSerializer(questions_list, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized_questions.data)

class RegisterView(APIView):
    """
    API для рагистрации пользователя
    """
    def post(self, request):
        """
        Регистрайия пользователя

        expect:
            request COOKIE: csrf token and jwt token
            request data: dict({ email: str })

        return:
            response COOKIE: csrf token and jwt token
            data: dict({ models.User })
        """
        new_user = serializers.UserSerializer(data=request.data)
        new_user.is_valid(raise_exception=True)
        new_user.save()

        token = set_jwt(new_user.data['id'], request.data['auth_status'])

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True, path='/')
        response.data = new_user.data

        return response

class RefreshView(APIView):
    """
    API для обновление JWT токена
    """
    def post(self, request):
        """
        Обновление JWT токена

        expect:
            request COOKIE: jwt token
            request data: dict({ email: str })

        return:
            response COOKIE: jwt token
        """
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = get_data_from_jwt(token)
            user = User.objects.filter(id=payload['id']).first()
            serialized_user = serializers.UserSerializer(user)
            if serialized_user is None:
                return Response(status=status.HTTP_404_NOT_FOUND, data={ 'message': 'User not found' })
        except jwt.ExpiredSignatureError:
            user_email = request.data['email']
            user_instance = User.objects.filter(email=user_email).first()
            serialized_user = serializers.UserSerializer(user_instance)
            token = set_jwt(serialized_user.data.pop('id'), serialized_user.data.pop('auth_status'))

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True, path='/')
            response.status_code = 200
            return response

        return Response(status=status.HTTP_200_OK)

class LoginView(APIView):
    """
    API для входа пользователя в систему

    """
    def post(self, request):
        """
        Вхдо в систему

        expect: 
            request data: dict({ email: str, password: str, auth_status: str })
    
        return: 
            COOKIE: csrf token and jwt token
            data: dict({ name: str, email: str, surname: str })
        """
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
        response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True, path='/')        
        response.data = {
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        }
        return response

class LogoutView(APIView):
    """
    API для выхода пользователя из системы

    """
    def post(self, request):
        """
        Выход из системы

        expect:
            request COOKIE: csrf token and jwt token

        return:
            dict({ message: str })
        """
        response = Response()
        response.delete_cookie(key='jwt', samesite='None', path='/')
        response.delete_cookie(key='jwt')
        response.status = status.HTTP_200_OK

        response.data = {
            'message': 'success'
        }
        return response

class QuestionGroupView(APIView):
    """
    API для управления группами вопросов
    """
    def get(self, request):
        """
        Поучение списка групп вопросов

        expect:
            request COOKIE: csrf token and jwt token

        return: 
            data: list(models.QuestionGroup)
        """
        
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        groups = QuestionGroup.objects.all()
        serialized_groups = serializers.QuestionGroupSerializer(groups, many=True)
        return Response(data=serialized_groups.data)

    def post(self, request):
        """
        Создание новой группы вопросов

        expect:
            request COOKIE: csrf token and jwt token
            request data: dict({ group_name: str, questions: list(empty) })
        return:
            data: list(models.QuestionGroup)
        """
        
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        new_group = serializers.QuestionGroupSerializer(data=request.data)
        new_group.is_valid(raise_exception=True)
        new_group.save()
        return Response(status=status.HTTP_201_CREATED, data=new_group.data)

    def put(self, request):
        """
        Добавление вопросов в группу

        expect:
            request COOKIE: csrf token and jwt token
            request data: dict({ group_name: str, questions: list(models.Question) })
        return:
            data: list(models.QuestionGroup)
        """
        
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        group_name = request.data['group_name']
        group = QuestionGroup.objects.all().filter(group_name=group_name).first()
        updated_group = serializers.QuestionGroupSerializer(instance=group, data=request.data)
        updated_group.is_valid(raise_exception=True)
        updated_group.save()

        return Response(data=updated_group.data)

    def delete(self, request):
        """
        Удаление группы вопросов

        expect:
            request COOKIE: csrf token and jwt token
            request data: dict({ group_id: int })

        return: 
            data: list(models.QuestionGroup)
        """
        
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        QuestionGroup.objects.filter(id=request.data.pop('group_id')).delete()
        groups = QuestionGroup.objects.all()
        serialized_group = serializers.QuestionGroupSerializer(groups, many=True)
        return Response(data=serialized_group.data)

class GradingUser(APIView):
    """
    API для оценки ответа пользователя
    """
    def post(self, request):
        """
        Оценка пользователя

        expect:
            request COOKIE: csrf token and jwt token
            request data: dict({ quizId: int, answers: list({ questionId: int, answer: str }) })

        return:
            data: dict({ message: str: success: boolean })
        """
        quiz_id = request.data['quizId']
        answers = request.data['answers']

        payload = get_data_from_jwt(request.COOKIES.get('jwt'))
        
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'worker':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        quiz_statistic = {}

        quiz_instance = Quiz.objects.all().filter(id=quiz_id).first()
        serialized_quiz = serializers.QuizSerializer(quiz_instance)
        quiz_instance = json.loads(json.dumps(serialized_quiz.data))
        quiz_statistic['quiz_name'] = quiz_instance['quiz_name']

        user_instance = User.objects.filter(id=payload['id']).first()
        serialized_user = serializers.UserSerializer(user_instance)
        quiz_statistic['user_email'] = serialized_user.data['email']
        quiz_statistic['user_name'] = serialized_user.data['name']
        quiz_statistic['user_surname'] = serialized_user.data['surname']

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

                if len(user_answer) == 0 or user_answer is None:
                    exist = -1
                else:
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
            "success": True
        })


class StatisticView(APIView):
    """
    API для просмотра статистики прохождения опросов (для менеджера)
    """
    def get(self, request):
        """
        expext:
            request COOKIE: csrf token and jwt token

        return: 
            data: list(QuestionStatistic)
        """
        try:
            payload = get_data_from_jwt(request.COOKIES.get('jwt'))
            if payload is False or payload['status'] != 'manager':
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'Incorrect authorization'})
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'ExpiredSignatureError'})

        quiz_statistic_instance = QuizStatistic.objects.all()
        serialized_statistic = serializers.QuizStatisticSerializer(quiz_statistic_instance, many=True)
        return Response(status=status.HTTP_200_OK, data=serialized_statistic.data)