from django.urls import path

from example import consumers as example_consumers

websocket_urlpatterns = [
    path('ws/echo/', example_consumers.EchoConsumer.as_asgi()),
]
