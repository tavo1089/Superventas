from django.contrib import admin
from .models import Perfil, Favorito

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'ciudad', 'pais']
    search_fields = ['user__username', 'user__email', 'telefono', 'ciudad']
    list_filter = ['pais', 'ciudad']

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['user', 'producto_nombre', 'producto_categoria', 'producto_precio', 'fecha_agregado']
    search_fields = ['user__username', 'producto_nombre', 'producto_categoria']
    list_filter = ['producto_categoria', 'fecha_agregado']
    readonly_fields = ['fecha_agregado']
