from django.urls import re_path, path

from . import consumers
from .F5040 import consumers5040
from .Hamkadeh_fellows import consumersSaleHamkadeh
websocket_urlpatterns = [
    path('ws/voip/' , consumers.SocketConsumer.as_asgi()),
    path('ws/voip/5040/' , consumers5040.SocketConsumer.as_asgi()),
    path('ws/voip/sale/hamkadeh/' , consumersSaleHamkadeh.SocketConsumer.as_asgi())

]
