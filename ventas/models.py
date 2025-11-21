from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
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


class Favorito(models.Model):
    """Modelo para guardar los productos favoritos de cada usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    producto_id = models.IntegerField()
    producto_nombre = models.CharField(max_length=255)
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2)
    producto_descuento = models.IntegerField(default=0)
    producto_imagen = models.URLField()
    producto_categoria = models.CharField(max_length=100)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.producto_nombre}'
    
    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ['user', 'producto_id', 'producto_categoria']
        ordering = ['-fecha_agregado']
