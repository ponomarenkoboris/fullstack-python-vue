from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# class QuizSerializer(serializers.ModelSerializer):
#     class MetaL:
#         # model = Quiz
#         fields = ['id', 'name', 'description', 'questions']
#
#     def create(self, validated_data):
#         instance = self.Meta.model(**validated_data)
#         instance.save()
#         return instance

# class StatisticSerializer(serializers.ModelSerializer):
#     class Meta:
#         # model = Statistic
#         # fields = ['id', '']