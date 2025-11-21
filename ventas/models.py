from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True, default='perfiles/default.jpg')
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, blank=True, default='Perú')
    codigo_postal = models.CharField(max_length=10, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

# Crear perfil automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
