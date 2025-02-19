from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Weather(models.Model):
    city = models.CharField(max_length=100, unique=True, help_text="Название города")
    air_temperature = models.FloatField(null=True, blank=True, help_text="Температура воздуха в градусах Цельсия")
    humidity = models.FloatField(null=True, blank=True, help_text="Влажность в процентах")
    visibility = models.FloatField(null=True, blank=True, help_text="Видимость в километрах")
    last_updated = models.DateTimeField(auto_now=True, help_text="Время последнего обновления данных")
