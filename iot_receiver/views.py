from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.

class IoTProtoReceiever(APIView):
    
    def post(self, request):
        data = request.data
        
        ####
        
        return JsonResponse({
            "status": True
        }, status=202)