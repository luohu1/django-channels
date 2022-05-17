from django.urls import path

from example import consumers as example_consumers

websocket_urlpatterns = [
    path('ws/chat/', example_consumers.ChatConsumer.as_asgi()),
]
