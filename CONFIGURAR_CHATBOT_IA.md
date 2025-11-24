# 🤖 Configurar Chatbot con IA (Gratis)

Tu chatbot ahora puede usar **inteligencia artificial gratuita** para responder preguntas de clientes automáticamente, similar a ChatGPT.

## ✅ ¿Qué hace el chatbot con IA?

- Responde preguntas sobre productos, precios y categorías
- Recomienda productos según necesidades del cliente
- Ayuda con dudas sobre envíos y pagos
- Funciona 24/7 automáticamente
- Si no sabe algo, sugiere contactar por WhatsApp

## 📋 Paso 1: Crear cuenta en Groq (100% Gratis)

1. Ve a: **https://console.groq.com/**
2. Haz clic en "Sign Up" (Registrarse)
3. Crea una cuenta con tu email (Gmail, etc.)
4. Verifica tu email

## 🔑 Paso 2: Obtener API Key

1. Una vez dentro de Groq Console
2. Ve a la sección **"API Keys"** en el menú lateral
3. Haz clic en **"Create API Key"**
4. Dale un nombre (ejemplo: "Superventas Chatbot")
5. Copia la API Key que se genera (empieza con `gsk_...`)

## ⚙️ Paso 3: Configurar en tu proyecto

1. Abre el archivo `.env` en VS Code
2. Busca la línea que dice `GROQ_API_KEY=`
3. Pega tu API Key después del `=`:

```
GROQ_API_KEY=gsk_tu_api_key_aqui
```

4. Guarda el archivo `.env`

## 🚀 Paso 4: Reiniciar el servidor

1. En la terminal donde corre Django, presiona **CTRL+C** para detenerlo
2. Vuelve a iniciar el servidor:

```bash
python manage.py runserver
```

## ✅ Paso 5: Probar el chatbot

1. Abre tu navegador en: http://127.0.0.1:8000/
2. Haz clic en el botón del chatbot (esquina inferior derecha)
3. Escribe cualquier pregunta, por ejemplo:
   - "¿Qué productos de belleza tienen?"
   - "¿Cuánto cuesta el smartphone?"
   - "¿Tienen descuentos activos?"
   - "¿Hacen envíos a domicilio?"

## 🎯 Cómo funciona

- El chatbot está conectado al modelo **Llama 3.1 70B** de Groq
- Es completamente gratis (sin límites para desarrollo)
- Respuestas en español, naturales y profesionales
- Si no tiene API Key, funciona con respuestas básicas

## 💡 Ventajas vs Twilio WhatsApp

| Característica | Chatbot Web con IA | WhatsApp Twilio |
|----------------|-------------------|-----------------|
| **Costo** | Gratis ilimitado | Sandbox gratis 72h |
| **Respuestas** | IA inteligente | Respuestas fijas |
| **Disponibilidad** | 24/7 siempre | Requiere ngrok corriendo |
| **Mensajes** | En la página | Solo WhatsApp |
| **Setup** | 5 minutos | Requiere configuración |

## 🔧 Personalizar el chatbot

Si quieres cambiar cómo responde el chatbot, edita el archivo:
`ventas/chatbot_ai.py`

En la variable `CONTEXTO_NEGOCIO` puedes:
- Agregar más información sobre productos
- Cambiar el tono de las respuestas
- Agregar políticas de devolución
- Incluir horarios de atención

## ⚠️ Importante

- **Nunca compartas** tu API Key públicamente
- El archivo `.env` está en `.gitignore` (no se sube a GitHub)
- La API Key es gratuita para desarrollo
- Groq tiene límites generosos para uso personal

## 🆘 Solución de problemas

### El chatbot no responde con IA
- Verifica que agregaste la API Key en `.env`
- Reinicia el servidor Django
- Revisa que instalaste `requests`: `pip install requests`

### Respuestas lentas
- Normal en primera consulta (carga el modelo)
- Groq es uno de los más rápidos del mercado

### Error de API Key
- Verifica que copiaste la key completa
- No debe tener espacios antes o después
- Debe empezar con `gsk_`

## 📞 Respaldo

Si el chatbot con IA falla, automáticamente muestra el botón de WhatsApp para que el cliente te contacte directamente a tu número personal: **+598 97403564**

---

**¡Disfruta tu chatbot inteligente gratis! 🎉**
