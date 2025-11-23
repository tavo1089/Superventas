# Configuración de Email para Notificaciones de Pedidos

## 📧 ¿Qué hace?

Cada vez que se realiza un pedido, el sistema enviará automáticamente:
1. **Email al cliente**: Confirmación con detalles del pedido
2. **Email al administrador**: Notificación de nuevo pedido

## 🔧 Configuración con Gmail

### Paso 1: Habilitar Contraseña de Aplicación en Gmail

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el menú izquierdo, selecciona **Seguridad**
3. Activa la **Verificación en 2 pasos** (si no la tienes activada)
4. Busca **Contraseñas de aplicaciones**
5. Selecciona:
   - Aplicación: **Correo**
   - Dispositivo: **Otro** (escribe "Django Superventas")
6. Copia la contraseña de 16 dígitos que te genera

### Paso 2: Configurar el archivo .env

Abre el archivo `.env` y actualiza estas líneas:

```env
# Email - Configuración para envío de emails
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # La contraseña de 16 dígitos de aplicación
DEFAULT_FROM_EMAIL=tu_email@gmail.com
ADMIN_EMAIL=tu_email@gmail.com  # Email donde recibirás las notificaciones de pedidos
```

**Importante**: 
- Usa la contraseña de aplicación de 16 dígitos, NO tu contraseña normal de Gmail
- `ADMIN_EMAIL` es donde recibirás las notificaciones de nuevos pedidos

### Paso 3: Reiniciar el servidor

```bash
# Detén el servidor con Ctrl+C y reinícialo
python manage.py runserver
```

## 🧪 Probar que funciona

1. Realiza un pedido de prueba en tu tienda
2. Deberías recibir:
   - Un email en la cuenta del cliente
   - Un email en el `ADMIN_EMAIL` con los detalles del pedido

## 📧 Usar otro proveedor de email (opcional)

### Gmail (ya configurado)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

### Outlook/Hotmail
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Yahoo
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Otro proveedor SMTP
Consulta la documentación de tu proveedor de email para obtener:
- Servidor SMTP (EMAIL_HOST)
- Puerto (EMAIL_PORT)
- Si usa TLS/SSL

## 🔍 Solución de Problemas

### No recibo emails

1. **Verifica la configuración del .env**:
   ```bash
   # Asegúrate que los datos son correctos
   EMAIL_HOST_USER=tu_email_real@gmail.com
   ```

2. **Revisa la consola del servidor**:
   - Cualquier error de email aparecerá en la terminal donde corre Django

3. **Verifica la contraseña de aplicación**:
   - Debe ser de 16 dígitos, sin espacios
   - NO es tu contraseña normal de Gmail

4. **Revisa carpeta de spam**:
   - Los primeros emails pueden caer en spam

### Error: "SMTPAuthenticationError"

- La contraseña de aplicación es incorrecta
- La verificación en 2 pasos no está activada en Gmail

### El email se envía pero no llega

- Revisa la carpeta de spam
- Verifica que `DEFAULT_FROM_EMAIL` sea un email válido

## 💡 Modo de Desarrollo

Si NO quieres configurar email ahora, el sistema funcionará igual:
- Los pedidos se crearán correctamente
- Solo no se enviarán los emails
- Los errores de email se ignoran (`fail_silently=True`)

Para ver los emails en consola sin enviarlos (útil para desarrollo):

En `settings.py` cambia:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Los emails se mostrarán en la terminal del servidor en lugar de enviarse.

## 📝 Contenido de los Emails

### Email al Cliente:
- Número de pedido
- Fecha y hora
- Lista de productos con precios
- Total a pagar
- Método de pago
- Dirección de envío
- Estado del pago

### Email al Administrador:
- Todos los datos del cliente
- Detalles completos del pedido
- Notas adicionales del cliente
- Información para preparar el envío

## ✅ Listo!

Una vez configurado, cada pedido enviará automáticamente las notificaciones por email.
