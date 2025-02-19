from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
import requests
from django.views.decorators.csrf import csrf_exempt
from geopy import Nominatim
from Jobtech import settings
from weatherapp.models import Weather, Profile


def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None, None


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        city = request.POST.get('city')

        if not all([username, password, city]):
            return JsonResponse({
                'error': 'Необходимо указать username, password и city'
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'error': 'Пользователь с таким именем уже существует'
            }, status=400)

        # Create user and set their city
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.get(user=user)
        profile.city = city
        profile.save()

        return JsonResponse({
            'message': 'Пользователь успешно зарегистрирован',
            'username': username,
            'city': city
        })

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

def is_manager(user):
    return user.groups.filter(name='Managers').exists()


@login_required
def user_weather(request):
    profile = get_object_or_404(Profile, user=request.user)
    if not profile.city:
        return JsonResponse({'error': 'Город не указан в профиле пользователя.'}, status=400)

    weather_data = fetch_weather_data(profile.city)
    return JsonResponse(weather_data)


def fetch_weather_data(city):
    longitude, latitude = get_city_coordinates(city)

    try:
        weather_obj = Weather.objects.get(city=city)
    except Weather.DoesNotExist:
        weather_obj = None

    ten_minutes_ago = timezone.now() - timedelta(minutes=10)

    if weather_obj and weather_obj.last_updated > ten_minutes_ago:
        data = {
            'city': weather_obj.city,
            'air_temperature': weather_obj.air_temperature,
            'humidity': weather_obj.humidity,
            'visibility': weather_obj.visibility,
            'last_updated': weather_obj.last_updated.isoformat(),
        }
        return data
    else:
        api_key = settings.API_KEY
        api_url = 'https://api.stormglass.io/v2/weather/point'
        params = {
            "lat": latitude,
            "lng": longitude,
            "params": ','.join(['humidity', 'airTemperature', 'visibility'])
        }
        response = requests.get(api_url, params=params, headers={"Authorization": api_key})
        if response.status_code != 200:
            return {'error': 'Ошибка получения данных от внешнего API.'}

        weather_data = response.json()
        try:
            first_interval = weather_data["hours"][0]
            air_temperature = first_interval["airTemperature"]["sg"]
            humidity = first_interval["humidity"]["sg"]
            visibility = first_interval["visibility"]["sg"]
        except (KeyError, IndexError):
            return {'error': 'Ошибка обработки данных от API.'}
        if weather_obj:
            weather_obj.air_temperature = air_temperature
            weather_obj.humidity = humidity
            weather_obj.visibility = visibility
            weather_obj.save()
        else:
            weather_obj = Weather.objects.create(
                city=city,
                air_temperature=air_temperature,
                humidity=humidity,
                visibility=visibility,
            )
        data = {
            'city': weather_obj.city,
            'air_temperature': weather_obj.air_temperature,
            'humidity': weather_obj.humidity,
            'visibility': weather_obj.visibility,
            'last_updated': weather_obj.last_updated.isoformat(),
        }
        return data



@user_passes_test(is_manager)
def add_city_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            if Weather.objects.filter(city=city).exists():
                messages.error(request, 'Город уже существует.')
            else:
                Weather.objects.create(city=city)
                messages.success(request, f'Город {city} успешно добавлен.')
        return redirect('add_city_view')
    return render(request, 'add_city.html')
