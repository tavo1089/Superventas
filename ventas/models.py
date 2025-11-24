from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Producto(models.Model):
    """Modelo para gestionar el inventario y stock de productos"""
    producto_id = models.IntegerField(unique=True, help_text='ID del producto en la API externa')
    nombre = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0, help_text='Porcentaje de descuento')
    
    # Control de stock
    stock = models.IntegerField(default=0, help_text='Cantidad disponible en inventario')
    stock_minimo = models.IntegerField(default=5, help_text='Alerta cuando el stock sea menor a este valor')
    
    # Información adicional
    imagen_url = models.URLField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True, help_text='Desactivar producto sin eliminarlo')
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.nombre} (Stock: {self.stock})'
    
    @property
    def precio_con_descuento(self):
        """Calcula el precio final con descuento aplicado"""
        if self.descuento > 0:
            return self.precio * (1 - self.descuento / 100)
        return self.precio
    
    @property
    def stock_bajo(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock <= self.stock_minimo
    
    @property
    def sin_stock(self):
        """Verifica si no hay stock disponible"""
        return self.stock <= 0
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']


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


class Pedido(models.Model):
    """Modelo para gestionar los pedidos de los usuarios"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Pago Contra Entrega'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    numero_pedido = models.CharField(max_length=50, unique=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Información de pago
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='efectivo')
    estado_pago = models.BooleanField(default=False)  # False = pendiente, True = pagado
    
    # Información de envío
    direccion_envio = models.TextField()
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=20)
    
    # Notas adicionales
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'Pedido {self.numero_pedido} - {self.user.username}'
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']


class DetallePedido(models.Model):
    """Modelo para los items individuales de cada pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto_id = models.IntegerField()
    producto_nombre = models.CharField(max_length=255)
    producto_imagen = models.URLField()
    producto_categoria = models.CharField(max_length=100)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.IntegerField(default=0)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.producto_nombre} x{self.cantidad} - Pedido {self.pedido.numero_pedido}'
    
    class Meta:
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedidos'
