# 🚨 Solución Rápida: Error al Crear Preferencia de Pago

## El Problema
Ves el mensaje: **"Error al crear la preferencia de pago"** cuando intentas confirmar un pedido con Mercado Pago.

## Causa
**No tienes configuradas las credenciales de Mercado Pago** en tu proyecto.

---

## ✅ SOLUCIÓN RÁPIDA (5 minutos)

### Paso 1: Obtener Credenciales de Prueba

1. **Crea una cuenta en Mercado Pago Uruguay**
   - Ve a: https://www.mercadopago.com.uy/
   - Regístrate (es gratis)

2. **Accede al Panel de Desarrolladores**
   - Ve a: https://www.mercadopago.com.uy/developers/panel
   - Inicia sesión con tu cuenta

3. **Crea una Aplicación**
   - Haz clic en "Crear aplicación"
   - Nombre: "Superventas"
   - Selecciona "Pagos en línea"
   - Guarda

4. **Copia tus Credenciales de PRUEBA**
   - En el panel, ve a "Credenciales de prueba"
   - Verás dos credenciales:
     * **Public Key**: `TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
     * **Access Token**: `TEST-xxxxxxxxxxxx-xxxxxx-xxxxx...`
   - Copia ambas

### Paso 2: Configurar en tu Proyecto

**Opción A: Crear archivo .env (Recomendado)**

1. Crea un archivo llamado `.env` en la carpeta raíz de tu proyecto (donde está `manage.py`)

2. Agrega estas líneas (reemplaza con tus credenciales):

```env
MERCADOPAGO_PUBLIC_KEY=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MERCADOPAGO_ACCESS_TOKEN=TEST-xxxxxxxxxxxx-xxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxx
```

3. Guarda el archivo

**Opción B: Editar settings.py directamente**

1. Abre el archivo `superventas/settings.py`

2. Busca estas líneas (al final del archivo):

```python
try:
    MERCADOPAGO_ACCESS_TOKEN = env('MERCADOPAGO_ACCESS_TOKEN', default='')
    MERCADOPAGO_PUBLIC_KEY = env('MERCADOPAGO_PUBLIC_KEY', default='')
except:
    MERCADOPAGO_ACCESS_TOKEN = ''
    MERCADOPAGO_PUBLIC_KEY = ''
```

3. Reemplázalas con:

```python
MERCADOPAGO_ACCESS_TOKEN = 'TEST-xxxxxxxxxxxx-xxxxxx-xxxxx'  # TU ACCESS TOKEN AQUÍ
MERCADOPAGO_PUBLIC_KEY = 'TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxx'  # TU PUBLIC KEY AQUÍ
```

### Paso 3: Reiniciar el Servidor

1. Detén el servidor (Ctrl+C en la terminal)
2. Vuelve a iniciarlo:
   ```bash
   python manage.py runserver
   ```

### Paso 4: Probar

1. Ve a: http://127.0.0.1:8000/test-mp-config/
2. Deberías ver: `✅ Mercado Pago está correctamente configurado`

Si ves este mensaje, ¡ya está funcionando! 🎉

---

## 🧪 Probar un Pago de Prueba

### Tarjetas de Prueba para Uruguay:

**Visa (Aprobar pago):**
- Número: `4509 9535 6623 3704`
- CVV: `123`
- Vencimiento: `11/25`
- Nombre: `APRO`

**Mastercard (Aprobar pago):**
- Número: `5031 4332 1540 6351`
- CVV: `123`
- Vencimiento: `11/25`
- Nombre: `APRO`

### Flujo de Prueba:

1. Agrega productos al carrito
2. Ve a checkout
3. Selecciona "Mercado Pago"
4. Haz clic en "Confirmar Pedido"
5. Serás redirigido a Mercado Pago
6. Usa una tarjeta de prueba
7. Completa el pago
8. Volverás a tu sitio con el pago aprobado

---

## ❓ Verificar si está Configurado

Visita esta URL en tu navegador:
```
http://127.0.0.1:8000/test-mp-config/
```

Verás algo como:
```json
{
  "access_token_configurado": true,
  "public_key_configurado": true,
  "sdk_inicializado": true,
  "mensaje": "✅ Mercado Pago está correctamente configurado"
}
```

Si `access_token_configurado` es `false`, significa que falta configurar las credenciales.

---

## 🔍 Errores Comunes

### Error: "Mercado Pago no está configurado"
**Solución**: Configura las credenciales (ver Paso 2)

### Error: "Invalid credentials"
**Solución**: Verifica que copiaste bien las credenciales, sin espacios extras

### Error: "Currency not supported"
**Solución**: El código ya está configurado para Uruguay (UYU)

### Error al redirigir
**Solución**: Asegúrate de que el servidor esté corriendo en `http://127.0.0.1:8000/`

---

## 📞 ¿Necesitas Ayuda?

1. **Verifica la configuración**: http://127.0.0.1:8000/test-mp-config/
2. **Revisa los logs**: En la consola donde corre el servidor, busca mensajes que empiecen con "===" 
3. **Credenciales correctas**: Deben empezar con `TEST-` para pruebas

---

## 🎯 Checklist Rápido

- [ ] Tengo una cuenta en Mercado Pago Uruguay
- [ ] Creé una aplicación en el panel de desarrolladores
- [ ] Copié el Access Token (empieza con TEST-)
- [ ] Copié el Public Key (empieza con TEST-)
- [ ] Agregué las credenciales al archivo .env o settings.py
- [ ] Reinicié el servidor
- [ ] Probé http://127.0.0.1:8000/test-mp-config/
- [ ] Veo "✅ Mercado Pago está correctamente configurado"

Si completaste todo esto, ¡deberías poder hacer pagos de prueba! 🚀
