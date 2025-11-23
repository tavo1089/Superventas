# 🛒 Configuración de Mercado Pago para Uruguay

## 📋 Requisitos Previos

1. **Crear una cuenta de Mercado Pago Uruguay**
   - Visita: https://www.mercadopago.com.uy/
   - Regístrate o inicia sesión

2. **Acceder al Panel de Desarrolladores**
   - Ve a: https://www.mercadopago.com.uy/developers/panel
   - Crea una aplicación si no tienes una

## 🔑 Obtener Credenciales

### Paso 1: Credenciales de Prueba (para desarrollo)

1. En el panel de desarrolladores, ve a **"Tus integraciones"**
2. Selecciona tu aplicación
3. Ve a **"Credenciales de prueba"**
4. Copia:
   - **Public Key** (comienza con `TEST-...`)
   - **Access Token** (comienza con `TEST-...`)

### Paso 2: Credenciales de Producción (para ventas reales)

1. En el panel, ve a **"Credenciales de producción"**
2. **IMPORTANTE**: Solo estarán disponibles después de completar el proceso de activación
3. Copia:
   - **Public Key** (comienza con `APP_USR-...`)
   - **Access Token** (comienza con `APP_USR-...`)

## ⚙️ Configurar en tu Proyecto

### Opción 1: Variables de Entorno (Recomendado)

1. Crea o edita el archivo `.env` en la raíz de tu proyecto:

```env
# Mercado Pago - Credenciales de PRUEBA
MERCADOPAGO_PUBLIC_KEY=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MERCADOPAGO_ACCESS_TOKEN=TEST-xxxxxxxxxxxx-xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxx

# Para PRODUCCIÓN, reemplaza con tus credenciales reales:
# MERCADOPAGO_PUBLIC_KEY=APP_USR-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# MERCADOPAGO_ACCESS_TOKEN=APP_USR-xxxxxxxxxxxx-xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxx
```

2. Las variables ya están configuradas en `settings.py` para leerlas automáticamente

### Opción 2: Editar settings.py directamente (No recomendado para producción)

```python
# En superventas/settings.py
MERCADOPAGO_ACCESS_TOKEN = 'TEST-xxxxxxxxxxxx-xxxxxx-xxxxx'
MERCADOPAGO_PUBLIC_KEY = 'TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxx'
```

## 🧪 Probar los Pagos

### Tarjetas de Prueba para Uruguay

Mercado Pago proporciona tarjetas de prueba específicas para cada país:

**Tarjetas de Crédito de Prueba:**

| Tarjeta | Número | CVV | Fecha |
|---------|--------|-----|-------|
| Visa | 4509 9535 6623 3704 | 123 | 11/25 |
| Mastercard | 5031 4332 1540 6351 | 123 | 11/25 |

**Estados de Pago de Prueba:**

Para probar diferentes estados, usa estos nombres en el titular:
- **APRO**: Pago aprobado
- **CONT**: Pago pendiente
- **OTHE**: Rechazado por error general
- **CALL**: Rechazado con validación para autorizar
- **FUND**: Rechazado por monto insuficiente
- **SECU**: Rechazado por código de seguridad inválido
- **EXPI**: Rechazado por fecha de expiración inválida
- **FORM**: Rechazado por error en formulario

**Ejemplo:** 
- Nombre: `APRO`
- Tarjeta: `4509 9535 6623 3704`
- CVV: `123`
- Vencimiento: `11/25`

## 🚀 Pasar a Producción

### 1. Completar la Homologación

1. Ve al panel de Mercado Pago
2. Completa el formulario de **"Homologación"**:
   - Información del negocio
   - Datos fiscales
   - URL del sitio web
   - Flujo de compra

### 2. Activar las Credenciales de Producción

1. Una vez aprobada la homologación
2. Obtén tus credenciales de producción
3. **Actualiza el archivo `.env`**:

```env
# Cambiar a credenciales de PRODUCCIÓN
MERCADOPAGO_PUBLIC_KEY=APP_USR-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MERCADOPAGO_ACCESS_TOKEN=APP_USR-xxxxxxxxxxxx-xxxxxx-xxxxx
```

### 3. Configurar Webhooks (Notificaciones)

Para recibir notificaciones de pagos en tiempo real:

1. En el panel de Mercado Pago, ve a **"Webhooks"**
2. Agrega la URL de tu webhook:
   ```
   https://tudominio.com/webhook/mercadopago/
   ```
3. Selecciona los eventos:
   - ✅ Pagos
   - ✅ Reembolsos
   - ✅ Contracargos

4. **IMPORTANTE**: Tu servidor debe estar en HTTPS para recibir webhooks

## 📝 Notas Importantes

### Comisiones en Uruguay

- **Tarjetas de crédito**: ~5.9% + UYU 10 por transacción
- **Tarjetas de débito**: ~3.9% + UYU 10 por transacción
- **Saldo de Mercado Pago**: ~3.4%

### Plazos de Acreditación

- **Saldo de Mercado Pago**: Inmediato
- **Tarjeta de crédito**: 14 días
- **Tarjeta de débito**: 2 días hábiles

### Límites

- **Monto mínimo por transacción**: UYU 4
- **Monto máximo por transacción**: Consulta en el panel

## 🔒 Seguridad

1. **NUNCA** compartas tus credenciales
2. **NUNCA** subas el archivo `.env` a GitHub
3. Usa variables de entorno en producción
4. Mantén actualizadas las librerías de seguridad

## 📞 Soporte

- **Centro de ayuda**: https://www.mercadopago.com.uy/ayuda
- **Documentación técnica**: https://www.mercadopago.com.uy/developers/es/docs
- **Comunidad de desarrolladores**: https://www.mercadopago.com.uy/developers/es/community

## 🧪 Flujo de Prueba Completo

1. Agregar productos al carrito
2. Ir a checkout
3. Seleccionar "Mercado Pago"
4. Hacer clic en "Confirmar Pedido"
5. Serás redirigido al checkout de Mercado Pago
6. Usar tarjeta de prueba
7. Completar el pago
8. Serás redirigido de vuelta a tu sitio
9. El pedido aparecerá en "Mis Pedidos"

## ✅ Verificación

Para verificar que todo está configurado correctamente:

```python
# En el shell de Django
python manage.py shell

from django.conf import settings
print(settings.MERCADOPAGO_ACCESS_TOKEN)
print(settings.MERCADOPAGO_PUBLIC_KEY)
```

Si ves tus credenciales, ¡está todo listo! 🎉

## 🌐 URLs Importantes

- **Panel de Desarrolladores**: https://www.mercadopago.com.uy/developers/panel
- **Documentación SDK Python**: https://github.com/mercadopago/sdk-python
- **Credenciales de Prueba**: https://www.mercadopago.com.uy/developers/panel/credentials/test
- **Credenciales de Producción**: https://www.mercadopago.com.uy/developers/panel/credentials/production
