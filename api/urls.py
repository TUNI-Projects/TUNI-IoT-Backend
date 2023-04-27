from django.contrib import admin
from django.urls import path, include
from api.v1.records import Records
from api.v1.daily import DailyRecord

urlpatterns = [
    path('records/', Records.as_view()),
    path('daily/', DailyRecord.as_view()),
]
