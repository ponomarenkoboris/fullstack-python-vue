from rest_framework import serializers
from .models import Variant, Quiz, Question, User, QuestionGroup, UserAnswers, QuestionStatistic, QuizStatistic

class VariantSerializer(serializers.ModelSerializer):
    """
    Сериащизация модели вариантов ответа
    """
    class Meta:
        model = Variant
        fields = ['id', 'variant', 'score']

class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализация модели вопросов
    """
    variants = VariantSerializer(many=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'question',
            'variants',
            'answer',
            'multiple',
            'question_photo',
            'question_group',
            'question_max_grade'
        ]
        ordering = ['question_group']

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        questions_instance = Question.objects.create(**validated_data)

        for variant in variants_data:
            Variant.objects.create(question=questions_instance, **variant)

        return questions_instance

class QuizSerializer(serializers.ModelSerializer):
    """
    Сериализация модели опросов
    """
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'quiz_name', 'description', 'questions', 'quiz_max_grade']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz_instance = Quiz.objects.create(**validated_data)

        for question in questions_data:
            variants_data = question.pop('variants')
            question_instance = Question.objects.create(quiz=quiz_instance, **question)

            for variant in variants_data:
                Variant.objects.create(question=question_instance, **variant)

        return quiz_instance


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалищация модели пользователя
    """

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'surname', 'password', 'auth_status']
        extra_kwargs = {
            'password': {'write_only': True},
            'auth_status': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_instance = self.Meta.model(**validated_data)

        if password is not None:
            user_instance.set_password(password)

        user_instance.save()
        return user_instance

# Question group serializer
class QuestionGroupSerializer(serializers.ModelSerializer):
    """
    Сериализация группы вопросов
    """
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionGroup
        fields = ['id', 'group_name', 'date_created', 'questions']

    def create(self, validated_data):
        questions = validated_data.pop('questions')

        if (len(questions)) == 0:
            return QuestionGroup.objects.create(**validated_data)

        group_instance = QuestionGroup.objects.create(**validated_data)
        for question in questions:
            variants_data = question.pop('variants')
            question_instance = Question.objects.create(question_group=group_instance, **question)

            for variant in variants_data:
                Variant.objects.create(question=question_instance, **variant)

        return group_instance

    def update(self, instance, validated_data):
        instance.group_name = validated_data.pop('group_name')

        for question in validated_data.pop('questions'):
            variants_data = question.pop('variants')
            question_instance = Question.objects.create(question_group=instance, **question)

            for variant in variants_data:
                Variant.objects.create(question=question_instance, **variant)

        return instance

# Сериализация модели ответов на вопросы
class UserAnswersSerializer(serializers.ModelSerializer):
    """
    Сериализация модели пользовательских ответов на вопросы
    """
    class Meta:
        model = UserAnswers
        fields = [
            'id',
            'user_id',
            'quiz_id',
            'quiz_name',
            'user_grade',
            'max_grade'
        ]


# Сериализация статистики вопросов в опросе
class QuestionStatisticSerializer(serializers.ModelSerializer):
    """
    Сериализация статистики вопросов в опросе
    """
    class Meta:
        model = QuestionStatistic
        fields = [
            'id',
            'question_name',
            'user_answer',
            'correct_answer',
            'user_grade',
            'question_max_grade'
        ]

# Сериализация статистики прохождения опросов
class QuizStatisticSerializer(serializers.ModelSerializer):
    """
    Сериализация статистики прохождения опросов
    """
    questions_statistic = QuestionStatisticSerializer(many=True)

    class Meta:
        model = QuizStatistic
        fields = [
            'id',
            'quiz_name',
            'user_grade',
            'quiz_max_grade',
            'user_email',
            'questions_statistic'
        ]

    def create(self, validated_data):
        questions_statistic = validated_data.pop('questions_statistic')
        quiz_statistic_instance = QuizStatistic.objects.create(**validated_data)

        for question in questions_statistic:
            QuestionStatistic.objects.create(quiz_statistic=quiz_statistic_instance, **question)

        return quiz_statistic_instance