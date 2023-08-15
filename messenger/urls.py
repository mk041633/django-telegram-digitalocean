from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('send-message/', views.SendMessageView.as_view(), name='send-message'),
    path('message-list/', views.MessageListView.as_view(), name='message-list'),
]
