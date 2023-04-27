# Web Socket Routing
from django.urls import re_path

from api.consumer.heart_beat import LastAvailableData

websocket_urlpatterns = [
    re_path(r"ws/last_data/$", LastAvailableData.as_asgi()),
]
