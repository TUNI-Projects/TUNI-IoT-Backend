from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime, timedelta
from iot_receiver.models import data as data_db, gyro, acc


class Records(APIView):

    OPTIONAL_PARAMETER = ("start_date", "end_date", "choice")
    """
    start_date: from, defaults to None
    end_date: to, defaults to None
    choice: acc, heart, gyro, default to acc
    
    This API doesn't return all records. It only returns what's ordered.
    """

    def get(self, request):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        choice = request.GET.get('choice', "acc")

        if choice not in ["heart", "gyro", "acc"]:
            return JsonResponse({
                "message": "Invalid Option!"
            }, status=400)

        if start_date is not None:
            try:
                start_date = int(start_date)
                start_date = datetime.fromtimestamp(
                    start_date)  # possible error
            except ValueError:
                return JsonResponse({
                    "message": "Invalid Value as datetime"
                }, status=400)

        if end_date is not None:
            try:
                end_date = int(end_date)
                end_date = datetime.fromtimestamp(end_date)  # possible error
            except ValueError:
                return JsonResponse({
                    "message": "Invalid Value as datetime"
                }, status=400)

        if (start_date is not None and end_date is None) or (start_date is None and end_date is not None):
            return JsonResponse({
                "message": "Invalid parameter. Both from and to is needed!"
            }, status=400)
        
        if (end_date - start_date).days > 1:
            return JsonResponse({
                "message": "Maximum 1 day worth of data record is supported!"
            }, status=400)

        if choice == "gyro":
            if start_date is None:
                data = list(gyro.objects.all().order_by("-created_on"))
            else:
                data = list(gyro.objects.filter(
                    created_on__gte=start_date, created_on__lt=end_date).order_by('-created_on'))

            payload = list()
            for item in data:
                payload.append({
                    "index": item.index,
                    "gyro_x": item.gyro_x,
                    "gyro_y": item.gyro_y,
                    "gyro_z": item.gyro_z,
                    "created_on": item.created_on,
                })

            return JsonResponse({
                "choice": choice,
                "total": len(payload),
                "payload": payload,
            })
        elif choice == "acc":
            if start_date is None:
                data = list(acc.objects.all().order_by("-created_on"))
            else:
                data = list(acc.objects.filter(
                    created_on__gte=start_date, created_on__lt=end_date).order_by('-created_on'))

            payload = list()
            for item in data:
                payload.append({
                    "index": item.index,
                    "acc_x": item.acc_x,
                    "acc_y": item.acc_y,
                    "acc_z": item.acc_z,
                    "created_on": item.created_on,
                })
            return JsonResponse({
                "choice": choice,
                "total": len(payload),
                "payload": payload,
            })
        else:
            if start_date is None:
                data = list(data_db.objects.all())
            else:
                data = list(data_db.objects.filter(
                    created_on__gte=start_date, created_on__lt=end_date).order_by('-created_on'))

            payload = list()
            for item in data:
                payload.append({
                    "index": item.id,
                    "heart": item.heart,
                    "created_on": item.created_on,
                })
            return JsonResponse({
                "choice": choice,
                "total": len(payload),
                "payload": payload,
            })
