from django.urls import path
from . import views
from .whatsapp_bot import whatsapp_webhook

app_name = 'ventas'

urlpatterns = [
    path('', views.index, name='index'),
    path('carrito/', views.carrito, name='carrito'),
    path('buscar/', views.buscar, name='buscar'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('perfil/cambiar-password/', views.cambiar_password_view, name='cambiar_password'),
    path('detalle/<str:categoria>/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('belleza/', views.categoria_belleza, name='belleza'),
    path('tecnologia/', views.categoria_tecnologia, name='tecnologia'),
    path('electrodomesticos/', views.categoria_electrodomesticos, name='electrodomesticos'),
    path('ferreteria/', views.categoria_ferreteria, name='ferreteria'),
    path('bebe/', views.categoria_bebe, name='bebe'),
    path('aire-libre/', views.categoria_aire_libre, name='aire_libre'),
    path('entretenimiento/', views.categoria_entretenimiento, name='entretenimiento'),
    path('salud/', views.categoria_salud, name='salud'),
    # WhatsApp Webhook
    path('webhook/whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
]
