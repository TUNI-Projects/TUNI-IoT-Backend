from django.contrib import admin
from django.urls import path, include
from iot_receiver.views import IoTProtoReceiever

urlpatterns = [
    path('data/', IoTProtoReceiever.as_view()),
]
