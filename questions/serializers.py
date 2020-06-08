from rest_framework import serializers
from .models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# admin register serializer
class CreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        admin = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        admin.set_password(validated_data['password'])
        admin.is_staff = True
        add_permission = Permission.objects.get(name='Can add question')
        view_permission = Permission.objects.get(name='Can view question')
        change_permission = Permission.objects.get(name='Can change question')
        delete_permission = Permission.objects.get(name='Can delete question')
        view_answer = Permission.objects.get(name='Can view answer')

        admin.save()
        admin.user_permissions.add(
            add_permission,
            view_permission,
            change_permission,
            delete_permission,
            view_answer
        )
        return admin


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'owner']


class QuestionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionTitleSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'choice', 'user']

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

