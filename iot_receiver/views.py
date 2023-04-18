from datetime import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializer import BasicSerializer, AccSerializer, GyroSerializer


class IoTProtoReceiever(APIView):

    REQUIRED_PARAMS = ["acc", "gyro", "heart"]

    def post(self, request):
        data = request.data
        print("{} : data received: ".format(datetime.utcnow()), data)

        for item in self.REQUIRED_PARAMS:
            if item not in data:
                return HttpResponse("missing params: {}".format(item), status=400)

        acc = data["acc"]
        gyro = data["gyro"]

        try:
            heart = float(data["heart"])
        except ValueError:
            return HttpResponse("heart: value errr", status=500)

        try:
            acc = list(float(i) for i in acc)
        except ValueError:
            return HttpResponse("acc: value errr", status=500)

        try:
            gyro = list(float(i) for i in gyro)
        except ValueError:
            return HttpResponse("gyro: value errr", status=500)

        basic_data = {
            "heart": heart
        }

        basic_serializer = BasicSerializer(data=basic_data)
        basic = None

        if basic_serializer.is_valid():
            basic = basic_serializer.save()
        else:
            print(basic_serializer.errors)
            return HttpResponse("basic serialization failed", status=500)

        acc_data = {
            "acc_x": acc[0],
            "acc_y": acc[1],
            "acc_z": acc[2],
            "connected_to": basic.pk,
        }
        acc_serializer = AccSerializer(data=acc_data)
        if acc_serializer.is_valid():
            acc_serializer.save()
        else:
            print(acc_serializer.errors)
            return HttpResponse("acc serialization failed", status=500)

        gyro_data = {
            "gyro_x": gyro[0],
            "gyro_y": gyro[1],
            "gyro_z": gyro[2],
            "connected_to": basic.pk,
        }
        gyro_serializer = GyroSerializer(data=gyro_data)
        if gyro_serializer.is_valid():
            gyro_serializer.save()
            print("{} : data saved: ".format(datetime.utcnow()), basic.pk)
            return HttpResponse("It worked - {}".format(basic.pk), status=202)
        else:
            print(gyro_serializer.errors)
            return HttpResponse("gyro serialization failed", status=500)
