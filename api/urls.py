from django.contrib import admin
from django.urls import path, include
from api.v1.records import Records

urlpatterns = [
    path('records/', Records.as_view()),
]
