from django.urls import path
from . import views
from .whatsapp_bot import whatsapp_webhook
from .chatbot_ai import chatbot_respuesta

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
    # Favoritos
    path('favoritos/', views.lista_favoritos, name='favoritos'),
    path('agregar-favorito/', views.agregar_favorito, name='agregar_favorito'),
    path('quitar-favorito/', views.quitar_favorito, name='quitar_favorito'),
    # Pedidos
    path('checkout/', views.checkout, name='checkout'),
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('cancelar-pedido/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
    # Mercado Pago
    path('crear-preferencia-mp/', views.crear_preferencia_mercadopago, name='crear_preferencia_mp'),
    path('test-mp-config/', views.test_mercadopago_config, name='test_mp_config'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago-pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('webhook/mercadopago/', views.webhook_mercadopago, name='webhook_mercadopago'),
    # Stripe
    path('crear-checkout-stripe/', views.crear_checkout_stripe, name='crear_checkout_stripe'),
    path('pago-exitoso-stripe/', views.pago_exitoso_stripe, name='pago_exitoso_stripe'),
    path('test-stripe-config/', views.test_stripe_config, name='test_stripe_config'),
    # WhatsApp Webhook
    path('webhook/whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
    # Chatbot AI
    path('chatbot/respuesta/', chatbot_respuesta, name='chatbot_respuesta'),
]
