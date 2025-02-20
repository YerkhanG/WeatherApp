from django.urls import path
from weatherapp.views import add_city, user_weather, register_user
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('add-city/', add_city, name='add_city_view'),
    path('user_weather/', user_weather, name='user_weather'),
    path('register_user/', register_user, name='register_user'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]