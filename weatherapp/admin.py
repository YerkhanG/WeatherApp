from django.contrib import admin

from weatherapp.models import Profile, Weather

# Register your models here.
admin.site.register(Weather)
admin.site.register(Profile)