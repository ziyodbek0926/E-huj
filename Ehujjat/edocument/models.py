from django.db import models
from django.contrib.auth.models import User

class Tashkilot(models.Model):
    nomi = models.CharField(max_length=255)

    def __str__(self):
        return self.nomi

class UserP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete argumentini qo'shish
    full_name = models.CharField(max_length=200)


class Table(models.Model):
    user = models.CharField(max_length=150, blank=True, null=True)
    tashkilot = models.ForeignKey(Tashkilot, on_delete=models.CASCADE)
    zayafka_vaqti = models.DateTimeField(auto_now_add=True)
    tekshirilgan_vaqti = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tashkilot.nomi} - {self.status} - {self.user}"


