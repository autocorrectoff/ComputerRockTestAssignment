from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Weather
from .serializers import WeatherSerializer

@api_view(['GET'])
def weather(request, call_sign):
    weather_info = Weather.objects.order_by('-last_update').first()
    serializer = WeatherSerializer(weather_info, many=False)
    return Response(serializer.data)