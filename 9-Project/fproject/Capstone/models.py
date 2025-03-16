from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def directorio_usuario(instance, filename):
    return f"files/{instance.user.id}/{filename}"


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="capstone_user_groups",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="capstone_user_permissions",  
        blank=True
    )

class Event(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allDay = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=75)
    file = models.FileField(upload_to=directorio_usuario)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    
