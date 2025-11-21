# 🚀 Guía Rápida de Instalación - WhatsApp Bot

## Paso 1: Instalar dependencias

```bash
.\entorno_virtual\Scripts\activate
pip install twilio django-environ
```

## Paso 2: Crear cuenta Twilio

1. Ve a https://www.twilio.com/try-twilio
2. Regístrate gratis (incluye $15 de crédito)
3. Verifica tu email y número de teléfono

## Paso 3: Configurar WhatsApp Sandbox

1. En Twilio Console: https://console.twilio.com/
2. Ve a "Messaging" > "Try it out" > "Send a WhatsApp message"
3. Copia el código de activación (ej: "join abc-xyz")
4. Desde tu WhatsApp, envía ese código a +1 415 523 8886
5. Recibirás confirmación: "Twilio Sandbox: ✅ You are all set!"

## Paso 4: Obtener credenciales

En https://console.twilio.com/:
- **Account SID**: ACxxxxxxxxxx (en el Dashboard)
- **Auth Token**: Click en "Show" para verlo
- **WhatsApp Number**: whatsapp:+14155238886 (del sandbox)

## Paso 5: Configurar variables de entorno

Copia `.env.example` a `.env`:

```bash
copy .env.example .env
```

Edita `.env` con tus credenciales reales:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_token_secreto
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Paso 6: Actualizar settings.py

Ya está configurado, pero verifica que tenga:

```python
import environ

env = environ.Env()
environ.Env.read_env()

TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN', default='')
TWILIO_WHATSAPP_NUMBER = env('TWILIO_WHATSAPP_NUMBER', default='')
```

## Paso 7: Exponer servidor localmente con ngrok

### Instalar ngrok:

**Windows:**
1. Descargar de https://ngrok.com/download
2. Extraer ngrok.exe
3. Registrarse en ngrok.com para obtener authtoken
4. Abrir PowerShell en la carpeta de ngrok:

```bash
.\ngrok.exe authtoken TU_AUTH_TOKEN
.\ngrok.exe http 8000
```

Obtendrás una URL como: `https://abc123.ngrok.io`

## Paso 8: Configurar Webhook en Twilio

1. Ve a: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox
2. En **"WHEN A MESSAGE COMES IN"**, poner:
   ```
   https://abc123.ngrok.io/webhook/whatsapp/
   ```
3. Método: **POST**
4. Click "Save"

## Paso 9: Iniciar servidor Django

En otra terminal:

```bash
.\entorno_virtual\Scripts\activate
python manage.py runserver
```

## Paso 10: ¡Probar!

Desde tu WhatsApp, envía al número del sandbox:

- `hola` - Ver menú principal
- `1` - Ver catálogo
- `2` - Buscar producto
- `3` - Estado de pedido
- `soporte` - Contactar soporte

## 🎯 Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| hola, menu | Menú principal |
| 1 | Ver catálogo |
| 2 | Buscar producto |
| 3 | Rastrear pedido |
| 4 | Soporte |
| 5 | Horarios |
| 6 | Ubicación |
| soporte | Contacto directo |

## 🔧 Troubleshooting

### Error: "Twilio credentials not configured"
- Verifica que `.env` existe y tiene las credenciales correctas
- Reinicia el servidor Django

### Error: "Webhook timeout"
- Verifica que ngrok está corriendo
- Verifica que el servidor Django está corriendo
- Confirma la URL del webhook en Twilio

### No recibo respuestas
- Verifica que enviaste el mensaje de activación al sandbox
- Revisa la consola de Django por errores
- Verifica los logs en Twilio Console

## 📱 Para Producción

Cuando estés listo para producción:

1. **Obtener número WhatsApp Business propio:**
   - Solicitar en Twilio: $1/mes
   - O usar WhatsApp Business API oficial

2. **Usar dominio real:**
   - Desplegar en Heroku, Railway, o servidor propio
   - Configurar webhook con tu dominio

3. **Verificación de negocio:**
   - Para check verde oficial
   - Proceso toma 1-2 semanas

## 💰 Costos

### Twilio (Sandbox - Pruebas):
- ✅ GRATIS con $15 de crédito
- Limitado a números que se unieron al sandbox

### Twilio (Producción):
- Número: $1/mes
- Mensajes entrantes: GRATIS
- Mensajes salientes: $0.005 c/u

### WhatsApp Business API:
- Setup: ~$50-100
- Conversaciones: $0.005-0.05 c/u

## 🎓 Recursos

- Docs Twilio WhatsApp: https://www.twilio.com/docs/whatsapp
- ngrok Docs: https://ngrok.com/docs
- Django Environ: https://django-environ.readthedocs.io/

## ✅ Checklist

- [ ] Cuenta Twilio creada
- [ ] WhatsApp sandbox activado
- [ ] Credenciales en `.env`
- [ ] `pip install twilio django-environ`
- [ ] ngrok instalado y corriendo
- [ ] Webhook configurado en Twilio
- [ ] Servidor Django corriendo
- [ ] Primer mensaje de prueba enviado

¡Listo! Tu chatbot de WhatsApp está funcionando 🎉
