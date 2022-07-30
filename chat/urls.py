from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('friends/<str:pk>', views.detail, name="detail"),
    path('sent_msg/<str:pk>', views.sent_messages, name="sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name="rec_msg"),
    path('notification', views.chatNotification, name="notification"),
    path('search-friends', views.search_list_view, name='search_list_view')
    
]
