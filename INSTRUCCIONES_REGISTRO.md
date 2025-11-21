# 🎯 Guía de Registro de Usuarios - Superventas

## 📋 Cómo Registrar un Nuevo Usuario

### Paso 1: Acceder al Formulario de Registro
1. Abre tu navegador y ve a: `http://127.0.0.1:8000/`
2. Haz clic en el botón **"Iniciar Sesión"** en la esquina superior derecha
3. En la página de login, haz clic en **"Regístrate aquí"**
4. O accede directamente a: `http://127.0.0.1:8000/registro/`

### Paso 2: Completar el Formulario
Todos los campos marcados con **<span style="color: red;">*</span>** son obligatorios:

#### Información Personal
- **Nombre** *: Tu nombre real
- **Apellido** *: Tu apellido
- **Email** *: Debe ser un email válido (ej: usuario@email.com)
- **Usuario** *: Mínimo 4 caracteres, sin espacios

#### Contraseña Segura
La contraseña debe cumplir **TODOS** estos requisitos:

✅ **Mínimo 8 caracteres**
✅ **Al menos una letra MAYÚSCULA** (A-Z)
✅ **Al menos una letra minúscula** (a-z)
✅ **Al menos un número** (0-9)
✅ **Al menos un carácter especial** (!@#$%^&*)

**Ejemplos de contraseñas válidas:**
- `MiClave123!`
- `Segura@2024`
- `P@ssw0rd#`
- `Ventas*456`

**Ejemplos de contraseñas NO válidas:**
- `password` ❌ (no tiene mayúsculas, números ni caracteres especiales)
- `PASSWORD123` ❌ (no tiene minúsculas ni caracteres especiales)
- `Pass123` ❌ (menos de 8 caracteres)
- `MiPassword` ❌ (no tiene números ni caracteres especiales)

#### Confirmar Contraseña
- Escribe exactamente la misma contraseña
- El sistema te mostrará si coinciden ✓

#### Términos y Condiciones
- ✅ Debes aceptar los términos y condiciones

### Paso 3: Validación en Tiempo Real
El formulario te mostrará en tiempo real:

🔴 **Rojo con X** = Requisito NO cumplido
🟢 **Verde con ✓** = Requisito cumplido

**Barra de fuerza de contraseña:**
- 🔴 Roja (0-40%) = Débil
- 🟡 Amarilla (41-60%) = Media
- 🔵 Azul (61-80%) = Buena
- 🟢 Verde (81-100%) = ¡Segura!

### Paso 4: Enviar el Formulario
1. Revisa que todos los campos estén correctos
2. Asegúrate de que la barra de contraseña esté en verde
3. Verifica que ambas contraseñas coincidan
4. Haz clic en **"Registrarme"**

### Paso 5: Confirmar Registro Exitoso
✅ Si todo está correcto:
- Verás un mensaje: **"¡Cuenta creada exitosamente! Ya puedes iniciar sesión."**
- Serás redirigido a la página de login
- Podrás iniciar sesión con tu usuario y contraseña

❌ Si hay errores:
- El sistema te mostrará mensajes específicos
- Corrige los errores indicados
- Intenta registrarte nuevamente

---

## 🔐 Iniciar Sesión Después del Registro

1. En la página de login, ingresa:
   - **Usuario**: El nombre de usuario que elegiste
   - **Contraseña**: Tu contraseña segura
2. (Opcional) Marca "Recordarme" para mantener la sesión
3. Haz clic en **"Iniciar Sesión"**

✅ **Bienvenido**: Verás tu nombre en la esquina superior derecha
- Acceso al menú desplegable con tu nombre
- Opciones: Mi Perfil, Mis Pedidos, Favoritos, Cerrar Sesión

---

## 🎨 Características del Sistema de Registro

### Seguridad
- ✅ Contraseñas con hash seguro (Django auth)
- ✅ Validación robusta frontend y backend
- ✅ Usuarios únicos (no se permiten duplicados)
- ✅ Emails únicos en el sistema

### Experiencia de Usuario
- ✅ Validación en tiempo real
- ✅ Indicadores visuales claros
- ✅ Mensajes de error específicos
- ✅ Botones para mostrar/ocultar contraseña
- ✅ Diseño responsive (funciona en móviles)
- ✅ Colores verde/blanco/negro profesionales

### Navegación
- ✅ Breadcrumbs en todas las páginas
- ✅ Botón "Volver al Inicio" en catálogos
- ✅ Botón flotante "Volver Arriba"
- ✅ Enlaces directos al inicio desde el logo
- ✅ Botón "Seguir Comprando" en el carrito

---

## 🚀 Ejemplos de Usuarios de Prueba

Puedes crear usuarios con estas credenciales de ejemplo:

### Usuario 1
- **Nombre**: Juan
- **Apellido**: Pérez
- **Email**: juan.perez@email.com
- **Usuario**: juanp
- **Contraseña**: JuanP@2024

### Usuario 2
- **Nombre**: María
- **Apellido**: García
- **Email**: maria.garcia@email.com
- **Usuario**: mariag
- **Contraseña**: MariaG#123

### Usuario 3
- **Nombre**: Carlos
- **Apellido**: López
- **Email**: carlos.lopez@email.com
- **Usuario**: carlosl
- **Contraseña**: Carlos*456

---

## ⚠️ Errores Comunes y Soluciones

### "El nombre de usuario ya está en uso"
**Solución**: Elige un usuario diferente

### "El email ya está registrado"
**Solución**: Usa otro email o inicia sesión si ya tienes cuenta

### "Las contraseñas no coinciden"
**Solución**: Asegúrate de escribir la misma contraseña en ambos campos

### "La contraseña debe contener..."
**Solución**: Revisa los requisitos de seguridad y ajusta tu contraseña

### Campos marcados en rojo
**Solución**: Completa todos los campos obligatorios (marcados con *)

---

## 🛠️ Comandos Útiles del Sistema

### Iniciar el servidor
```bash
cd C:\Users\eltav\escritorio_local\superventas
.\entorno_virtual\Scripts\activate
python manage.py runserver
```

### Crear un superusuario (administrador)
```bash
python manage.py createsuperuser
```

### Acceder al panel de administración
- URL: `http://127.0.0.1:8000/admin/`
- Usa las credenciales del superusuario

---

## 📞 Soporte

Si tienes problemas:
1. Verifica que el servidor esté corriendo
2. Revisa la consola por errores
3. Asegúrate de estar usando un navegador moderno
4. Limpia la caché del navegador si algo no funciona

---

**¡Bienvenido a Superventas! 🎉**
