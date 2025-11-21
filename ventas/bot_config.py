# 🤖 CONFIGURACIÓN DEL CHATBOT DE WHATSAPP
# ==========================================
# Edita este archivo para personalizar las respuestas del bot

"""
INSTRUCCIONES PARA PERSONALIZAR:

1. Cambia la información de tu negocio en la sección DATOS DEL NEGOCIO
2. Ajusta los horarios según tu disponibilidad
3. Modifica las categorías según tus productos
4. Actualiza costos de envío y métodos de pago
5. Guarda el archivo y reinicia el servidor

Nota: Después de editar, ejecuta:
python manage.py runserver
"""

# ==========================================
# DATOS DEL NEGOCIO
# ==========================================

NOMBRE_NEGOCIO = "Superventas"
URL_TIENDA = "http://127.0.0.1:8000"  # Cambiar por tu dominio en producción
TELEFONO_SOPORTE = "+51 999 999 999"  # Tu número de WhatsApp/teléfono
EMAIL_SOPORTE = "soporte@superventas.com"
CIUDAD_NEGOCIO = "Lima"
DIRECCION_NEGOCIO = "Av. Ejemplo 123, San Isidro"

# ==========================================
# HORARIOS DE ATENCIÓN
# ==========================================

HORARIO_TIENDA_SEMANA = "Lun-Vie: 9:00 AM - 8:00 PM"
HORARIO_TIENDA_SABADO = "Sábados: 9:00 AM - 6:00 PM"
HORARIO_TIENDA_DOMINGO = "Domingos: 10:00 AM - 2:00 PM"
HORARIO_DELIVERY = "Lun-Sáb: 9:00 AM - 6:00 PM"
HORARIO_SOPORTE = "Lun-Vie: 9:00 AM - 6:00 PM"

# ==========================================
# CATEGORÍAS DE PRODUCTOS
# ==========================================
# Edita, agrega o elimina categorías según tu catálogo

CATEGORIAS = [
    {'emoji': '🌸', 'nombre': 'Belleza - Cuidado personal y cosmética'},
    {'emoji': '💻', 'nombre': 'Tecnología - Smartphones, laptops y más'},
    {'emoji': '🏠', 'nombre': 'Electrodomésticos - Para tu hogar'},
    {'emoji': '🔧', 'nombre': 'Ferretería - Herramientas profesionales'},
    {'emoji': '👶', 'nombre': 'Bebé - Productos infantiles'},
    {'emoji': '🏕️', 'nombre': 'Aire Libre - Camping y aventura'},
    {'emoji': '🎮', 'nombre': 'Entretenimiento - Gaming y diversión'},
    {'emoji': '💪', 'nombre': 'Salud - Fitness y bienestar'}
]

# ==========================================
# INFORMACIÓN DE ENVÍOS
# ==========================================

COSTO_ENVIO_ESTANDAR = "S/10"
TIEMPO_ENVIO_ESTANDAR = "3-5 días hábiles"
COSTO_ENVIO_EXPRESS = "S/20"
TIEMPO_ENVIO_EXPRESS = "1-2 días hábiles"
ENVIO_GRATIS_DESDE = "S/100"
ZONAS_COBERTURA = "Lima y Callao"

# ==========================================
# HORARIOS Y UBICACIÓN
# ==========================================

HORARIOS = f"""{HORARIO_TIENDA_SEMANA}
{HORARIO_TIENDA_SABADO}
{HORARIO_TIENDA_DOMINGO}

Delivery: {HORARIO_DELIVERY}
Soporte: {HORARIO_SOPORTE}"""

DIRECCION_TIENDA = f"""{DIRECCION_NEGOCIO}
{CIUDAD_NEGOCIO}
Telefono: {TELEFONO_SOPORTE}
Email: {EMAIL_SOPORTE}"""

METODOS_ENVIO = [
    f"Envio Estandar - {COSTO_ENVIO_ESTANDAR} ({TIEMPO_ENVIO_ESTANDAR})",
    f"Envio Express - {COSTO_ENVIO_EXPRESS} ({TIEMPO_ENVIO_EXPRESS})",
    f"Envio GRATIS en compras desde {ENVIO_GRATIS_DESDE}"
]

# ==========================================
# MENÚ PRINCIPAL
# ==========================================

MENU_PRINCIPAL = """¿En que puedo ayudarte?

1️⃣ Ver catalogo
2️⃣ Buscar producto
3️⃣ Estado de pedido
4️⃣ Soporte
5️⃣ Horarios
6️⃣ Ubicacion

Escribe el numero de la opcion"""

# ==========================================
# MÉTODOS DE PAGO
# ==========================================

METODOS_PAGO = [
    "✅ Tarjetas Visa/Mastercard",
    "✅ Yape / Plin",
    "✅ Transferencia bancaria",
    "✅ Efectivo contra entrega"
]

# ==========================================
# MENSAJES PERSONALIZADOS
# ==========================================

# Mensaje de bienvenida (puedes usar {sender_name} para el nombre del cliente)
MENSAJE_BIENVENIDA = """
🛒 *¡Hola {sender_name}! Bienvenido a {negocio}*

¿En qué puedo ayudarte hoy?

*1* 📦 Ver catálogo completo
*2* 🔍 Buscar producto específico
*3* 📋 Estado de mi pedido
*4* 🆘 Hablar con soporte
*5* ⏰ Horarios de atención
*6* 📍 Ubicación y contacto

_Responde con el número de la opción_
"""

# Mensaje de despedida
MENSAJE_DESPEDIDA = """
😊 *¡Gracias por contactar a {negocio}!*

Fue un placer ayudarte.

¿Necesitas algo más?
Escribe *MENU* para ver opciones.

🛒 Visita nuestra tienda:
👉 {url}
"""

# Mensaje para consultas no reconocidas
MENSAJE_NO_ENTENDIDO = """
🤔 No entendí tu mensaje.

Puedes:
• Escribir *MENU* para ver opciones
• Escribir el nombre de un producto para buscarlo
• Contactar soporte: *4*

¿En qué puedo ayudarte?
"""

# ==========================================
# PROMOCIONES Y OFERTAS (OPCIONAL)
# ==========================================

# Si tienes promociones activas, edítalas aquí
PROMOCION_ACTIVA = True
MENSAJE_PROMOCION = """
🎉 *¡OFERTA ESPECIAL!*

💥 20% de descuento en productos seleccionados
🎁 Envío GRATIS en compras mayores a S/100
⏰ Válido hasta el 30/11/2025

Ver ofertas: {url}
"""

# ==========================================
# POLÍTICAS Y TÉRMINOS
# ==========================================

TIEMPO_GARANTIA = "30 días"
ACEPTA_DEVOLUCIONES = True
TIEMPO_DEVOLUCION = "15 días"

POLITICA_DEVOLUCION = f"""
🔄 *Política de Devoluciones*

✅ Aceptamos devoluciones hasta {TIEMPO_DEVOLUCION} después de la compra
✅ El producto debe estar en su empaque original
✅ Reembolso completo o cambio por otro producto

📞 Contacta a soporte para iniciar: {TELEFONO_SOPORTE}
"""

# ==========================================
# RESPUESTAS AUTOMÁTICAS ADICIONALES
# ==========================================

# Palabras clave y sus respuestas
RESPUESTAS_AUTOMATICAS = {
    'precio': 'Para consultar precios, visita nuestro catalogo: {url} o escribe el nombre del producto.',
    'ofertas': '🎁 Tenemos ofertas especiales cada semana. Visita: {url} o escribe *MENU*',
    'garantia': f'Todos nuestros productos tienen {TIEMPO_GARANTIA} de garantia. Escribe *4* para mas info.',
    'cambio': POLITICA_DEVOLUCION,
    'devolucion': POLITICA_DEVOLUCION,
    'soporte': f'Estamos aqui para ayudarte! \n\nContactanos:\n📞 {TELEFONO_SOPORTE}\n📧 {EMAIL_SOPORTE}\n\nHorario: {HORARIO_SOPORTE}',
    'envio': f'Opciones de envio:\n- {COSTO_ENVIO_ESTANDAR} ({TIEMPO_ENVIO_ESTANDAR})\n- {COSTO_ENVIO_EXPRESS} ({TIEMPO_ENVIO_EXPRESS})\n- GRATIS desde {ENVIO_GRATIS_DESDE}\n\nCobertura: {ZONAS_COBERTURA}',
    'devoluciones': POLITICA_DEVOLUCION,
    'promociones': MENSAJE_PROMOCION if PROMOCION_ACTIVA else 'Proximamente nuevas promociones! Visita: {url}'
}

# ==========================================
# CONFIGURACIÓN AVANZADA
# ==========================================

# Activar/desactivar funciones
ACTIVAR_BUSQUEDA_AUTOMATICA = True
ACTIVAR_RECOMENDACIONES = True
ACTIVAR_PROMOCIONES = True
REGISTRAR_CONVERSACIONES = True

# Mensajes automáticos
ENVIAR_CONFIRMACION_PEDIDO = True
ENVIAR_ACTUALIZACION_ENVIO = True
ENVIAR_RECORDATORIO_CARRITO = True

# Tiempo para recordatorio de carrito abandonado (en horas)
TIEMPO_RECORDATORIO_CARRITO = 24
