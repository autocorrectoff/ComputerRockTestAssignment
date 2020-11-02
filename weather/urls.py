from django.urls import path

from . import views

urlpatterns = [
  path('<str:call_sign>/weather', views.weather)
]