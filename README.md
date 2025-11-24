# Superventas
Tienda de ventas de productos en línea con sistema de gestión de inventario, pagos integrados y chatbot con inteligencia artificial.

## 🚀 Características

- ✅ **Sistema de inventario**: Control de stock automático
- ✅ **Pagos integrados**: Stripe, MercadoPago, Google Pay
- ✅ **Chatbot con IA**: Respuestas inteligentes 24/7 (Groq - Gratis)
- ✅ **WhatsApp Bot**: Integración con Twilio
- ✅ **Panel de administración**: Gestión completa de productos y pedidos
- ✅ **Sistema de usuarios**: Perfiles, favoritos y pedidos
- ✅ **Responsive**: Optimizado para móviles y escritorio

## 📚 Documentación

- [Configurar Chatbot con IA (Gratis)](CONFIGURAR_CHATBOT_IA.md)
- [Configurar WhatsApp Bot](WHATSAPP_SETUP_FINAL.md)
- [Configurar Pagos](README_PAGOS.md)
- [Panel de Administración](PANEL_ADMIN.md)

## 🛠️ Instalación rápida

```bash
# Clonar repositorio
git clone https://github.com/tavo1089/Superventas.git
cd Superventas

# Crear entorno virtual
python -m venv entorno_virtual
entorno_virtual\Scripts\activate  # Windows
source entorno_virtual/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Copia .env.example a .env y configura tus claves

# Migrar base de datos
python manage.py migrate

# Importar productos de ejemplo
python manage.py importar_productos

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## 🤖 Chatbot con IA

El chatbot usa **Groq** (gratuito) para responder preguntas automáticamente:
- Información de productos
- Recomendaciones personalizadas
- Dudas sobre envíos y pagos
- Soporte 24/7

Ver: [CONFIGURAR_CHATBOT_IA.md](CONFIGURAR_CHATBOT_IA.md)

## 📦 Requisitos

- Python 3.8+
- Django 5.2.8
- SQLite (incluido)
- Cuenta Groq (gratis) para chatbot IA

## 📄 Licencia

Proyecto personal para fines educativos.

