from django.urls import path
from .views import ChatRoom,Join_Group,add_msg,forward_msg
urlpatterns = [
    path('<str:grpslug>/',ChatRoom,name='chat-room'),
    path('join-group/<slug:grpslug>',Join_Group,name='join-group'),
    path('user/add-msg/',add_msg,name='add-msg'),
    path('group/forward-msg/',forward_msg,name='forward-msg'),
]