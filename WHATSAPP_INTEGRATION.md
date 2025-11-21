# 🤖 Integración WhatsApp Chatbot - Superventas

## Opción 1: Twilio WhatsApp (Recomendada)

### Paso 1: Crear cuenta en Twilio
1. Ir a https://www.twilio.com/
2. Registrarse (gratis con crédito de prueba)
3. Verificar número de teléfono

### Paso 2: Configurar WhatsApp Sandbox (Pruebas)
1. En el dashboard de Twilio, ir a "Messaging" > "Try it out" > "Send a WhatsApp message"
2. Escanear código QR o enviar mensaje de activación desde tu WhatsApp
3. Copiar:
   - Account SID
   - Auth Token
   - WhatsApp número (ej: whatsapp:+14155238886)

### Paso 3: Instalar dependencias

```bash
pip install twilio django-environ
```

### Paso 4: Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### Paso 5: Crear vista para webhook de WhatsApp

Archivo: `ventas/whatsapp_bot.py`

```python
from twilio.twiml.messaging_response import MessagingResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from ventas.models import Perfil


@csrf_exempt
def whatsapp_webhook(request):
    """Maneja mensajes entrantes de WhatsApp"""
    if request.method == 'POST':
        incoming_msg = request.POST.get('Body', '').strip().lower()
        from_number = request.POST.get('From', '')
        
        response = MessagingResponse()
        message = response.message()
        
        # Lógica del chatbot
        if incoming_msg in ['hola', 'hi', 'hello', 'ola']:
            reply = """
🛒 *¡Bienvenido a Superventas!*

¿En qué puedo ayudarte?

1️⃣ Ver catálogo
2️⃣ Buscar producto
3️⃣ Estado de pedido
4️⃣ Soporte
5️⃣ Horarios

Escribe el número de la opción 👆
            """
        
        elif incoming_msg == '1':
            reply = """
📦 *Nuestras categorías:*

🌸 Belleza y Cuidado
💻 Tecnología
🏠 Electrodomésticos
🔧 Ferretería
👶 Bebé y Niños
🏕️ Aire Libre
🎮 Entretenimiento
💪 Salud y Bienestar

Responde con el nombre de la categoría o visita:
👉 https://superventas.com
            """
        
        elif incoming_msg == '2':
            reply = "🔍 Escribe el nombre del producto que buscas:"
        
        elif incoming_msg == '3':
            reply = """
📦 *Estado de Pedido*

Por favor, envíanos tu número de pedido.

Formato: #12345
            """
        
        elif incoming_msg == '4':
            reply = """
🆘 *Soporte al Cliente*

📞 Tel: +51 999 999 999
📧 Email: soporte@superventas.com
⏰ Lun-Vie: 9AM - 6PM

¿Cuál es tu consulta?
            """
        
        elif incoming_msg == '5':
            reply = """
⏰ *Horarios de Atención*

🏪 Tienda Física:
Lunes a Viernes: 9:00 AM - 8:00 PM
Sábados: 9:00 AM - 6:00 PM
Domingos: 10:00 AM - 2:00 PM

🚚 Entregas:
Lunes a Sábado: 9:00 AM - 6:00 PM

💬 Chat: 24/7
            """
        
        elif 'precio' in incoming_msg or 'costo' in incoming_msg:
            reply = "💰 Para ver precios actualizados, visita nuestro catálogo:\n👉 https://superventas.com/catalogo"
        
        else:
            # Búsqueda de producto básica
            reply = f"""
Buscando "{incoming_msg}"... 🔍

Para ver todos nuestros productos, visita:
👉 https://superventas.com

O escribe *MENU* para ver opciones.
            """
        
        message.body(reply)
        return HttpResponse(str(response), content_type='application/xml')
    
    return HttpResponse('OK', status=200)


def send_whatsapp_notification(to_number, message):
    """Envía notificación de WhatsApp"""
    from twilio.rest import Client
    from django.conf import settings
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        return message.sid
    except Exception as e:
        print(f"Error enviando WhatsApp: {e}")
        return None
```

### Paso 6: Agregar URL

En `ventas/urls.py`:

```python
from ventas.whatsapp_bot import whatsapp_webhook

urlpatterns = [
    # ... otras URLs
    path('webhook/whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
]
```

### Paso 7: Configurar Webhook en Twilio

1. Ir a Twilio Console > WhatsApp Sandbox Settings
2. En "WHEN A MESSAGE COMES IN", poner:
   ```
   https://tu-dominio.com/webhook/whatsapp/
   ```
3. Para desarrollo local, usar **ngrok**:
   ```bash
   ngrok http 8000
   ```
   Copiar la URL https de ngrok

### Paso 8: Actualizar settings.py

```python
import environ

env = environ.Env()
environ.Env.read_env()

TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN', default='')
TWILIO_WHATSAPP_NUMBER = env('TWILIO_WHATSAPP_NUMBER', default='')
```

## Opción 2: WhatsApp Business API (Producción)

Para cuenta verificada con check verde:

1. **Meta Business Suite**
   - Ir a https://business.facebook.com/
   - Crear cuenta de negocio
   - Solicitar WhatsApp Business API

2. **Proveedor recomendado: 360Dialog**
   - Más económico
   - Fácil integración
   - Buena documentación en español

3. **Costos aproximados:**
   - Conversaciones de servicio: $0.005-0.01/msg
   - Conversaciones de marketing: $0.03-0.05/msg
   - Verificación: ~$50-100 (una vez)

## Opción 3: Solución No Oficial (Gratis pero con riesgos)

### Usando whatsapp-web.py

```bash
pip install whatsapp-web.py
```

⚠️ **ADVERTENCIA**: Puede resultar en bloqueo de cuenta.

## 🎯 Funcionalidades Recomendadas

1. ✅ **Menú interactivo**
2. ✅ **Búsqueda de productos**
3. ✅ **Estado de pedidos**
4. ✅ **Notificaciones automáticas**:
   - Confirmación de pedido
   - Estado de envío
   - Recordatorios de carrito abandonado
5. ✅ **Soporte 24/7**
6. ✅ **Catálogo de productos**

## 📊 Mensajes Automáticos Útiles

### Confirmación de pedido
```python
def enviar_confirmacion_pedido(pedido):
    mensaje = f"""
✅ *Pedido Confirmado* #{pedido.id}

📦 Productos: {pedido.cantidad_items}
💰 Total: S/ {pedido.total}
🚚 Entrega estimada: {pedido.fecha_entrega}

Rastrea tu pedido:
👉 https://superventas.com/pedidos/{pedido.id}

¡Gracias por tu compra! 🎉
    """
    send_whatsapp_notification(pedido.usuario.telefono, mensaje)
```

### Carrito abandonado
```python
def recordatorio_carrito():
    mensaje = """
🛒 ¡Tienes productos en tu carrito!

No olvides completar tu compra.
Tus productos te están esperando 😊

Ver carrito:
👉 https://superventas.com/carrito

¿Necesitas ayuda? Responde a este mensaje.
    """
    send_whatsapp_notification(usuario.telefono, mensaje)
```

## 🚀 Próximos Pasos

1. **Fase 1**: Twilio Sandbox (gratis, para pruebas)
2. **Fase 2**: Twilio producción (cuando tengas clientes)
3. **Fase 3**: WhatsApp Business API oficial (para escalar)

## 💡 Tips

- Usa botones interactivos cuando sea posible
- Mantén respuestas cortas y claras
- Incluye emojis para mejor UX
- Siempre ofrece opción de hablar con humano
- Registra conversaciones para mejorar el bot

## 🔗 Recursos

- Twilio Docs: https://www.twilio.com/docs/whatsapp
- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp
- 360Dialog: https://www.360dialog.com/
