from rest_framework import serializers
from .models import Variant, Quiz, Question, User, QuestionGroup

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'variant']

class QuestionSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'variants', 'answer', 'multiple', 'question_photo']

# Question group serializer
class QuestionGroupSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuestionGroup
        fields = ['id', 'group_name', 'date_created', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        group_instance = QuestionGroup.objects.create(**validated_data)

        for question in questions_data:
            variants_data = question.pop('variants')
            question_instance = Question.objects.create(question_group=group_instance, **question)

            for variant in variants_data:
                Variant.objects.create(question=question_instance, **variant)

        return group_instance

    def update(self, instance, validated_data):
        # TODO complete update method
        pass
#

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
        fields = ['id', 'name', 'email', 'surname', 'password', 'is_manager']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_manager': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_instance = self.Meta.model(**validated_data)

        if password is not None:
            user_instance.set_password(password)

        user_instance.save()
        return user_instance