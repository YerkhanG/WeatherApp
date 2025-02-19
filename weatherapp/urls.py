from django.urls import path
from weatherapp.views import add_city_view, user_weather

urlpatterns = [
    path('add-city-view/', add_city_view, name='add_city_view'),
    path('user_weather/', user_weather, name='user_weather'),
]