from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TelegramUser, BotToken, Message

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    def get_token(self, user):
        token, created = BotToken.objects.get_or_create(user=user)
        return token.token
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'token')

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'

class BotTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotToken
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['timestamp', 'text']