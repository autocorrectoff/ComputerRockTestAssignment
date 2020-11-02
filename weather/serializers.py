from rest_framework import serializers
from .models import Weather
import json

class WeatherSerializer(serializers.ModelSerializer):
    wind = serializers.SerializerMethodField(source='wind', read_only=True)

    def get_wind(self, instance):
        return json.loads(instance.wind)

    class Meta:
        model = Weather
        fields = ('description', 'temperature', 'visibility', 'wind', 'last_update')