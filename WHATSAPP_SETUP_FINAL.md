# ✅ Chatbot WhatsApp - Activado y Listo

## Estado Actual

✅ **Código del chatbot**: Implementado y funcional  
✅ **Webhook**: Habilitado en `/webhook/whatsapp/`  
✅ **Configuración**: Personalizable en `ventas/bot_config.py`  
⏳ **Twilio**: Pendiente de configurar (requiere cuenta)

## Próximos Pasos para Activar Completamente

### Paso 1: Crear Cuenta en Twilio (GRATIS)

1. Ve a: https://www.twilio.com/try-twilio
2. Regístrate (incluye $15 USD de crédito gratuito)
3. Verifica tu email y número de teléfono

### Paso 2: Activar WhatsApp Sandbox

1. En Twilio Console: https://console.twilio.com/
2. Ve a: **Messaging** > **Try it out** > **Send a WhatsApp message**
3. Verás un código como: `join abc-xyz`
4. Desde tu WhatsApp personal, envía ese código al número: **+1 415 523 8886**
5. Recibirás: "✅ You are all set!"

### Paso 3: Obtener Credenciales

En https://console.twilio.com/:

- **Account SID**: ACxxxxxxxxxx (visible en el Dashboard)
- **Auth Token**: Click en "Show" para verlo
- **WhatsApp Number**: `whatsapp:+14155238886`

### Paso 4: Configurar Variables de Entorno

Crea el archivo `.env` en la raíz del proyecto con:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_token_secreto_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

**⚠️ IMPORTANTE**: Nunca subas este archivo a GitHub (ya está en `.gitignore`)

### Paso 5: Instalar ngrok (Para pruebas locales)

1. Descarga ngrok: https://ngrok.com/download
2. Descomprime y ejecuta:
   ```bash
   ngrok http 8000
   ```
3. Copia la URL que aparece (ej: `https://xxxx-xxxx.ngrok.io`)

### Paso 6: Configurar Webhook en Twilio

1. En Twilio Console, ve a: **Messaging** > **Settings** > **WhatsApp sandbox settings**
2. En "WHEN A MESSAGE COMES IN", pega:
   ```
   https://xxxx-xxxx.ngrok.io/webhook/whatsapp/
   ```
3. Guarda cambios

### Paso 7: ¡Probar!

Envía desde tu WhatsApp al número de Twilio:
- `hola` → Verás el menú principal
- `1` → Ver catálogo
- `2` → Buscar productos
- `3` → Estado de pedido
- `4` → Soporte
- `5` → Horarios
- `6` → Ubicación

## Personalizar Respuestas del Bot

Edita el archivo `ventas/bot_config.py`:

```python
# Cambia el nombre de tu negocio
NOMBRE_NEGOCIO = "Tu Tienda"

# Ajusta horarios
HORARIO_TIENDA_SEMANA = "Lun-Vie: 10:00 AM - 7:00 PM"

# Modifica métodos de pago
METODOS_PAGO = [
    "Visa/Mastercard",
    "Yape",
    "Transferencia"
]

# Y más...
```

Después de editar, reinicia el servidor:
```bash
python manage.py runserver
```

## Funcionalidades del Bot

🤖 **Menú interactivo** con 6 opciones principales  
📦 **Catálogo de productos** por categorías  
🔍 **Búsqueda de productos** por nombre  
📋 **Consulta de pedidos** por número de orden  
💬 **Soporte al cliente** con horarios  
🕐 **Información de horarios** de atención  
📍 **Ubicación** y métodos de envío  
💳 **Métodos de pago** disponibles  
🎁 **Promociones** activas  

## Funciones Avanzadas (Ya implementadas)

El bot incluye funciones para enviar notificaciones automáticas:

```python
# Enviar confirmación de pedido
enviar_confirmacion_pedido(
    numero_telefono="+51999999999",
    numero_pedido="ORD-12345",
    total=299.99,
    productos=[{'nombre': 'Laptop', 'cantidad': 1}]
)

# Notificar cambio en envío
enviar_actualizacion_envio(
    numero_telefono="+51999999999",
    numero_pedido="ORD-12345",
    estado="en_camino"
)

# Recordatorio de carrito abandonado
enviar_recordatorio_carrito(
    numero_telefono="+51999999999",
    productos_carrito=[{'nombre': 'Laptop'}, {'nombre': 'Mouse'}]
)
```

## Costos

- **Twilio Sandbox (Pruebas)**: GRATIS
- **Crédito inicial**: $15 USD gratis
- **Mensajes WhatsApp**: ~$0.005 por mensaje
- **ngrok**: Gratis para desarrollo

## Producción (Cuando estés listo)

1. Solicitar número WhatsApp Business oficial en Twilio
2. Obtener dominio propio (ej: superventas.com)
3. Configurar webhook con tu dominio
4. Actualizar `URL_TIENDA` en `bot_config.py`

## Documentación Completa

- `WHATSAPP_INTEGRATION.md` - Integración detallada
- `SETUP_WHATSAPP.md` - Guía paso a paso
- `INSTRUCCIONES_BOT_PERSONALIZAR.md` - Cómo personalizar

## ¿Necesitas Ayuda?

El bot está listo para funcionar. Solo falta:
1. Crear cuenta Twilio (5 minutos)
2. Configurar archivo `.env` (2 minutos)
3. Instalar ngrok (3 minutos)
4. ¡Listo para probar!

Total: ~10 minutos para tenerlo funcionando completamente.
