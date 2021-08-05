from rest_framework import serializers
from .models import Variant, Quiz, Question, User

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'variant']

class QuestionSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'variants', 'answer', 'multiple']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'questions']

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
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'surname', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_instance = self.Meta.model(**validated_data)

        if password is not None:
            user_instance.set_password(password)

        user_instance.save()
        return user_instance