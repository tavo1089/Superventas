# Configuración de Stripe para Pagos con Tarjeta

## 📌 ¿Qué es Stripe?

Stripe es una plataforma de procesamiento de pagos que permite aceptar tarjetas de crédito y débito de forma segura en tu tienda online.

## 🚀 Pasos para Configurar Stripe

### 1. Crear Cuenta en Stripe

1. Ve a [https://dashboard.stripe.com/register](https://dashboard.stripe.com/register)
2. Crea tu cuenta (puede ser con email o Google/GitHub)
3. Completa la información de tu negocio

### 2. Obtener Claves de API de Prueba

1. Una vez dentro del dashboard, ve a **Developers** (Desarrolladores)
2. Haz clic en **API keys** (Claves de API)
3. Verás dos claves en modo **Test** (Prueba):
   - **Publishable key** (Clave pública): Empieza con `pk_test_...`
   - **Secret key** (Clave secreta): Empieza con `sk_test_...`
   - ⚠️ Haz clic en "Reveal test key" para ver la clave secreta completa

### 3. Configurar en tu Proyecto

Abre el archivo `.env` y reemplaza las claves:

```env
# Stripe - Claves de prueba
STRIPE_PUBLIC_KEY=pk_test_TU_CLAVE_PUBLICA_AQUI
STRIPE_SECRET_KEY=sk_test_TU_CLAVE_SECRETA_AQUI
```

**Ejemplo:**
```env
STRIPE_PUBLIC_KEY=pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890
STRIPE_SECRET_KEY=sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz9876543210
```

### 4. Reiniciar el Servidor

Después de guardar el archivo `.env`, reinicia el servidor Django:

```bash
# Detén el servidor (Ctrl+C)
# Vuelve a iniciarlo
python manage.py runserver
```

## 🧪 Probar Pagos en Modo Test

Stripe proporciona tarjetas de prueba que puedes usar:

### Tarjetas de Prueba Exitosas:

| Número de Tarjeta | Tipo | Resultado |
|-------------------|------|-----------|
| `4242 4242 4242 4242` | Visa | Pago exitoso |
| `5555 5555 5555 4444` | Mastercard | Pago exitoso |
| `3782 822463 10005` | American Express | Pago exitoso |

### Datos Adicionales para Pruebas:

- **Fecha de expiración**: Cualquier fecha futura (ej: 12/25)
- **CVC**: Cualquier 3 dígitos (ej: 123)
- **Código postal**: Cualquier código (ej: 12345)

### Tarjetas para Probar Errores:

| Número de Tarjeta | Resultado |
|-------------------|-----------|
| `4000 0000 0000 0002` | Tarjeta declinada |
| `4000 0000 0000 9995` | Fondos insuficientes |

## 🌍 Activar Modo Producción

Cuando estés listo para recibir pagos reales:

### 1. Completar Información de Negocio

En el dashboard de Stripe:
1. Ve a **Settings** > **Business settings**
2. Completa toda la información requerida:
   - Datos del negocio
   - Información fiscal
   - Cuenta bancaria para recibir pagos

### 2. Obtener Claves de Producción

1. Ve a **Developers** > **API keys**
2. Cambia el toggle de **Test mode** a **Live mode**
3. Copia las nuevas claves (empiezan con `pk_live_...` y `sk_live_...`)

### 3. Actualizar el .env

```env
# Stripe - Claves de PRODUCCIÓN
STRIPE_PUBLIC_KEY=pk_live_TU_CLAVE_PUBLICA_PRODUCCION
STRIPE_SECRET_KEY=sk_live_TU_CLAVE_SECRETA_PRODUCCION
```

## 💰 Comisiones de Stripe

Stripe cobra por transacción:
- **Uruguay**: ~2.9% + $0.30 USD por transacción exitosa
- **Sin costos mensuales fijos**
- Solo pagas cuando recibes un pago

## 🔒 Seguridad

- ✅ **PCI Compliance**: Stripe maneja toda la seguridad de las tarjetas
- ✅ **Encriptación**: Todos los datos se transmiten de forma segura
- ✅ **No almacenas tarjetas**: Los datos sensibles nunca pasan por tu servidor
- ✅ **3D Secure**: Autenticación adicional para tarjetas que lo requieren

## 📞 Soporte

- **Documentación**: [https://stripe.com/docs](https://stripe.com/docs)
- **Soporte**: support@stripe.com
- **Dashboard**: [https://dashboard.stripe.com](https://dashboard.stripe.com)

## ✅ Verificar Configuración

Para verificar que Stripe está configurado correctamente:

1. Ve a tu tienda y agrega productos al carrito
2. Ve a **Checkout**
3. Selecciona "Tarjeta de Crédito o Débito"
4. Haz clic en "Confirmar Pedido"
5. Deberías ser redirigido a la página de pago de Stripe

Si ves un error, revisa:
- ✅ Las claves están correctamente copiadas en `.env`
- ✅ No hay espacios antes/después de las claves
- ✅ El servidor está reiniciado después de modificar `.env`

---

## 🎯 Diferencias: Stripe vs Mercado Pago

| Característica | Stripe | Mercado Pago |
|----------------|--------|--------------|
| Alcance | Global | Latinoamérica |
| Interfaz | En tu sitio | Redirección externa |
| Comisiones | ~2.9% + $0.30 | ~3.99% |
| Monedas | Múltiples | Local |
| Implementación | Más técnico | Más simple |

**Recomendación**: Ofrece ambas opciones para dar más flexibilidad a tus clientes. Algunos prefieren Mercado Pago (más conocido en Uruguay), otros prefieren pagar directo con tarjeta vía Stripe.
