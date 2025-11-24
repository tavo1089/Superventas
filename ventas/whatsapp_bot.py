from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse


@csrf_exempt
@require_POST
def whatsapp_webhook(request):
    """Webhook para manejar mensajes entrantes de WhatsApp"""
    
    # Obtener el mensaje del usuario
    mensaje = request.POST.get('Body', '').strip().lower()
    numero_usuario = request.POST.get('From', '')
    
    # Crear respuesta TwiML
    resp = MessagingResponse()
    msg = resp.message()
    
    # Procesar el mensaje
    if not mensaje:
        msg.body("👋 ¡Hola! Soy el asistente de Superventas.\n\nEscribe *menu* para ver las opciones disponibles.")
    
    elif 'menu' in mensaje or 'ayuda' in mensaje or 'help' in mensaje:
        respuesta = """
📱 *MENÚ PRINCIPAL - SUPERVENTAS*

Escribe el número o nombre de la categoría:

1️⃣ *Belleza* - Productos de belleza y cuidado personal
2️⃣ *Tecnología* - Smartphones, laptops y gadgets
3️⃣ *Electrodomésticos* - Para tu hogar
4️⃣ *Ferretería* - Herramientas y construcción
5️⃣ *Bebé* - Productos para bebé y niños
6️⃣ *Aire Libre* - Camping y deportes
7️⃣ *Entretenimiento* - Gaming y TV
8️⃣ *Salud* - Fitness y bienestar

También puedes escribir:
• *Ofertas* - Ver productos en descuento
• *Info* - Información de contacto
        """
        msg.body(respuesta.strip())
    
    elif 'belleza' in mensaje or mensaje == '1':
        respuesta = """
💄 *PRODUCTOS DE BELLEZA*

🌸 Crema Facial Hidratante
   $25.99 → $20.79 (20% OFF)

💅 Set de Maquillaje Profesional
   $89.99 → $76.49 (15% OFF)

✨ Perfume Elegance 100ml
   $65.00 → $48.75 (25% OFF)

🎀 Serum Anti-Edad
   $45.50 → $40.95 (10% OFF)

Para comprar visita: http://127.0.0.1:8000/belleza/
        """
        msg.body(respuesta.strip())
    
    elif 'tecnologia' in mensaje or 'tecnología' in mensaje or mensaje == '2':
        respuesta = """
💻 *PRODUCTOS DE TECNOLOGÍA*

📱 Smartphone Galaxy Pro
   $899.99 → $764.99 (15% OFF)

💾 Laptop Gaming RGB
   $1299.99 → $1039.99 (20% OFF)

🎧 Auriculares Bluetooth Premium
   $399.99 → $299.99 (25% OFF)

⌚ Smartwatch Ultra
   $399.99 → $279.99 (30% OFF)

Para comprar visita: http://127.0.0.1:8000/tecnologia/
        """
        msg.body(respuesta.strip())
    
    elif 'electrodomestico' in mensaje or mensaje == '3':
        respuesta = """
🔌 *ELECTRODOMÉSTICOS*

❄️ Refrigeradora Smart 500L
   $1499.99 → $1349.99 (10% OFF)

🧺 Lavadora Automática 18kg
   $899.99 → $764.99 (15% OFF)

☕ Cafetera Express
   $179.99 → $152.99 (15% OFF)

Para comprar visita: http://127.0.0.1:8000/electrodomesticos/
        """
        msg.body(respuesta.strip())
    
    elif 'ferreteria' in mensaje or 'ferretería' in mensaje or mensaje == '4':
        respuesta = """
🔧 *FERRETERÍA Y CONSTRUCCIÓN*

⚡ Taladro Inalámbrico 20V
   $149.99 → $119.99 (20% OFF)

🛠️ Set de Herramientas 120 Piezas
   $89.99 → $76.49 (15% OFF)

🪚 Sierra Circular Profesional
   $199.99 → $149.99 (25% OFF)

Para comprar visita: http://127.0.0.1:8000/ferreteria/
        """
        msg.body(respuesta.strip())
    
    elif 'bebe' in mensaje or 'bebé' in mensaje or 'niño' in mensaje or mensaje == '5':
        respuesta = """
👶 *BEBÉ Y NIÑOS*

🍼 Coche para Bebé Premium
   $349.99 → $279.99 (20% OFF)

🛏️ Cuna Convertible
   $299.99 → $254.99 (15% OFF)

📹 Monitor de Bebé con Cámara
   $129.99 → $97.49 (25% OFF)

Para comprar visita: http://127.0.0.1:8000/bebe/
        """
        msg.body(respuesta.strip())
    
    elif 'aire' in mensaje or mensaje == '6':
        respuesta = """
🌲 *AIRE LIBRE*

🚴 Bicicleta de Montaña Pro
   $599.99 → $479.99 (20% OFF)

⛺ Carpa Camping 6 Personas
   $249.99 → $212.49 (15% OFF)

🎣 Set de Pesca Completo
   $129.99 → $116.99 (10% OFF)

Para comprar visita: http://127.0.0.1:8000/aire-libre/
        """
        msg.body(respuesta.strip())
    
    elif 'entretenimiento' in mensaje or mensaje == '7':
        respuesta = """
🎮 *ENTRETENIMIENTO*

🎯 Consola Gaming Next Gen
   $499.99 → $449.99 (10% OFF)

📺 Smart TV 55" 4K
   $699.99 → $559.99 (20% OFF)

🎸 Guitarra Eléctrica
   $379.99 → $265.99 (30% OFF)

Para comprar visita: http://127.0.0.1:8000/entretenimiento/
        """
        msg.body(respuesta.strip())
    
    elif 'salud' in mensaje or mensaje == '8':
        respuesta = """
💪 *SALUD Y BIENESTAR*

🏃 Caminadora Eléctrica Pro
   $899.99 → $719.99 (20% OFF)

🏋️ Set de Pesas Ajustables
   $199.99 → $149.99 (25% OFF)

🧘 Mat de Yoga Premium
   $49.99 → $34.99 (30% OFF)

Para comprar visita: http://127.0.0.1:8000/salud/
        """
        msg.body(respuesta.strip())
    
    elif 'ofertas' in mensaje or 'descuento' in mensaje:
        respuesta = """
🔥 *OFERTAS DESTACADAS*

⭐ Hasta 30% de descuento en:
• Plancha de Cabello - 30% OFF
• Smartwatch Ultra - 30% OFF
• Guitarra Eléctrica - 30% OFF
• Mat de Yoga - 30% OFF

Visita nuestra tienda: http://127.0.0.1:8000/
        """
        msg.body(respuesta.strip())
    
    elif 'info' in mensaje or 'contacto' in mensaje:
        respuesta = """
📞 *INFORMACIÓN DE CONTACTO*

🏪 Superventas
📧 Email: info@superventas.com
📱 WhatsApp: +598 97403564
🌐 Web: http://127.0.0.1:8000/

🕒 Horario de atención:
Lunes a Viernes: 9:00 AM - 6:00 PM
Sábados: 9:00 AM - 1:00 PM

¡Envíos a todo el país! 🚚
        """
        msg.body(respuesta.strip())
    
    elif 'hola' in mensaje or 'hi' in mensaje or 'buenos' in mensaje:
        respuesta = """
👋 ¡Hola! Bienvenido a *Superventas*

Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?

Escribe *menu* para ver todas las opciones disponibles.
        """
        msg.body(respuesta.strip())
    
    else:
        respuesta = """
❓ No entendí tu mensaje.

Escribe *menu* para ver las opciones disponibles o escribe el nombre de una categoría:
• Belleza
• Tecnología
• Electrodomésticos
• Ferretería
• Bebé
• Aire Libre
• Entretenimiento
• Salud
        """
        msg.body(respuesta.strip())
    
    return HttpResponse(str(resp), content_type='text/xml')
