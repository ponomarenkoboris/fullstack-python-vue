from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz
from . import serializers

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
        quiz = Quiz.objects.filter(id=request.data.pop('quizId'))
        serialized_quiz = serializers.QuizSerializer(quiz, many=True)
        needed_quiz = list(serialized_quiz.data).copy()

        # TODO сделать проверку ответов на вопросы
        print(needed_quiz)

        return Response()
