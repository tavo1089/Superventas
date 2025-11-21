# 📱 WhatsApp Bot - Instalación Rápida

## ⚡ Instalación Express (5 minutos)

### 1. Instalar paquetes necesarios
```bash
.\entorno_virtual\Scripts\activate
pip install twilio django-environ
```

### 2. Crear cuenta Twilio GRATIS
- Ve a: https://www.twilio.com/try-twilio
- Regístrate (incluye $15 de crédito)
- Activa el WhatsApp Sandbox

### 3. Configurar .env
```bash
# Copia el archivo de ejemplo
copy .env.example .env

# Edita .env con tus credenciales de Twilio
```

### 4. Instalar ngrok (para pruebas locales)
- Descarga: https://ngrok.com/download
- Ejecuta: `ngrok http 8000`
- Copia la URL https que te da

### 5. Configurar webhook en Twilio
- Ve a: https://console.twilio.com/
- Pega tu URL de ngrok: `https://tu-url.ngrok.io/webhook/whatsapp/`

### 6. ¡Listo! Pruébalo
```bash
# Inicia el servidor
python manage.py runserver

# Envía "hola" desde WhatsApp al número del sandbox
```

## 📖 Documentación Completa
Lee `SETUP_WHATSAPP.md` para instrucciones detalladas.

## 🤖 Comandos del Bot

| Mensaje | Respuesta |
|---------|-----------|
| `hola` | Menú principal |
| `1` | Ver catálogo completo |
| `2` | Buscar producto |
| `3` | Estado de pedido |
| `4` | Contactar soporte |
| `5` | Ver horarios |

## 💡 Características

✅ Menú interactivo
✅ Búsqueda de productos
✅ Consulta de pedidos
✅ Información de envíos
✅ Soporte 24/7
✅ Notificaciones automáticas

## 🚀 Para Producción

Cuando estés listo:
1. Obtén un número WhatsApp Business ($1/mes en Twilio)
2. Despliega en un servidor real (no ngrok)
3. Actualiza el webhook con tu dominio

## 💰 Costos

- **Pruebas (Sandbox):** GRATIS
- **Producción Twilio:** $1/mes + $0.005 por mensaje
- **WhatsApp Business API:** Desde $50/mes

## ❓ ¿Necesitas ayuda?

Lee la documentación completa en:
- `WHATSAPP_INTEGRATION.md` - Guía técnica completa
- `SETUP_WHATSAPP.md` - Paso a paso detallado
