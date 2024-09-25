
from .consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('chat/<slug:grpslug>/',ChatConsumer.as_asgi())
]