from django.db import models


class User(models.Model):
    name = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    creation_date = models.DateTimeField(auto_now_add=True)
