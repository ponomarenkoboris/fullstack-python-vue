from rest_framework import serializers
from quiz.models import Quiz, User


class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'vin', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_email', 'user_password']
