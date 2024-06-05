from django.urls import path

from chat_module.views import *

urlpatterns = [
    path('api/rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('api/rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('api/message/', MessageListAPIView.as_view(), name='message-list'),
    path('api/message/<int:pk>/', MessageDetailsAPIView.as_view(), name='message-detail'),
]