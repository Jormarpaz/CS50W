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

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=75)
    description = models.TextField()
    file = models.FileField(upload_to=directorio_usuario)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    questions = models.JSONField()  # Guardamos las preguntas en formato JSON
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test de {self.user.username} - {self.file.name}"
