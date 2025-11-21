# 📝 GUÍA: Cómo Personalizar el Chatbot de WhatsApp

## 🎯 Archivo Principal de Configuración

**Archivo:** `ventas/bot_config.py`

Este archivo contiene **TODA** la configuración del bot. Solo edita este archivo para cambiar las respuestas.

---

## 📦 SECCIÓN 1: Datos del Negocio

```python
NOMBRE_NEGOCIO = "Superventas"              # ← Cambia por el nombre de tu tienda
URL_TIENDA = "http://127.0.0.1:8000"        # ← Tu dominio (ej: www.mitienda.com)
TELEFONO_SOPORTE = "+51 999 999 999"        # ← Tu WhatsApp/teléfono
EMAIL_SOPORTE = "soporte@superventas.com"   # ← Tu email
CIUDAD_NEGOCIO = "Lima"                     # ← Tu ciudad
DIRECCION_NEGOCIO = "Av. Ejemplo 123"       # ← Tu dirección
```

**Ejemplo real:**
```python
NOMBRE_NEGOCIO = "TechStore Peru"
URL_TIENDA = "https://www.techstoreperu.com"
TELEFONO_SOPORTE = "+51 987 654 321"
EMAIL_SOPORTE = "ventas@techstoreperu.com"
CIUDAD_NEGOCIO = "Arequipa"
DIRECCION_NEGOCIO = "Calle Mercaderes 456, Centro"
```

---

## ⏰ SECCIÓN 2: Horarios

```python
HORARIO_TIENDA_SEMANA = "Lun-Vie: 9:00 AM - 8:00 PM"
HORARIO_TIENDA_SABADO = "Sábados: 9:00 AM - 6:00 PM"
HORARIO_TIENDA_DOMINGO = "Domingos: 10:00 AM - 2:00 PM"
HORARIO_DELIVERY = "Lun-Sáb: 9:00 AM - 6:00 PM"
```

**Ejemplo: Tienda 24/7**
```python
HORARIO_TIENDA_SEMANA = "Lun-Dom: 24 horas"
HORARIO_DELIVERY = "Lun-Dom: 24 horas"
```

**Ejemplo: Solo fin de semana**
```python
HORARIO_TIENDA_SEMANA = "Cerrado entre semana"
HORARIO_TIENDA_SABADO = "Sáb-Dom: 10:00 AM - 8:00 PM"
```

---

## 📦 SECCIÓN 3: Categorías de Productos

```python
CATEGORIAS = [
    "🌸 *Belleza* - Cuidado personal",
    "💻 *Tecnología* - Gadgets",
    # Agrega o elimina categorías aquí
]
```

**Ejemplo: Tienda de ropa**
```python
CATEGORIAS = [
    "👕 *Hombres* - Ropa masculina",
    "👗 *Mujeres* - Moda femenina",
    "👶 *Niños* - Ropa infantil",
    "👟 *Calzado* - Zapatos y zapatillas",
    "👜 *Accesorios* - Bolsos y más"
]
```

**Ejemplo: Restaurante**
```python
CATEGORIAS = [
    "🍕 *Pizzas* - Artesanales y clásicas",
    "🍔 *Hamburguesas* - Gourmet y tradicionales",
    "🥗 *Ensaladas* - Frescas y saludables",
    "🍰 *Postres* - Dulces y helados",
    "🥤 *Bebidas* - Naturales y gaseosas"
]
```

---

## 🚚 SECCIÓN 4: Información de Envíos

```python
COSTO_ENVIO_ESTANDAR = "S/10"
TIEMPO_ENVIO_ESTANDAR = "3-5 días hábiles"
COSTO_ENVIO_EXPRESS = "S/20"
TIEMPO_ENVIO_EXPRESS = "1-2 días hábiles"
ENVIO_GRATIS_DESDE = "S/100"
ZONAS_COBERTURA = "Lima y Callao"
```

**Ejemplo: Envío gratis siempre**
```python
COSTO_ENVIO_ESTANDAR = "GRATIS"
ENVIO_GRATIS_DESDE = "S/0"
```

---

## 💳 SECCIÓN 5: Métodos de Pago

```python
METODOS_PAGO = [
    "✅ Tarjetas Visa/Mastercard",
    "✅ Yape / Plin",
    "✅ Transferencia bancaria",
    "✅ Efectivo contra entrega"
]
```

**Ejemplo: Solo efectivo**
```python
METODOS_PAGO = [
    "✅ Efectivo contra entrega",
    "✅ Transferencia BCP/Interbank"
]
```

---

## 💬 SECCIÓN 6: Mensajes Personalizados

### Mensaje de Bienvenida

```python
MENSAJE_BIENVENIDA = """
🛒 *¡Hola {sender_name}! Bienvenido a {negocio}*

¿En qué puedo ayudarte hoy?
"""
```

**Variables disponibles:**
- `{sender_name}` - Nombre del cliente
- `{negocio}` - Nombre de tu negocio
- `{url}` - URL de tu tienda

**Ejemplo personalizado:**
```python
MENSAJE_BIENVENIDA = """
👋 *Hola {sender_name}!*

Bienvenido a *{negocio}* 🎉

Somos tu tienda de confianza con más de 10 años de experiencia.

¿Qué estás buscando hoy?

*1* Ver productos
*2* Ofertas del día
*3* Hablar con asesor
"""
```

---

## 🎁 SECCIÓN 7: Promociones

```python
PROMOCION_ACTIVA = True  # True = mostrar, False = ocultar
MENSAJE_PROMOCION = """
🎉 *¡OFERTA ESPECIAL!*

💥 20% de descuento
"""
```

**Ejemplo: Black Friday**
```python
PROMOCION_ACTIVA = True
MENSAJE_PROMOCION = """
🔥 *BLACK FRIDAY - HOY SOLAMENTE*

💥 Hasta 70% de descuento
🎁 2x1 en productos seleccionados
🚚 Envío GRATIS en todo
⏰ Solo hasta medianoche

🛒 Aprovecha: {url}/black-friday
"""
```

---

## 🔄 SECCIÓN 8: Políticas

```python
TIEMPO_GARANTIA = "30 días"
ACEPTA_DEVOLUCIONES = True
TIEMPO_DEVOLUCION = "15 días"
```

**Ejemplo: Sin devoluciones**
```python
ACEPTA_DEVOLUCIONES = False
TIEMPO_GARANTIA = "No aplicable - productos digitales"
```

---

## 🤖 RESPUESTAS AUTOMÁTICAS POR PALABRA CLAVE

```python
RESPUESTAS_AUTOMATICAS = {
    'precio': 'Respuesta cuando mencionen "precio"',
    'ofertas': 'Respuesta cuando mencionen "ofertas"',
    # Agrega más palabras clave
}
```

**Ejemplo completo:**
```python
RESPUESTAS_AUTOMATICAS = {
    'precio': '💰 Todos nuestros precios están en {url}. ¿Qué producto te interesa?',
    'ofertas': '🎁 Esta semana: 20% en tecnología. Ver: {url}/ofertas',
    'garantia': '✅ Garantía de {TIEMPO_GARANTIA} en todos los productos.',
    'horario': 'Abiertos: {HORARIO_TIENDA_SEMANA}',
    'ubicacion': '📍 Estamos en {DIRECCION_NEGOCIO}, {CIUDAD_NEGOCIO}',
    'envio': '🚚 Envío desde {COSTO_ENVIO_ESTANDAR}. GRATIS en compras +{ENVIO_GRATIS_DESDE}',
}
```

---

## 📋 EJEMPLOS DE NEGOCIOS ESPECÍFICOS

### 🍕 Restaurante / Delivery de Comida

```python
NOMBRE_NEGOCIO = "Pizza Express"
CATEGORIAS = [
    "🍕 Pizzas - Clásicas y especiales",
    "🍝 Pastas - Caseras",
    "🥗 Ensaladas - Frescas",
    "🍰 Postres - Dulces",
]
HORARIO_TIENDA_SEMANA = "Lun-Dom: 11:00 AM - 11:00 PM"
COSTO_ENVIO_ESTANDAR = "S/5"
TIEMPO_ENVIO_ESTANDAR = "30-45 minutos"
ENVIO_GRATIS_DESDE = "S/50"
```

### 👗 Tienda de Ropa

```python
NOMBRE_NEGOCIO = "Fashion Store"
CATEGORIAS = [
    "👕 Hombres - Casual y formal",
    "👗 Mujeres - Vestidos y blusas",
    "👶 Niños - Ropa infantil",
    "👟 Calzado - Todas las tallas",
]
METODOS_PAGO = [
    "✅ Tarjetas",
    "✅ Yape/Plin",
    "✅ Cuotas sin interés"
]
```

### 💊 Farmacia

```python
NOMBRE_NEGOCIO = "FarmaPlus"
CATEGORIAS = [
    "💊 Medicamentos - Con receta",
    "🏥 Salud - Vitaminas y suplementos",
    "👶 Bebé - Pañales y leches",
    "💄 Belleza - Cosméticos",
]
HORARIO_TIENDA_SEMANA = "Lun-Dom: 24 horas"
COSTO_ENVIO_EXPRESS = "S/10"
TIEMPO_ENVIO_EXPRESS = "30 minutos"
```

---

## ⚙️ Cómo Aplicar los Cambios

### Paso 1: Editar el archivo
```bash
# Abre el archivo
code ventas/bot_config.py

# O usa cualquier editor de texto
notepad ventas/bot_config.py
```

### Paso 2: Guardar cambios

### Paso 3: Reiniciar el servidor
```bash
# Ctrl+C para detener el servidor
# Luego:
python manage.py runserver
```

### Paso 4: Probar en WhatsApp
```
Envía: hola
```

---

## 🎨 Tips de Personalización

### Emojis Recomendados

```
🛒 Compras/Carrito
📦 Productos/Pedidos
🚚 Envíos
💳 Pagos
⏰ Horarios
📍 Ubicación
💰 Precios
🎁 Ofertas/Regalos
✅ Confirmación
❌ Cancelación
🔍 Búsqueda
💬 Chat/Mensajes
📞 Teléfono
📧 Email
⭐ Destacados
🔥 Popular
```

### Formato de Texto WhatsApp

```
*Negrita* - Usa asteriscos
_Cursiva_ - Usa guiones bajos
~Tachado~ - Usa virgulilla
```monoespaciado``` - Usa acentos graves
```

---

## ✅ Checklist de Personalización

- [ ] Cambiar NOMBRE_NEGOCIO
- [ ] Actualizar URL_TIENDA
- [ ] Configurar TELEFONO_SOPORTE
- [ ] Ajustar HORARIOS
- [ ] Modificar CATEGORIAS según tus productos
- [ ] Actualizar costos de ENVIO
- [ ] Configurar METODOS_PAGO
- [ ] Personalizar MENSAJE_BIENVENIDA
- [ ] Agregar PROMOCIONES activas
- [ ] Definir POLITICA_DEVOLUCION
- [ ] Probar enviando "hola" al bot

---

## 🆘 Ayuda Rápida

**¿No aparecen los cambios?**
1. Guarda el archivo
2. Reinicia el servidor (Ctrl+C y `python manage.py runserver`)

**¿Quieres más opciones en el menú?**
Edita el archivo `ventas/whatsapp_bot.py` línea 70+

**¿Problemas con emojis?**
Los emojis funcionan perfectamente en WhatsApp, no te preocupes por los errores del editor.

---

## 📞 Soporte

Si necesitas ayuda personalizando tu bot, contacta con el desarrollador.
