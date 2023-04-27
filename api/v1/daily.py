from django.http import JsonResponse
from rest_framework.views import APIView
from iot_receiver.models import data as data_db, gyro, acc
from datetime import datetime


class DailyRecord(APIView):
    
    def get(self, request):
        """
        this is a daily record, current date

        Args:
            request (_type_): _description_
        """
        frm = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        to = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=0)
        
        data = list(data_db.objects.filter(
                    created_on__gte=frm, created_on__lt=to).order_by('-created_on'))
        
        max = 0
        max_recorded_at = None
        avg = 0
        
        
        for item in data:
            if item.heart >= max:
                max = item.heart
                max_recorded_at = item.created_on
            avg += item.heart
        try:
            avg = avg / len(data)
        except ZeroDivisionError:
            avg = 0
        
        return JsonResponse({
            "choice": "heart",
            "max": max,
            "recorded_at": max_recorded_at,
            "avg": avg
        })
