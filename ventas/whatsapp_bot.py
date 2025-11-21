from twilio.twiml.messaging_response import MessagingResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.conf import settings


@csrf_exempt
def whatsapp_webhook(request):
    """Maneja mensajes entrantes de WhatsApp"""
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').strip().lower()
        from_number = request.POST.get('From', '')
        sender_name = request.POST.get('ProfileName', 'Cliente')
        
        response = MessagingResponse()
        message = response.message()
        
        # Lógica del chatbot
        if incoming_msg in ['hola', 'hi', 'hello', 'menu', 'inicio']:
            reply = f"""
🛒 *¡Hola {sender_name}! Bienvenido a Superventas*

¿En qué puedo ayudarte hoy?

*1* 📦 Ver catálogo
*2* 🔍 Buscar producto
*3* 📋 Estado de pedido
*4* 🆘 Soporte
*5* ⏰ Horarios de atención
*6* 📍 Ubicación

_Responde con el número de la opción_
            """
        
        elif incoming_msg == '1':
            reply = """
📦 *Nuestras Categorías:*

🌸 *Belleza* - Cuidado personal
💻 *Tecnología* - Últimas novedades
🏠 *Electrodomésticos* - Para tu hogar
🔧 *Ferretería* - Herramientas
👶 *Bebé* - Productos infantiles
🏕️ *Aire Libre* - Aventura
🎮 *Entretenimiento* - Diversión
💪 *Salud* - Bienestar

👉 Ver todos: http://127.0.0.1:8000/

Escribe *MENU* para volver al inicio
            """
        
        elif incoming_msg == '2':
            reply = """
🔍 *Búsqueda de Productos*

Escríbeme el nombre del producto que buscas.
Por ejemplo:
• _smartphone_
• _licuadora_
• _taladro_

O visita nuestro buscador:
👉 http://127.0.0.1:8000/buscar/
            """
        
        elif incoming_msg == '3':
            reply = """
📦 *Rastrear Pedido*

Para conocer el estado de tu pedido, necesito tu número de orden.

Escríbelo en este formato:
📝 *#12345*

¿No tienes tu número? Ingresa aquí:
👉 http://127.0.0.1:8000/perfil/
            """
        
        elif incoming_msg == '4':
            reply = """
🆘 *Soporte al Cliente*

Estamos aquí para ayudarte:

📞 Teléfono: +51 999 999 999
📧 Email: soporte@superventas.com
💬 Chat web: http://127.0.0.1:8000/

⏰ *Horario de atención:*
Lun-Vie: 9:00 AM - 6:00 PM
Sáb: 9:00 AM - 2:00 PM

¿Cuál es tu consulta? Escríbela aquí 👇
            """
        
        elif incoming_msg == '5':
            reply = """
⏰ *Horarios de Atención*

🏪 *Tienda Física:*
📅 Lun-Vie: 9:00 AM - 8:00 PM
📅 Sábados: 9:00 AM - 6:00 PM
📅 Domingos: 10:00 AM - 2:00 PM

🚚 *Entregas a Domicilio:*
📅 Lun-Sáb: 9:00 AM - 6:00 PM

💬 *WhatsApp:* 24/7 (respuesta automática)
🤝 *Atención personalizada:* Lun-Vie 9AM-6PM
            """
        
        elif incoming_msg == '6':
            reply = """
📍 *Nuestra Ubicación*

🏪 *Tienda Principal:*
Av. Ejemplo 123, Lima
San Isidro, Perú

🚗 Estacionamiento disponible
🚇 Metro: Estación San Isidro
🚌 Buses: 301, 302, 405

📱 Ver en mapa:
[Proximamente Google Maps]

¿Necesitas direcciones? Responde *SI*
            """
        
        elif incoming_msg.startswith('#'):
            # Número de pedido
            pedido_num = incoming_msg[1:]
            reply = f"""
🔍 *Buscando pedido #{pedido_num}...*

Para ver el detalle completo de tu pedido:
👉 http://127.0.0.1:8000/perfil/

Si tienes problemas, contacta a soporte:
📞 +51 999 999 999

Escribe *MENU* para volver al inicio
            """
        
        elif 'precio' in incoming_msg or 'costo' in incoming_msg or 'cuanto' in incoming_msg:
            reply = """
💰 *Consulta de Precios*

Para ver precios actualizados y ofertas:
👉 http://127.0.0.1:8000/

🎁 *Ofertas especiales disponibles*
🚚 *Envío gratis* en compras +S/100

Escribe el nombre del producto para ayudarte mejor.
            """
        
        elif 'envio' in incoming_msg or 'delivery' in incoming_msg or 'entrega' in incoming_msg:
            reply = """
🚚 *Información de Envíos*

📦 *Envío estándar:* S/10 (3-5 días)
⚡ *Envío express:* S/20 (1-2 días)
🎁 *Envío GRATIS:* Compras +S/100

📍 *Cobertura:* Lima y Callao

🕐 *Horarios de entrega:*
Lun-Sáb: 9:00 AM - 6:00 PM

Escribe *MENU* para más opciones
            """
        
        elif 'pago' in incoming_msg or 'pagar' in incoming_msg:
            reply = """
💳 *Métodos de Pago*

Aceptamos:
✅ Tarjetas Visa/Mastercard
✅ Yape / Plin
✅ Transferencia bancaria
✅ Efectivo contra entrega

🔒 *Pago seguro 100%*

Para realizar tu compra:
👉 http://127.0.0.1:8000/

Escribe *MENU* para volver al inicio
            """
        
        elif 'gracias' in incoming_msg or 'thank' in incoming_msg:
            reply = """
😊 *¡De nada!*

Fue un placer ayudarte.

¿Necesitas algo más?
Escribe *MENU* para ver opciones.

🛒 Visita nuestra tienda:
👉 http://127.0.0.1:8000/
            """
        
        else:
            # Búsqueda de producto
            reply = f"""
🔍 Buscando *"{incoming_msg}"*...

Para ver resultados y disponibilidad:
👉 http://127.0.0.1:8000/buscar/?q={incoming_msg}

O escribe *MENU* para ver todas las opciones.

_¿Te gustaría hablar con un asesor?_
Responde *SOPORTE* para contacto directo.
            """
        
        message.body(reply)
        return HttpResponse(str(response), content_type='application/xml')
    
    return HttpResponse('Método no permitido', status=405)


def send_whatsapp_notification(to_number, message_text):
    """
    Envía una notificación de WhatsApp a un número
    
    Args:
        to_number: Número de teléfono (ej: '+51999999999')
        message_text: Texto del mensaje
    
    Returns:
        message.sid si exitoso, None si falla
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message_text,
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        
        return message.sid
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")
        return None


def enviar_confirmacion_pedido(pedido, usuario):
    """Envía confirmación de pedido por WhatsApp"""
    mensaje = f"""
✅ *¡Pedido Confirmado!* 

🛍️ *Pedido #{pedido.get('id', 'N/A')}*

👤 Cliente: {usuario.get_full_name() or usuario.username}
📦 Productos: {pedido.get('items', 0)} artículos
💰 Total: S/ {pedido.get('total', 0):.2f}

🚚 *Entrega estimada:*
{pedido.get('fecha_entrega', '3-5 días hábiles')}

📱 Rastrea tu pedido aquí:
👉 http://127.0.0.1:8000/perfil/

¿Dudas? Responde a este mensaje.

¡Gracias por tu compra! 🎉
_Equipo Superventas_
    """
    
    telefono = getattr(usuario.perfil, 'telefono', None)
    if telefono:
        return send_whatsapp_notification(telefono, mensaje)
    return None


def enviar_recordatorio_carrito(usuario, productos):
    """Envía recordatorio de carrito abandonado"""
    mensaje = f"""
🛒 *¡Hola {usuario.first_name or usuario.username}!*

Tienes *{len(productos)} producto(s)* esperándote en tu carrito 🎁

No pierdas estas ofertas:
{chr(10).join([f"• {p.get('nombre', 'Producto')}" for p in productos[:3]])}

✨ *¡Completa tu compra ahora!*
👉 http://127.0.0.1:8000/carrito/

¿Necesitas ayuda? Responde a este mensaje.

_Equipo Superventas_
    """
    
    telefono = getattr(usuario.perfil, 'telefono', None)
    if telefono:
        return send_whatsapp_notification(telefono, mensaje)
    return None


def enviar_actualizacion_envio(pedido, estado):
    """Envía actualización de estado de envío"""
    estados_emoji = {
        'procesando': '📦',
        'enviado': '🚚',
        'en_camino': '🛣️',
        'entregado': '✅'
    }
    
    emoji = estados_emoji.get(estado, '📦')
    
    mensaje = f"""
{emoji} *Actualización de Pedido*

🛍️ *Pedido #{pedido.get('id', 'N/A')}*

📍 *Estado:* {estado.upper().replace('_', ' ')}

{pedido.get('mensaje_adicional', '')}

📱 Ver detalles:
👉 http://127.0.0.1:8000/perfil/

_Equipo Superventas_
    """
    
    telefono = pedido.get('telefono_cliente')
    if telefono:
        return send_whatsapp_notification(telefono, mensaje)
    return None
