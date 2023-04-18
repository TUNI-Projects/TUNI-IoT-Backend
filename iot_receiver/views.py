from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView

# Create your views here.

class IoTProtoReceiever(APIView):
    
    REQUIRED_PARAMS = ["acc", "gyro", "heart"]
    
    def post(self, request):
        data = request.data
        
        for item in self.REQUIRED_PARAMS:
            if item not in data:
                return HttpResponse("missing params: {}".format(item), status=400)
        
        print(data)
        return HttpResponse("It worked", status=202)