from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from TelegramBotProject.settings import TELEGRAM_BOT_TOKEN
from .models import TelegramUser, BotToken, Message
from .serializers import UserSerializer, MessageSerializer
from .telegram_send_msg import send_message_to_telegram
import uuid

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        unique_token = str(uuid.uuid4())[:8]  

        BotToken.objects.create(user=user, token=unique_token)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token, created = BotToken.objects.get_or_create(user=request.user)

        if created:
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return response
    
class SendMessageView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
            token = request.data['token']
            message = request.data['message']

            telegram_user = TelegramUser.objects.get(telegram_token=token)
            chat_id = telegram_user.chat_id
            username = telegram_user.username

            send_message_to_telegram(token=TELEGRAM_BOT_TOKEN, username=username, chat_id=chat_id, message=message)

            message = Message.objects.create(user=telegram_user.user, text=message)

            return Response({'message': 'Message sent successfully'}, status=status.HTTP_200_OK)

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
   
        user = request.user
        messages = Message.objects.filter(user=user)
        
        serializer = MessageSerializer(messages, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)