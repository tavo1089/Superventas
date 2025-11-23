# 📦 Panel de Administración de Pedidos

## ✅ Ya está configurado!

He mejorado el panel de administración de Django para que puedas gestionar todos los pedidos fácilmente.

## 🚀 Cómo acceder

### 1. Crear un usuario administrador (si no tienes uno)

Abre la terminal y ejecuta:

```bash
python manage.py createsuperuser
```

Te pedirá:
- **Username**: (elige un nombre, ejemplo: admin)
- **Email**: tu_email@gmail.com
- **Password**: (elige una contraseña segura)
- **Password (again)**: (repite la contraseña)

### 2. Acceder al panel

1. Asegúrate que el servidor esté corriendo:
   ```bash
   python manage.py runserver
   ```

2. Abre tu navegador y ve a:
   ```
   http://127.0.0.1:8000/admin
   ```

3. Inicia sesión con el usuario y contraseña que creaste

## 📋 Funcionalidades del Panel

### Vista de Lista de Pedidos

Verás todos los pedidos con:
- ✅ **Número de pedido** (clickeable)
- 👤 **Cliente**
- 📅 **Fecha y hora**
- 🏷️ **Estado** (con colores):
  - 🟡 Pendiente
  - 🔵 Procesando
  - 🔷 Enviado
  - 🟢 Entregado
  - 🔴 Cancelado
- 💳 **Estado de pago** (Pagado/Pendiente)
- 💰 **Total**
- 🌆 **Ciudad**

### Filtros disponibles:
- Por estado (pendiente, procesando, enviado, etc.)
- Por método de pago
- Por estado de pago
- Por fecha
- Por ciudad

### Búsqueda:
Puedes buscar por:
- Número de pedido
- Nombre de usuario
- Email
- Teléfono
- Ciudad
- Dirección

### Acciones Masivas:
Selecciona uno o varios pedidos y:
- 🔄 **Marcar como Procesando** (cuando empiezas a prepararlo)
- 📦 **Marcar como Enviado** (cuando lo envías)
- ✅ **Marcar como Entregado** (cuando llega al cliente)

## 📦 Ver Detalles de un Pedido

Haz click en el número de pedido para ver:

### 1. Información del Pedido
- Número único
- Cliente
- Fecha y hora
- Estado actual
- Total

### 2. Información de Pago
- Método de pago usado
- Estado (pagado/pendiente)

### 3. Datos de Envío (¡Formato especial para preparar envío!)
Verás un recuadro destacado con:
- 📦 Nombre del cliente
- ☎️ Teléfono (clickeable para llamar)
- 📧 Email (clickeable para enviar email)
- 📍 Dirección completa
- 🏙️ Ciudad
- 📮 Código postal

### 4. Productos del Pedido
Una tabla con:
- Nombre del producto
- Cantidad
- Precio unitario
- Descuento (si hay)
- Subtotal

### 5. Notas del Cliente
Si el cliente dejó notas adicionales (instrucciones especiales, horario preferido, etc.)

## 🎯 Flujo de Trabajo Recomendado

### 1. Cuando llega un pedido nuevo:
- Estado: **Pendiente**
- Acción: Revisa los productos y la dirección

### 2. Cuando empiezas a prepararlo:
- Cambia estado a: **Procesando**
- Prepara los productos
- Empaca el pedido

### 3. Cuando lo envías:
- Cambia estado a: **Enviado**
- El cliente puede ver que su pedido está en camino

### 4. Cuando el cliente lo recibe:
- Cambia estado a: **Entregado**
- Pedido completado

## 📊 Dashboard Rápido

En la página principal del admin verás:
- Total de pedidos
- Pedidos recientes
- Acceso rápido a todas las secciones

## 💡 Consejos

### Para preparar un envío:
1. Entra al pedido
2. Mira la sección "Datos de Envío" (tiene toda la info que necesitas)
3. Revisa los productos en la tabla inferior
4. Lee las notas del cliente (si hay)
5. Prepara el paquete
6. Marca como "Enviado"

### Para gestionar múltiples pedidos:
1. Filtra por estado "Pendiente"
2. Selecciona los que vas a preparar
3. Usa la acción "Marcar como Procesando"
4. Prepara todos juntos
5. Cuando los envíes, márcalos como "Enviado"

## 🔒 Seguridad

- Solo usuarios administradores pueden acceder
- Mantén tu contraseña segura
- No compartas el acceso al panel

## ❓ Troubleshooting

### "No tengo acceso al admin"
- Asegúrate de haber creado un superusuario con `python manage.py createsuperuser`
- Verifica que estés usando las credenciales correctas

### "No veo los pedidos"
- Verifica que haya pedidos creados en la base de datos
- Revisa los filtros activos (puede que estés filtrando algo)

### "No puedo cambiar el estado"
- Abre el pedido haciendo click en el número
- Cambia el estado en el campo correspondiente
- Guarda los cambios

## ✅ ¡Listo para usar!

Ya puedes gestionar todos tus pedidos desde:
**http://127.0.0.1:8000/admin**

Cada vez que un cliente haga un pedido, aparecerá automáticamente en el panel.
