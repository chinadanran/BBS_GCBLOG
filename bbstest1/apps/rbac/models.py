from django.db import models
# Create your models here.

class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField("Permission")

    def __str__(self):
        return self.title


class Permission(models.Model):
    url=models.CharField(max_length=128)
    title = models.CharField(max_length=32)
    code=models.CharField(max_length=32,default="list")
    def __str__(self):
        return self.title

