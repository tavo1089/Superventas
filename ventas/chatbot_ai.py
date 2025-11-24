"""
Chatbot con IA usando Groq (gratuito)
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import requests

GROQ_API_KEY = getattr(settings, 'GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Información del negocio para el chatbot
CONTEXTO_NEGOCIO = """
Eres un asistente virtual de SUPERVENTAS, una tienda online en Uruguay.

INFORMACIÓN DE LA TIENDA:
- Vendemos productos de 8 categorías: Belleza, Tecnología, Electrodomésticos, Ferretería, Bebé, Aire Libre, Entretenimiento y Salud
- Ofrecemos descuentos en productos seleccionados
- Aceptamos pagos con Stripe, MercadoPago y Google Pay
- Tenemos WhatsApp de contacto: +598 97403564
- El sitio web es http://127.0.0.1:8000/

PRODUCTOS DESTACADOS:
- Belleza: Crema Hidratante ($399), Set de Maquillaje ($2599), Perfume Premium ($1799)
- Tecnología: Smartphone Galaxy ($7999), Laptop HP ($18999), Auriculares Bluetooth ($1299)
- Electrodomésticos: Licuadora ($1899), Cafetera Express ($3299), Aspiradora Robot ($8999)

TU TRABAJO:
1. Responder preguntas sobre productos, precios y categorías
2. Ayudar con dudas sobre envíos y pagos
3. Recomendar productos según necesidades del cliente
4. Si no sabes algo específico, sugiere contactar por WhatsApp
5. Sé amable, profesional y conciso (máximo 3-4 líneas por respuesta)

IMPORTANTE: Siempre habla en español y de manera natural.
"""

@csrf_exempt
@require_POST
def chatbot_respuesta(request):
    """
    Endpoint para recibir mensajes del chatbot y responder con IA
    """
    try:
        data = json.loads(request.body)
        mensaje_usuario = data.get('mensaje', '').strip()
        
        if not mensaje_usuario:
            return JsonResponse({
                'error': 'No se recibió ningún mensaje'
            }, status=400)
        
        if not GROQ_API_KEY:
            # Respuesta de fallback si no hay API key
            return JsonResponse({
                'respuesta': '¡Hola! Soy el asistente virtual de Superventas. ¿En qué puedo ayudarte?\n\n' +
                            '📱 Para respuestas más rápidas, escríbenos por WhatsApp: +598 97403564'
            })
        
        # Llamar a Groq API
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'llama-3.1-8b-instant',  # Modelo gratuito, rápido y disponible
            'messages': [
                {
                    'role': 'system',
                    'content': CONTEXTO_NEGOCIO
                },
                {
                    'role': 'user',
                    'content': mensaje_usuario
                }
            ],
            'temperature': 0.7,
            'max_tokens': 300,
            'top_p': 1
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            resultado = response.json()
            respuesta_ia = resultado['choices'][0]['message']['content']
            
            return JsonResponse({
                'respuesta': respuesta_ia
            })
        else:
            # Imprimir error para debug
            print(f"Error Groq API - Status: {response.status_code}")
            print(f"Respuesta: {response.text}")
            # Fallback si hay error
            return JsonResponse({
                'respuesta': '¡Hola! Estoy teniendo problemas técnicos. ' +
                            'Para ayudarte mejor, escríbenos por WhatsApp: +598 97403564 😊'
            })
    
    except Exception as e:
        print(f"Error en chatbot: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'respuesta': '¡Hola! Soy el asistente de Superventas. ' +
                        'Para ayudarte de inmediato, contáctanos por WhatsApp: +598 97403564'
        })
