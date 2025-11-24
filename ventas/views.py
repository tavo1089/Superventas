from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Favorito, Pedido, DetallePedido, Producto
from .forms import UserUpdateForm, PerfilUpdateForm, CambiarPasswordForm
import re
import uuid
from datetime import datetime
import json
import mercadopago
import stripe

# Create your views here.

def enviar_email_pedido(pedido):
    """Función para enviar email de confirmación de pedido"""
    try:
        # Email al cliente
        subject_cliente = f'Confirmación de Pedido #{pedido.numero_pedido}'
        
        # Crear contexto para el template
        context = {
            'pedido': pedido,
            'items': pedido.items.all(),
            'usuario': pedido.user,
        }
        
        # Mensaje para el cliente
        mensaje_cliente = f"""
        ¡Hola {pedido.user.get_full_name() or pedido.user.username}!
        
        Tu pedido #{pedido.numero_pedido} ha sido recibido exitosamente.
        
        DETALLES DEL PEDIDO:
        ---------------------
        Número de Pedido: {pedido.numero_pedido}
        Fecha: {pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M')}
        Total: ${pedido.total}
        Método de Pago: {pedido.get_metodo_pago_display()}
        Estado de Pago: {'✅ Pagado' if pedido.estado_pago else '⏳ Pendiente'}
        
        PRODUCTOS:
        ---------------------
        """
        
        for item in pedido.items.all():
            mensaje_cliente += f"\n- {item.producto_nombre} x{item.cantidad} - ${item.precio_unitario}"
            if item.descuento > 0:
                mensaje_cliente += f" ({item.descuento}% descuento)"
        
        mensaje_cliente += f"""
        
        DIRECCIÓN DE ENVÍO:
        ---------------------
        {pedido.direccion_envio}
        {pedido.ciudad}, {pedido.codigo_postal}
        Teléfono: {pedido.telefono}
        
        Te notificaremos cuando tu pedido sea enviado.
        
        ¡Gracias por tu compra!
        Superventas
        """
        
        # Enviar email al cliente
        send_mail(
            subject_cliente,
            mensaje_cliente,
            settings.DEFAULT_FROM_EMAIL,
            [pedido.user.email],
            fail_silently=True,
        )
        
        # Email al administrador si está configurado
        if settings.ADMIN_EMAIL:
            subject_admin = f'Nuevo Pedido #{pedido.numero_pedido} - {pedido.user.username}'
            
            mensaje_admin = f"""
            NUEVO PEDIDO RECIBIDO
            =====================
            
            Número de Pedido: {pedido.numero_pedido}
            Cliente: {pedido.user.get_full_name() or pedido.user.username}
            Email: {pedido.user.email}
            Teléfono: {pedido.telefono}
            Fecha: {pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M')}
            
            TOTAL: ${pedido.total}
            Método de Pago: {pedido.get_metodo_pago_display()}
            Estado de Pago: {'PAGADO' if pedido.estado_pago else 'PENDIENTE'}
            
            PRODUCTOS:
            ---------------------
            """
            
            for item in pedido.items.all():
                mensaje_admin += f"\n- {item.producto_nombre} x{item.cantidad} - ${item.precio_unitario}"
                if item.descuento > 0:
                    mensaje_admin += f" ({item.descuento}% descuento)"
            
            mensaje_admin += f"""
            
            DIRECCIÓN DE ENVÍO:
            ---------------------
            {pedido.direccion_envio}
            {pedido.ciudad}, {pedido.codigo_postal}
            
            NOTAS DEL CLIENTE:
            {pedido.notas or 'Sin notas'}
            """
            
            send_mail(
                subject_admin,
                mensaje_admin,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        
        return True
    except Exception as e:
        print(f"Error enviando email de pedido: {str(e)}")
        return False


def ordenar_productos(productos, orden):
    """Función helper para ordenar productos"""
    if orden == 'precio_asc':
        return sorted(productos, key=lambda x: x['precio'])
    elif orden == 'precio_desc':
        return sorted(productos, key=lambda x: x['precio'], reverse=True)
    elif orden == 'descuento':
        return sorted(productos, key=lambda x: x['descuento'], reverse=True)
    elif orden == 'nombre':
        return sorted(productos, key=lambda x: x['nombre'])
    return productos

def filtrar_productos(productos, buscar):
    """Función helper para filtrar productos por término de búsqueda"""
    if not buscar:
        return productos
    
    buscar = buscar.lower()
    return [p for p in productos if buscar in p['nombre'].lower()]

def index(request):
    """Vista principal de la aplicación"""
    context = {
        'titulo': 'Bienvenido a Superventas',
        'mensaje': 'Sistema de gestión de ventas'
    }
    return render(request, 'ventas/index.html', context)


def carrito(request):
    """Vista del carrito de compras"""
    return render(request, 'ventas/carrito.html')


def buscar(request):
    """Vista de búsqueda de productos"""
    query = request.GET.get('q', '')
    
    # Base de datos de todos los productos
    todos_productos = []
    
    # Productos de Belleza
    todos_productos.extend([
        {'nombre': 'Crema Facial Hidratante', 'precio': 25.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
        {'nombre': 'Set de Maquillaje Profesional', 'precio': 89.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
        {'nombre': 'Perfume Elegance 100ml', 'precio': 65.00, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
    ])
    
    # Productos de Tecnología
    todos_productos.extend([
        {'nombre': 'Smartphone Galaxy Pro', 'precio': 899.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
        {'nombre': 'Laptop Gaming RGB', 'precio': 1299.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
        {'nombre': 'Auriculares Bluetooth', 'precio': 159.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
    ])
    
    # Productos de Electrodomésticos
    todos_productos.extend([
        {'nombre': 'Refrigeradora Smart 500L', 'precio': 1499.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
        {'nombre': 'Lavadora Automática 18kg', 'precio': 899.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
        {'nombre': 'Auriculares Bluetooth Premium', 'precio': 399.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
    ])
    
    # Filtrar productos según la búsqueda
    resultados = []
    if query:
        query_lower = query.lower()
        resultados = [p for p in todos_productos if query_lower in p['nombre'].lower() or query_lower in p['categoria'].lower()]
    
    context = {
        'query': query,
        'productos': resultados,
        'total': len(resultados)
    }
    return render(request, 'ventas/buscar.html', context)


def categoria_belleza(request):
    """Vista de la categoría Belleza"""
    productos = [
        {'id': 1, 'nombre': 'Crema Facial Hidratante', 'precio': 25.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Set de Maquillaje Profesional', 'precio': 89.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Perfume Elegance 100ml', 'precio': 65.00, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Serum Anti-Edad', 'precio': 45.50, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Plancha de Cabello Profesional', 'precio': 75.00, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Kit de Cuidado de Uñas', 'precio': 35.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop'},
    ]
    
    # Obtener parámetros de búsqueda y ordenamiento
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    
    # Filtrar y ordenar productos
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    
    context = {
        'categoria': 'Belleza',
        'categoria_slug': 'belleza',
        'icono': 'bi-heart-fill',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_tecnologia(request):
    """Vista de la categoría Tecnología"""
    productos = [
        {'id': 1, 'nombre': 'Smartphone Galaxy Pro', 'precio': 899.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Laptop Gaming RGB', 'precio': 1299.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Tablet Pro 12"', 'precio': 599.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Auriculares Bluetooth Premium', 'precio': 399.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Smartwatch Ultra', 'precio': 399.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Teclado Mecánico RGB', 'precio': 129.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop'},
        {'id': 7, 'nombre': 'Mouse Gaming Pro', 'precio': 79.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop'},
        {'id': 8, 'nombre': 'Cámara Web 4K', 'precio': 149.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=400&h=300&fit=crop'},
    ]
    
    # Obtener parámetros de búsqueda y ordenamiento
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    
    # Filtrar y ordenar productos
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    
    context = {
        'categoria': 'Tecnología',
        'categoria_slug': 'tecnologia',
        'icono': 'bi-laptop',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_electrodomesticos(request):
    """Vista de la categoría Electrodomésticos"""
    productos = [
        {'id': 1, 'nombre': 'Refrigeradora Smart 500L', 'precio': 1499.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Lavadora Automática 18kg', 'precio': 899.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Microondas Digital', 'precio': 199.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Licuadora Pro 1200W', 'precio': 129.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Cafetera Express', 'precio': 179.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop'},
    ]
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    context = {
        'categoria': 'Electrodomésticos',
        'categoria_slug': 'electrodomesticos',
        'icono': 'bi-plug',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_ferreteria(request):
    """Vista de la categoría Ferretería y Construcción"""
    productos = [
        {'id': 1, 'nombre': 'Taladro Inalámbrico 20V', 'precio': 149.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Set de Herramientas 120 Piezas', 'precio': 89.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Sierra Circular Profesional', 'precio': 199.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Escalera Telescópica 5m', 'precio': 299.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1513467535987-fd81bc7d62f8?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Compresor de Aire', 'precio': 249.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Nivel Láser Digital', 'precio': 129.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop'},
    ]
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    context = {
        'categoria': 'Ferretería y Construcción',
        'categoria_slug': 'ferreteria',
        'icono': 'bi-tools',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_bebe(request):
    """Vista de la categoría Bebé y Niños"""
    productos = [
        {'id': 1, 'nombre': 'Coche para Bebé Premium', 'precio': 349.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Cuna Convertible', 'precio': 299.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Monitor de Bebé con Cámara', 'precio': 129.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Set de Alimentación', 'precio': 45.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Juguete Educativo Musical', 'precio': 59.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1587818541473-f2e71229046f?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Pañalera de Viaje', 'precio': 79.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=300&fit=crop'},
    ]
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    context = {
        'categoria': 'Bebé y Niños',
        'categoria_slug': 'bebe',
        'icono': 'bi-balloon-heart',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_aire_libre(request):
    """Vista de la categoría Aire Libre"""
    productos = [
        {'id': 1, 'nombre': 'Bicicleta de Montaña Pro', 'precio': 599.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1541625602330-2277a4c46182?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Carpa Camping 6 Personas', 'precio': 249.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Parrilla Portátil a Gas', 'precio': 179.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Set de Pesca Completo', 'precio': 129.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1502139214982-d0ad755818d8?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Mochila Trekking 50L', 'precio': 99.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Kayak Inflable 2 Personas', 'precio': 399.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop'},
    ]
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    context = {
        'categoria': 'Aire Libre',
        'categoria_slug': 'aire_libre',
        'icono': 'bi-tree',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_entretenimiento(request):
    """Vista de la categoría Entretenimiento"""
    productos = [
        {'id': 1, 'nombre': 'Consola Gaming Next Gen', 'precio': 499.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1486401899868-0e435ed85128?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Smart TV 55" 4K', 'precio': 699.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Barra de Sonido Dolby', 'precio': 299.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Drone con Cámara 4K', 'precio': 449.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Guitarra Eléctrica', 'precio': 379.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Set de Juegos de Mesa', 'precio': 89.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop'},
    ]
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    context = {
        'categoria': 'Entretenimiento',
        'categoria_slug': 'entretenimiento',
        'icono': 'bi-controller',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def categoria_salud(request):
    """Vista de la categoría Salud y Bienestar"""
    productos = [
        {'id': 1, 'nombre': 'Caminadora Eléctrica Pro', 'precio': 899.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400&h=300&fit=crop'},
        {'id': 2, 'nombre': 'Set de Pesas Ajustables', 'precio': 199.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop'},
        {'id': 3, 'nombre': 'Bicicleta Estática Smart', 'precio': 449.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400&h=300&fit=crop'},
        {'id': 4, 'nombre': 'Mat de Yoga Premium', 'precio': 49.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400&h=300&fit=crop'},
        {'id': 5, 'nombre': 'Masajeador Eléctrico', 'precio': 129.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop'},
        {'id': 6, 'nombre': 'Monitor de Presión Digital', 'precio': 69.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=300&fit=crop'},
    ]
    buscar = request.GET.get('buscar', '')
    orden = request.GET.get('orden', '')
    productos = filtrar_productos(productos, buscar)
    productos = ordenar_productos(productos, orden)
    context = {
        'categoria': 'Salud y Bienestar',
        'categoria_slug': 'salud',
        'icono': 'bi-heart-pulse',
        'productos': productos,
        'orden': orden,
        'buscar': buscar
    }
    return render(request, 'ventas/catalogo.html', context)


def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('ventas:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'ventas:index')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'ventas/login.html')


def registro_view(request):
    """Vista de registro de usuarios"""
    if request.user.is_authenticated:
        return redirect('ventas:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validaciones básicas
        if not all([username, email, password1, password2, first_name, last_name]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'ventas/registro.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return render(request, 'ventas/registro.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'ventas/registro.html')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'ventas/registro.html')
        
        # Validación de contraseña segura
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'ventas/registro.html')
        
        if not re.search(r'[A-Z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
            return render(request, 'ventas/registro.html')
        
        if not re.search(r'[a-z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra minúscula')
            return render(request, 'ventas/registro.html')
        
        if not re.search(r'[0-9]', password1):
            messages.error(request, 'La contraseña debe contener al menos un número')
            return render(request, 'ventas/registro.html')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, 'La contraseña debe contener al menos un carácter especial (!@#$%^&*)')
            return render(request, 'ventas/registro.html')
        
        # Validar longitud del username
        if len(username) < 4:
            messages.error(request, 'El nombre de usuario debe tener al menos 4 caracteres')
            return render(request, 'ventas/registro.html')
        
        # Crear usuario
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, '¡Cuenta creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('ventas:login')
        except Exception as e:
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
    
    return render(request, 'ventas/registro.html')


def logout_view(request):
    """Vista de cierre de sesión"""
    auth_logout(request)
    messages.success(request, '¡Hasta pronto! Has cerrado sesión correctamente.')
    return redirect('ventas:index')


@login_required
def perfil_view(request):
    """Vista del perfil de usuario"""
    return render(request, 'ventas/perfil.html')


@login_required
def editar_perfil_view(request):
    """Vista para editar el perfil de usuario"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado correctamente!')
            return redirect('ventas:perfil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilUpdateForm(instance=request.user.perfil)
    
    context = {
        'user_form': user_form,
        'perfil_form': perfil_form
    }
    return render(request, 'ventas/editar_perfil.html', context)


@login_required
def cambiar_password_view(request):
    """Vista para cambiar la contraseña"""
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener la sesión activa
            messages.success(request, '¡Tu contraseña ha sido cambiada exitosamente!')
            return redirect('ventas:perfil')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = CambiarPasswordForm(request.user)
    
    return render(request, 'ventas/cambiar_password.html', {'form': form})


def detalle_producto(request, categoria, producto_id):
    """Vista de detalle de un producto específico"""
    # Base de datos de productos con información detallada
    productos_db = {
        'belleza': [
            {
                'id': 1,
                'nombre': 'Crema Facial Hidratante',
                'precio': 25.99,
                'descuento': 20,
                'imagen': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop',
                'categoria': 'Belleza',
                'icono': 'bi-heart-fill',
                'sku': 'BEL-001',
                'descripcion': 'Crema facial hidratante de día con protección solar SPF 30. Ideal para todo tipo de piel.',
                'descripcion_larga': 'Nuestra crema facial hidratante combina ingredientes naturales con tecnología avanzada para proporcionar una hidratación profunda y duradera. Enriquecida con ácido hialurónico, vitamina E y extractos botánicos, esta crema penetra en las capas profundas de la piel, dejándola suave, tersa y radiante. La fórmula ligera se absorbe rápidamente sin dejar residuos grasos.',
                'caracteristicas': [
                    'Hidratación profunda por 24 horas',
                    'Protección solar SPF 30',
                    'No comedogénico',
                    'Apto para pieles sensibles',
                    'Libre de parabenos'
                ],
                'beneficios': [
                    'Mejora la elasticidad de la piel',
                    'Reduce líneas de expresión',
                    'Protege contra rayos UV',
                    'Piel más luminosa y saludable'
                ],
                'especificaciones': {
                    'Contenido': '50 ml',
                    'Tipo de piel': 'Todo tipo',
                    'Ingrediente principal': 'Ácido Hialurónico',
                    'SPF': '30',
                    'Origen': 'Francia',
                    'Dermatológicamente probado': 'Sí'
                },
                'resenas': [
                    {'usuario': 'María G.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '15 Nov 2025', 'comentario': '¡Excelente producto! Mi piel se siente increíble, muy hidratada y suave.'},
                    {'usuario': 'Laura P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '10 Nov 2025', 'comentario': 'La mejor crema que he probado. Se absorbe rápido y no deja la piel grasosa.'},
                    {'usuario': 'Ana R.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '5 Nov 2025', 'comentario': 'Muy buena, aunque me gustaría que el envase fuera más grande.'}
                ]
            },
            {
                'id': 2,
                'nombre': 'Set de Maquillaje Profesional',
                'precio': 89.99,
                'descuento': 15,
                'imagen': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=300&fit=crop',
                'categoria': 'Belleza',
                'icono': 'bi-heart-fill',
                'sku': 'BEL-002',
                'descripcion': 'Set completo de maquillaje profesional con paleta de 120 colores, brochas y estuche.',
                'descripcion_larga': 'Este set de maquillaje profesional incluye todo lo que necesitas para crear looks espectaculares. Con 120 tonos cuidadosamente seleccionados, desde naturales hasta vibrantes, podrás explorar infinitas posibilidades. Las brochas de alta calidad aseguran una aplicación perfecta.',
                'caracteristicas': [
                    '120 tonos de sombras',
                    '10 brochas profesionales',
                    'Paleta de contorno y rubor',
                    'Estuche organizador',
                    'Pigmentación intensa'
                ],
                'beneficios': [
                    'Maquillaje de larga duración',
                    'Colores altamente pigmentados',
                    'Fácil de difuminar',
                    'No irrita los ojos'
                ],
                'especificaciones': {
                    'Contenido': '120 sombras + 10 brochas',
                    'Tipo': 'Profesional',
                    'Acabado': 'Mate y shimmer',
                    'Libre de crueldad': 'Sí',
                    'Vegano': 'Sí',
                    'Garantía': '1 año'
                },
                'resenas': [
                    {'usuario': 'Sofia M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Increíble set! Los colores son hermosos y muy pigmentados.'},
                    {'usuario': 'Carmen L.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '12 Nov 2025', 'comentario': 'Perfecta relación calidad-precio. Las brochas son de excelente calidad.'}
                ]
            },
            {
                'id': 3,
                'nombre': 'Perfume Elegance 100ml',
                'precio': 65.00,
                'descuento': 25,
                'imagen': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=300&fit=crop',
                'categoria': 'Belleza',
                'icono': 'bi-heart-fill',
                'sku': 'BEL-003',
                'descripcion': 'Perfume floral con notas de jazmín, rosa y vainilla. Elegancia en cada gota.',
                'descripcion_larga': 'Perfume Elegance es una fragancia sofisticada que combina notas florales con toques dulces y sensuales. Las notas de salida de bergamota y mandarina dan paso a un corazón de jazmín y rosa, finalizando con una base cálida de vainilla, ámbar y almizcle. Perfecto para ocasiones especiales.',
                'caracteristicas': [
                    'Fragancia floral oriental',
                    'Duración de 8-10 horas',
                    'Frasco elegante de vidrio',
                    'Atomizador de precisión',
                    '100ml de contenido'
                ],
                'beneficios': [
                    'Aroma duradero',
                    'Elegante y sofisticado',
                    'Ideal para día y noche',
                    'Notas equilibradas'
                ],
                'especificaciones': {
                    'Contenido': '100 ml',
                    'Tipo': 'Eau de Parfum',
                    'Familia olfativa': 'Floral Oriental',
                    'Concentración': '15-20%',
                    'Origen': 'Francia',
                    'Género': 'Femenino'
                },
                'resenas': [
                    {'usuario': 'Valentina S.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Huele increíble y dura todo el día. Me encanta!'},
                    {'usuario': 'Isabella R.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '11 Nov 2025', 'comentario': 'Muy buen perfume, el aroma es delicado y elegante.'}
                ]
            },
            {
                'id': 4,
                'nombre': 'Serum Anti-Edad',
                'precio': 45.50,
                'descuento': 10,
                'imagen': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=300&fit=crop',
                'categoria': 'Belleza',
                'icono': 'bi-heart-fill',
                'sku': 'BEL-004',
                'descripcion': 'Serum concentrado con retinol y vitamina C para combatir los signos del envejecimiento.',
                'descripcion_larga': 'Nuestro Serum Anti-Edad es una fórmula avanzada que combina retinol, vitamina C y péptidos para reducir visiblemente las arrugas, líneas de expresión y manchas. Su textura ligera se absorbe rápidamente, proporcionando resultados visibles en pocas semanas.',
                'caracteristicas': [
                    'Retinol 1% + Vitamina C',
                    'Reduce arrugas profundas',
                    'Ilumina y unifica el tono',
                    'Textura ligera no grasa',
                    'Uso diario día/noche'
                ],
                'beneficios': [
                    'Piel más firme y tersa',
                    'Reducción de manchas',
                    'Estimula colágeno',
                    'Resultados en 4 semanas'
                ],
                'especificaciones': {
                    'Contenido': '30 ml',
                    'Ingredientes activos': 'Retinol 1%, Vitamina C 10%',
                    'Tipo de piel': 'Todo tipo (mayores 25 años)',
                    'Aplicación': 'Día y noche',
                    'Origen': 'Suiza',
                    'Dermatológicamente probado': 'Sí'
                },
                'resenas': [
                    {'usuario': 'Patricia M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '16 Nov 2025', 'comentario': 'Resultados increíbles! Mi piel se ve más joven y radiante.'},
                    {'usuario': 'Elena V.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '9 Nov 2025', 'comentario': 'El mejor serum que he usado. Vale cada centavo.'}
                ]
            },
            {
                'id': 5,
                'nombre': 'Plancha de Cabello Profesional',
                'precio': 75.00,
                'descuento': 30,
                'imagen': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400&h=300&fit=crop',
                'categoria': 'Belleza',
                'icono': 'bi-heart-fill',
                'sku': 'BEL-005',
                'descripcion': 'Plancha de cabello profesional con placas de cerámica turmalina y control de temperatura digital.',
                'descripcion_larga': 'Esta plancha profesional cuenta con placas flotantes de cerámica turmalina que distribuyen el calor uniformemente, protegiendo tu cabello. El control digital de temperatura permite ajustes de 150°C a 230°C, adaptándose a todo tipo de cabello. Calentamiento rápido en 30 segundos.',
                'caracteristicas': [
                    'Placas cerámica turmalina',
                    'Temperatura 150-230°C',
                    'Calentamiento en 30 segundos',
                    'Apagado automático 60 min',
                    'Cable giratorio 360°',
                    'Tecnología iónica'
                ],
                'beneficios': [
                    'Protege el cabello',
                    'Resultados profesionales',
                    'Brillo duradero',
                    'Sin frizz'
                ],
                'especificaciones': {
                    'Potencia': '45W',
                    'Temperatura máxima': '230°C',
                    'Tipo de placas': 'Cerámica Turmalina',
                    'Ancho de placas': '2.5 cm',
                    'Voltaje': '110-240V',
                    'Garantía': '2 años'
                },
                'resenas': [
                    {'usuario': 'Gabriela T.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente plancha! Deja el cabello súper liso y brillante.'},
                    {'usuario': 'Camila D.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '13 Nov 2025', 'comentario': 'Muy buena, calienta rápido y es fácil de usar.'}
                ]
            },
            {
                'id': 6,
                'nombre': 'Kit de Cuidado de Uñas',
                'precio': 35.99,
                'descuento': 0,
                'imagen': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop',
                'categoria': 'Belleza',
                'icono': 'bi-heart-fill',
                'sku': 'BEL-006',
                'descripcion': 'Kit completo profesional para manicure y pedicure con 15 piezas de acero inoxidable.',
                'descripcion_larga': 'Kit profesional de cuidado de uñas que incluye todo lo necesario para una manicure y pedicure perfecta. Fabricado en acero inoxidable quirúrgico de alta calidad, resistente a la oxidación. Incluye estuche de cuero sintético para almacenamiento y transporte.',
                'caracteristicas': [
                    '15 piezas profesionales',
                    'Acero inoxidable quirúrgico',
                    'Cortauñas, tijeras, limas',
                    'Removedor de cutículas',
                    'Estuche de cuero elegante',
                    'Resistente a oxidación'
                ],
                'beneficios': [
                    'Calidad profesional',
                    'Duradero y resistente',
                    'Fácil de transportar',
                    'Set completo'
                ],
                'especificaciones': {
                    'Material': 'Acero inoxidable 420',
                    'Número de piezas': '15',
                    'Incluye estuche': 'Sí',
                    'Color': 'Plateado',
                    'Peso': '250 g',
                    'Garantía': '1 año'
                },
                'resenas': [
                    {'usuario': 'Andrea P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '15 Nov 2025', 'comentario': 'Excelente kit, muy completo y de buena calidad.'},
                    {'usuario': 'Monica L.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '10 Nov 2025', 'comentario': 'Perfecto para llevar de viaje. Todo muy bien organizado.'}
                ]
            }
        ],
        'tecnologia': [
            {
                'id': 1,
                'nombre': 'Smartphone Galaxy Pro',
                'precio': 899.99,
                'descuento': 15,
                'imagen': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-001',
                'descripcion': 'Smartphone de última generación con cámara de 108MP, procesador octa-core y pantalla AMOLED 6.7".',
                'descripcion_larga': 'El Smartphone Galaxy Pro redefine la experiencia móvil con su potente procesador octa-core de última generación, 12GB de RAM y 256GB de almacenamiento interno expandible. Su pantalla AMOLED de 6.7" con tasa de refresco de 120Hz ofrece colores vibrantes y fluidez excepcional. El sistema de triple cámara con sensor principal de 108MP captura fotos y videos con calidad profesional.',
                'caracteristicas': [
                    'Pantalla AMOLED 6.7" 120Hz',
                    'Cámara triple 108MP + 12MP + 5MP',
                    'Procesador Octa-core 3.2GHz',
                    '12GB RAM + 256GB ROM',
                    'Batería 5000mAh carga rápida 65W',
                    '5G + WiFi 6 + Bluetooth 5.2'
                ],
                'beneficios': [
                    'Rendimiento ultra rápido',
                    'Fotos de calidad profesional',
                    'Batería de larga duración',
                    'Pantalla inmersiva'
                ],
                'especificaciones': {
                    'Sistema Operativo': 'Android 14',
                    'Procesador': 'Snapdragon 8 Gen 3',
                    'RAM': '12 GB',
                    'Almacenamiento': '256 GB',
                    'Pantalla': '6.7" AMOLED 120Hz',
                    'Cámara Principal': '108 MP',
                    'Batería': '5000 mAh',
                    'Conectividad': '5G',
                    'Color': 'Negro Galaxia',
                    'Peso': '195 g'
                },
                'resenas': [
                    {'usuario': 'Carlos R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'El mejor smartphone que he tenido. La cámara es impresionante!'},
                    {'usuario': 'Diego F.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '14 Nov 2025', 'comentario': 'Excelente rendimiento, batería dura todo el día con uso intenso.'},
                    {'usuario': 'Roberto M.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '8 Nov 2025', 'comentario': 'Muy buen teléfono, solo que es un poco grande para mi mano.'}
                ]
            },
            {
                'id': 2,
                'nombre': 'Laptop Gaming RGB',
                'precio': 1299.99,
                'descuento': 20,
                'imagen': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-002',
                'descripcion': 'Laptop gaming potente con RTX 4060, Intel Core i7, 16GB RAM y SSD 512GB. Teclado RGB.',
                'descripcion_larga': 'Esta laptop gaming está diseñada para jugadores exigentes y creadores de contenido. Equipada con tarjeta gráfica NVIDIA RTX 4060 de 8GB, procesador Intel Core i7 de 13ª generación y 16GB de RAM DDR5, ofrece un rendimiento excepcional. La pantalla Full HD de 15.6" con tasa de refresco de 144Hz garantiza una experiencia visual fluida. El teclado retroiluminado RGB y el sistema de enfriamiento avanzado completan este equipo profesional.',
                'caracteristicas': [
                    'Intel Core i7-13700H (14 núcleos)',
                    'NVIDIA RTX 4060 8GB GDDR6',
                    '16GB RAM DDR5 4800MHz',
                    'SSD NVMe 512GB',
                    'Pantalla 15.6" FHD 144Hz',
                    'Teclado RGB retroiluminado',
                    'WiFi 6E + Bluetooth 5.3'
                ],
                'beneficios': [
                    'Juega en ultra calidad',
                    'Multitarea sin límites',
                    'Diseño gaming premium',
                    'Sistema de enfriamiento eficiente'
                ],
                'especificaciones': {
                    'Procesador': 'Intel Core i7-13700H',
                    'Tarjeta Gráfica': 'NVIDIA RTX 4060 8GB',
                    'RAM': '16 GB DDR5',
                    'Almacenamiento': '512 GB SSD NVMe',
                    'Pantalla': '15.6" FHD 144Hz IPS',
                    'Sistema Operativo': 'Windows 11 Home',
                    'Batería': '90Wh',
                    'Peso': '2.3 kg',
                    'Garantía': '2 años'
                },
                'resenas': [
                    {'usuario': 'Javier M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Bestial para gaming! Corre todo en ultra sin problemas.'},
                    {'usuario': 'Fernando R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '15 Nov 2025', 'comentario': 'Excelente laptop, la pantalla de 144Hz es una maravilla.'},
                    {'usuario': 'Lucas P.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '10 Nov 2025', 'comentario': 'Muy buena, solo que se calienta un poco en juegos pesados.'}
                ]
            },
            {
                'id': 3,
                'nombre': 'Tablet Pro 12"',
                'precio': 599.99,
                'descuento': 10,
                'imagen': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-003',
                'descripcion': 'Tablet profesional de 12 pulgadas con stylus incluido, 8GB RAM y 256GB almacenamiento.',
                'descripcion_larga': 'La Tablet Pro 12" es perfecta para productividad y creatividad. Su pantalla OLED de 12.4" ofrece colores vibrantes y negros profundos. Incluye stylus de precisión con 4096 niveles de presión, ideal para diseño y toma de notas. El procesador de 8 núcleos y 8GB de RAM garantizan fluidez en multitarea.',
                'caracteristicas': [
                    'Pantalla OLED 12.4" 2K',
                    'Procesador Octa-core 2.8GHz',
                    '8GB RAM + 256GB ROM',
                    'Stylus incluido (4096 niveles)',
                    'Cámara dual 13MP + 8MP',
                    'Batería 10,000mAh',
                    'Carga rápida 45W'
                ],
                'beneficios': [
                    'Ideal para diseño y dibujo',
                    'Pantalla de alta calidad',
                    'Batería de larga duración',
                    'Perfecta para estudiar'
                ],
                'especificaciones': {
                    'Pantalla': '12.4" OLED 2K',
                    'Procesador': 'Snapdragon 8 Gen 2',
                    'RAM': '8 GB',
                    'Almacenamiento': '256 GB',
                    'Cámara': '13MP + 8MP',
                    'Batería': '10,000 mAh',
                    'Sistema': 'Android 14',
                    'Peso': '565 g',
                    'Incluye': 'Stylus + Funda'
                },
                'resenas': [
                    {'usuario': 'Daniela S.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Perfecta para tomar notas en la universidad. El stylus es excelente.'},
                    {'usuario': 'Miguel A.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '12 Nov 2025', 'comentario': 'Gran tablet para diseño gráfico. La pantalla es espectacular.'}
                ]
            },
            {
                'id': 4,
                'nombre': 'Auriculares Bluetooth',
                'precio': 159.99,
                'descuento': 25,
                'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-004',
                'descripcion': 'Auriculares inalámbricos premium con cancelación de ruido activa y 30 horas de batería.',
                'descripcion_larga': 'Auriculares Bluetooth de alta gama con cancelación de ruido activa (ANC) que elimina hasta el 95% del ruido ambiental. Drivers de 40mm ofrecen audio Hi-Res con graves profundos y agudos cristalinos. Comodidad excepcional con almohadillas de espuma memory foam y diadema ajustable. Hasta 30 horas de reproducción con ANC activado.',
                'caracteristicas': [
                    'Cancelación de ruido ANC',
                    'Audio Hi-Res certificado',
                    'Batería 30 horas',
                    'Bluetooth 5.3 multipoint',
                    'Carga rápida (10min = 5h)',
                    'Micrófono con AI para llamadas',
                    'Plegables con estuche'
                ],
                'beneficios': [
                    'Sonido premium',
                    'Máximo confort',
                    'Ideal para viajes',
                    'Llamadas cristalinas'
                ],
                'especificaciones': {
                    'Tipo': 'Over-ear cerrados',
                    'Drivers': '40mm dinámicos',
                    'Respuesta frecuencia': '20Hz - 40kHz',
                    'Bluetooth': '5.3',
                    'Autonomía': '30h con ANC',
                    'Carga': 'USB-C rápida',
                    'Peso': '250 g',
                    'Certificación': 'Hi-Res Audio'
                },
                'resenas': [
                    {'usuario': 'Andrés L.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'El mejor sonido que he escuchado en auriculares inalámbricos!'},
                    {'usuario': 'Pablo G.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '14 Nov 2025', 'comentario': 'La cancelación de ruido es increíble. Perfectos para el avión.'},
                    {'usuario': 'Martín K.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '9 Nov 2025', 'comentario': 'Súper cómodos y la batería dura muchísimo.'}
                ]
            },
            {
                'id': 5,
                'nombre': 'Smartwatch Ultra',
                'precio': 399.99,
                'descuento': 30,
                'imagen': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-005',
                'descripcion': 'Smartwatch deportivo con GPS, monitor cardíaco, SpO2 y más de 100 modos deportivos.',
                'descripcion_larga': 'El Smartwatch Ultra es el compañero perfecto para tu estilo de vida activo. Con pantalla AMOLED siempre encendida de 1.43", GPS dual band para máxima precisión, monitoreo continuo de frecuencia cardíaca, SpO2 y sueño. Resistente al agua 5ATM y batería de hasta 14 días. Incluye más de 100 modos deportivos y métricas avanzadas.',
                'caracteristicas': [
                    'Pantalla AMOLED 1.43" Always-On',
                    'GPS dual band L1+L5',
                    'Monitor cardíaco 24/7',
                    'SpO2 y monitoreo de sueño',
                    'Resistencia agua 5ATM',
                    'Batería 14 días',
                    '100+ modos deportivos',
                    'Llamadas Bluetooth'
                ],
                'beneficios': [
                    'Seguimiento completo de salud',
                    'GPS ultra preciso',
                    'Batería de larga duración',
                    'Resistente y deportivo'
                ],
                'especificaciones': {
                    'Pantalla': '1.43" AMOLED 466x466',
                    'GPS': 'Dual Band L1+L5',
                    'Sensores': 'FC, SpO2, acelerómetro, giroscopio',
                    'Batería': '470mAh (14 días)',
                    'Resistencia': '5ATM (50m)',
                    'Conectividad': 'Bluetooth 5.3',
                    'Compatible': 'iOS/Android',
                    'Peso': '62 g'
                },
                'resenas': [
                    {'usuario': 'Ricardo S.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente reloj! El GPS es muy preciso en mis carreras.'},
                    {'usuario': 'Sebastián V.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '13 Nov 2025', 'comentario': 'La batería dura realmente 14 días. Muy completo.'},
                    {'usuario': 'Tomás B.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '8 Nov 2025', 'comentario': 'Muy buen smartwatch, aunque la app podría mejorar.'}
                ]
            },
            {
                'id': 6,
                'nombre': 'Teclado Mecánico RGB',
                'precio': 129.99,
                'descuento': 15,
                'imagen': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-006',
                'descripcion': 'Teclado mecánico gaming con switches azules, retroiluminación RGB y reposamuñecas.',
                'descripcion_larga': 'Teclado mecánico premium para gaming y productividad. Switches mecánicos azules con 50 millones de pulsaciones de vida útil, ofrecen feedback táctil y sonoro perfecto. Retroiluminación RGB personalizable por tecla con múltiples efectos. Construcción robusta de aluminio, anti-ghosting completo y teclas programables.',
                'caracteristicas': [
                    'Switches mecánicos azules',
                    'RGB por tecla personalizable',
                    'Anti-ghosting NKRO',
                    'Marco de aluminio',
                    'Teclas programables',
                    'Reposamuñecas incluido',
                    'Cable USB-C trenzado',
                    'Software de configuración'
                ],
                'beneficios': [
                    'Respuesta ultra rápida',
                    'Durabilidad excepcional',
                    'Comodidad en largas sesiones',
                    'Personalización total'
                ],
                'especificaciones': {
                    'Tipo': 'Mecánico 100%',
                    'Switches': 'Mecánicos azules',
                    'Vida útil': '50 millones pulsaciones',
                    'Retroiluminación': 'RGB por tecla',
                    'Conexión': 'USB-C',
                    'Anti-ghosting': 'NKRO',
                    'Material': 'Aluminio + ABS',
                    'Peso': '1.1 kg'
                },
                'resenas': [
                    {'usuario': 'David H.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Excelente teclado! Los switches suenan y se sienten increíbles.'},
                    {'usuario': 'Nicolás P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '12 Nov 2025', 'comentario': 'Muy buena construcción y las luces RGB son espectaculares.'}
                ]
            },
            {
                'id': 7,
                'nombre': 'Mouse Gaming Pro',
                'precio': 79.99,
                'descuento': 20,
                'imagen': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-007',
                'descripcion': 'Mouse gaming inalámbrico con sensor 25,000 DPI, 8 botones programables y RGB.',
                'descripcion_larga': 'Mouse gaming profesional con sensor óptico de 25,000 DPI ajustable, perfecto para FPS y MOBA. Diseño ergonómico ambidiestro con 8 botones totalmente programables. Conexión inalámbrica de baja latencia 2.4GHz o Bluetooth 5.0. Batería recargable de hasta 120 horas. Iluminación RGB personalizable con 16.8 millones de colores.',
                'caracteristicas': [
                    'Sensor óptico 25,000 DPI',
                    'Conexión dual (2.4GHz + BT 5.0)',
                    '8 botones programables',
                    'Batería 120 horas',
                    'RGB 16.8M colores',
                    'Peso ajustable 75-95g',
                    'Pies de PTFE',
                    'Polling rate 1000Hz'
                ],
                'beneficios': [
                    'Precisión extrema',
                    'Respuesta instantánea',
                    'Autonomía excepcional',
                    'Personalización total'
                ],
                'especificaciones': {
                    'Sensor': 'Óptico 25,000 DPI',
                    'Botones': '8 programables',
                    'Conectividad': '2.4GHz + Bluetooth 5.0',
                    'Batería': '800mAh (120h)',
                    'Polling rate': '1000Hz',
                    'Aceleración': '50G',
                    'Peso': '75-95 g ajustable',
                    'Garantía': '2 años'
                },
                'resenas': [
                    {'usuario': 'Alejandro F.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'El mejor mouse que he tenido! Precisión perfecta para FPS.'},
                    {'usuario': 'Maximiliano R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '14 Nov 2025', 'comentario': 'Ergonomía excelente y la batería dura muchísimo.'}
                ]
            },
            {
                'id': 8,
                'nombre': 'Cámara Web 4K',
                'precio': 149.99,
                'descuento': 0,
                'imagen': 'https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=400&h=300&fit=crop',
                'categoria': 'Tecnología',
                'icono': 'bi-laptop',
                'sku': 'TEC-008',
                'descripcion': 'Cámara web 4K con autofocus, corrección de luz y micrófono dual con cancelación de ruido.',
                'descripcion_larga': 'Cámara web profesional 4K Ultra HD perfecta para streaming, videoconferencias y creación de contenido. Sensor Sony de 8MP con autofocus rápido y preciso. Corrección automática de luz HDR para verse siempre bien iluminado. Micrófono estéreo dual con cancelación de ruido AI. Campo de visión ajustable 65°-90°.',
                'caracteristicas': [
                    'Resolución 4K 30fps',
                    'Sensor Sony 8MP',
                    'Autofocus rápido',
                    'HDR y corrección de luz',
                    'Micrófonos duales con AI',
                    'Campo visión 65-90°',
                    'Trípode incluido',
                    'Compatible USB 3.0'
                ],
                'beneficios': [
                    'Imagen profesional',
                    'Audio cristalino',
                    'Plug & play',
                    'Ideal para streaming'
                ],
                'especificaciones': {
                    'Resolución': '4K 30fps / 1080p 60fps',
                    'Sensor': 'Sony 8MP',
                    'Enfoque': 'Autofocus',
                    'Campo de visión': '65-90° ajustable',
                    'Micrófono': 'Dual estéreo con AI',
                    'Conexión': 'USB 3.0',
                    'Compatible': 'Windows/Mac/ChromeOS',
                    'Garantía': '2 años'
                },
                'resenas': [
                    {'usuario': 'Santiago M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Perfecta para mis reuniones de trabajo. Imagen espectacular!'},
                    {'usuario': 'Gabriel T.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '13 Nov 2025', 'comentario': 'Excelente cámara para streaming, el autofocus funciona muy bien.'}
                ]
            }
        ],
        'electrodomesticos': [
            {
                'id': 1, 'nombre': 'Refrigeradora Smart 500L', 'precio': 1499.99, 'descuento': 10,
                'imagen': 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400&h=300&fit=crop',
                'categoria': 'Electrodomésticos', 'icono': 'bi-plug', 'sku': 'ELEC-001',
                'descripcion': 'Refrigeradora inteligente de 500L con dispensador de agua y hielo, control por app.',
                'descripcion_larga': 'Refrigeradora Smart con tecnología No Frost, compresor inverter y panel de control táctil. Sistema de enfriamiento dual para refrigerador y congelador independientes. Dispensador externo de agua filtrada y hielo. Control remoto vía WiFi con app móvil. Iluminación LED interior y estantes ajustables de vidrio templado. Eficiencia energética A+++.',
                'caracteristicas': ['500L capacidad total', 'No Frost dual', 'Compresor Inverter', 'WiFi + control app', 'Dispensador agua/hielo', 'Eficiencia A+++', 'Filtro de agua'],
                'beneficios': ['Ahorro de energía 40%', 'Alimentos frescos más tiempo', 'Control remoto', 'Silencioso'],
                'especificaciones': {'Capacidad': '500L', 'Tipo': 'Side by Side', 'Tecnología': 'No Frost Inverter', 'Dispensador': 'Agua y hielo', 'Conectividad': 'WiFi', 'Eficiencia': 'A+++', 'Dimensiones': '90x70x180 cm', 'Garantía': '3 años'},
                'resenas': [{'usuario': 'Julia M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente refrigeradora! Muy espaciosa y silenciosa.'}]
            },
            {
                'id': 2, 'nombre': 'Lavadora Automática 18kg', 'precio': 899.99, 'descuento': 15,
                'imagen': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&h=300&fit=crop',
                'categoria': 'Electrodomésticos', 'icono': 'bi-plug', 'sku': 'ELEC-002',
                'descripcion': 'Lavadora carga frontal 18kg con motor inverter, 16 programas y función vapor.',
                'descripcion_larga': 'Lavadora automática de alta capacidad con motor Direct Drive Inverter sin correa, más silencioso y duradero. 16 programas de lavado incluyendo ciclos rápidos, delicados y vapor para desinfección. Panel LED intuitivo con inicio diferido hasta 24h. Tambor de acero inoxidable con sistema anti-vibración. Eficiencia energética A+++.',
                'caracteristicas': ['18kg capacidad', 'Motor Inverter', '16 programas', 'Función vapor', 'Inicio diferido 24h', 'Eficiencia A+++', 'Anti-vibración'],
                'beneficios': ['Ahorro agua y energía', 'Ultra silenciosa', 'Ropa perfectamente limpia', 'Larga durabilidad'],
                'especificaciones': {'Capacidad': '18 kg', 'Tipo': 'Carga frontal', 'Motor': 'Direct Drive Inverter', 'Programas': '16', 'Velocidad centrifugado': '1400 RPM', 'Eficiencia': 'A+++', 'Garantía motor': '10 años', 'Garantía': '2 años'},
                'resenas': [{'usuario': 'Carmen R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'La mejor lavadora que he tenido! Muy silenciosa y eficiente.'}]
            },
            {
                'id': 3, 'nombre': 'Microondas Digital', 'precio': 199.99, 'descuento': 20,
                'imagen': 'https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=400&h=300&fit=crop',
                'categoria': 'Electrodomésticos', 'icono': 'bi-plug', 'sku': 'ELEC-003',
                'descripcion': 'Microondas digital 1.2 pies cúbicos con grill, 10 niveles de potencia y 8 programas.',
                'descripcion_larga': 'Microondas digital multifunción con función grill para dorar y gratinar. Panel de control digital táctil con 8 programas preestablecidos: palomitas, pizza, bebidas, recalentar, descongelar, patatas, vegetales y pescado. 10 niveles de potencia hasta 1200W. Interior de cerámica easy-clean y plato giratorio de 31.5cm. Reloj digital y bloqueo de seguridad para niños.',
                'caracteristicas': ['1200W potencia', 'Función grill', '8 programas auto', '10 niveles potencia', 'Interior cerámico', 'Panel táctil', 'Bloqueo infantil'],
                'beneficios': ['Cocción uniforme', 'Fácil limpieza', 'Múltiples funciones', 'Uso sencillo'],
                'especificaciones': {'Capacidad': '34 litros (1.2 pies³)', 'Potencia': '1200W', 'Tipo': 'Digital con grill', 'Programas': '8 automáticos', 'Interior': 'Cerámica', 'Plato': '31.5 cm', 'Dimensiones': '54x44x34 cm', 'Garantía': '1 año'},
                'resenas': [{'usuario': 'Pedro L.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '16 Nov 2025', 'comentario': 'Buen microondas, el grill funciona muy bien.'}]
            },
            {
                'id': 4, 'nombre': 'Auriculares Bluetooth Premium', 'precio': 399.99, 'descuento': 25,
                'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
                'categoria': 'Tecnología', 'icono': 'bi-headphones', 'sku': 'TECH-004',
                'descripcion': 'Auriculares inalámbricos con cancelación de ruido activa y sonido Hi-Fi.',
                'descripcion_larga': 'Auriculares Bluetooth premium con cancelación de ruido activa (ANC) y modo de transparencia. Drivers de 40mm con sonido Hi-Fi de alta resolución. Batería de larga duración: hasta 30 horas con ANC desactivado y 20 horas con ANC activado. Carga rápida: 5 minutos para 2 horas de uso. Almohadillas de espuma viscoelástica para máximo confort. Controles táctiles intuitivos y asistente de voz integrado. Plegables con estuche rígido de transporte incluido.',
                'caracteristicas': ['Cancelación ruido ANC', 'Bluetooth 5.3', 'Drivers 40mm Hi-Fi', 'Batería 30h', 'Carga rápida USB-C', 'Controles táctiles', 'Micrófono con reducción de ruido'],
                'beneficios': ['Sonido premium', 'Comodidad extrema', 'Batería duradera', 'Aísla del ruido'],
                'especificaciones': {'Conectividad': 'Bluetooth 5.3', 'Batería': '30h (sin ANC), 20h (con ANC)', 'Drivers': '40mm Hi-Fi', 'ANC': 'Sí, activo', 'Micrófono': 'Dual con reducción ruido', 'Carga': 'USB-C rápida', 'Peso': '250g', 'Garantía': '1 año'},
                'resenas': [{'usuario': 'Carlos M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Increíble calidad de sonido! La cancelación de ruido es perfecta.'}]
            },
            {
                'id': 5, 'nombre': 'Licuadora Pro 1200W', 'precio': 129.99, 'descuento': 30,
                'imagen': 'https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400&h=300&fit=crop',
                'categoria': 'Electrodomésticos', 'icono': 'bi-plug', 'sku': 'ELEC-005',
                'descripcion': 'Licuadora profesional 1200W con 10 velocidades, vaso de vidrio 2L y cuchillas titanio.',
                'descripcion_larga': 'Licuadora de alto rendimiento con motor de 1200W capaz de triturar hielo, frutas congeladas y frutos secos. 10 velocidades + función pulso para control preciso. Vaso de vidrio reforzado de 2 litros libre de BPA. Cuchillas de 6 puntas recubiertas en titanio ultra resistentes. Base antideslizante con ventosas. Incluye vaso portátil para smoothies.',
                'caracteristicas': ['Motor 1200W', '10 velocidades + pulso', 'Vaso vidrio 2L', 'Cuchillas 6 puntas titanio', 'Libre de BPA', 'Base ventosa', 'Vaso portátil incluido'],
                'beneficios': ['Tritura hielo fácilmente', 'Smoothies perfectos', 'Duradera y potente', 'Fácil limpieza'],
                'especificaciones': {'Potencia': '1200W', 'Velocidades': '10 + pulso', 'Capacidad': '2 litros', 'Material vaso': 'Vidrio reforzado', 'Cuchillas': 'Titanio 6 puntas', 'RPM': '28,000', 'Voltaje': '110-120V', 'Garantía': '2 años'},
                'resenas': [{'usuario': 'Luis H.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '15 Nov 2025', 'comentario': 'Potentísima! Hace smoothies perfectos en segundos.'}]
            },
            {
                'id': 6, 'nombre': 'Cafetera Express', 'precio': 179.99, 'descuento': 15,
                'imagen': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop',
                'categoria': 'Electrodomésticos', 'icono': 'bi-plug', 'sku': 'ELEC-006',
                'descripcion': 'Cafetera express semi-automática con espumador de leche, 15 bares y molinillo.',
                'descripcion_larga': 'Cafetera express profesional con bomba italiana de 15 bares para extracciones perfectas. Molinillo cónico de cerámica integrado con 18 ajustes de molido. Vaporizador manual para crear espuma de leche cremosa estilo barista. Panel de control táctil para seleccionar intensidad y temperatura. Depósito de agua 1.8L removible. Bandeja calientatazas superior. Sistema de pre-infusión para máximo aroma.',
                'caracteristicas': ['Bomba 15 bares', 'Molinillo cerámico 18 niveles', 'Espumador profesional', 'Panel táctil', 'Depósito 1.8L', 'Calientatazas', 'Pre-infusión'],
                'beneficios': ['Café tipo barista', 'Molienda fresca', 'Espuma perfecta', 'Fácil de usar'],
                'especificaciones': {'Presión': '15 bares', 'Molinillo': 'Cónico cerámica', 'Depósito': '1.8 litros', 'Potencia': '1450W', 'Tipo': 'Semi-automática', 'Material': 'Acero inoxidable', 'Tazas': 'Simple o doble', 'Garantía': '2 años'},
                'resenas': [{'usuario': 'Ricardo G.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Como tener un café en casa! El espumador es excelente.'}]
            }
        ],
        'ferreteria': [
            {'id': 1, 'nombre': 'Taladro Inalámbrico 20V', 'precio': 149.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400&h=300&fit=crop', 'categoria': 'Ferretería', 'icono': 'bi-tools', 'sku': 'FERR-001', 'descripcion': 'Taladro percutor inalámbrico 20V con 2 baterías, 50 piezas y maletín.', 'descripcion_larga': 'Taladro percutor profesional con motor brushless de larga duración. Incluye 2 baterías de litio 20V 2.0Ah, cargador rápido y maletín. 21+3 ajustes de torque, 2 velocidades (0-400 / 0-1500 RPM). Mandril auto-apretante 13mm. Luz LED para trabajo en lugares oscuros. Set de 50 piezas: brocas, puntas y portabrocas.', 'caracteristicas': ['Motor brushless', '20V baterías litio', '2 velocidades', '24 ajustes torque', 'Luz LED', 'Set 50 piezas', 'Maletín incluido'], 'beneficios': ['Mayor potencia', 'Batería duradera', 'Versátil', 'Profesional'], 'especificaciones': {'Voltaje': '20V', 'Baterías': '2x 2.0Ah litio', 'Velocidades': '2 (400/1500 RPM)', 'Torque': '45 Nm', 'Mandril': '13mm', 'Peso': '1.3 kg', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'Jorge P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Excelente taladro! Muy potente y las baterías duran mucho.'}]},
            {'id': 2, 'nombre': 'Set de Herramientas 120 Piezas', 'precio': 89.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=400&h=300&fit=crop', 'categoria': 'Ferretería', 'icono': 'bi-tools', 'sku': 'FERR-002', 'descripcion': 'Set completo de herramientas 120 piezas con maletín organizador de aluminio.', 'descripcion_larga': 'Set profesional con 120 herramientas esenciales: destornilladores, llaves, alicates, martillo, cinta métrica y más. Fabricadas en acero cromo-vanadio resistente. Maletín de aluminio con organizador interno. Incluye nivel de burbuja, sierra manual, y juego completo de puntas y dados. Ideal para el hogar y uso profesional.', 'caracteristicas': ['120 piezas completas', 'Acero cromo-vanadio', 'Maletín aluminio', 'Organizador interno', 'Herramientas esenciales', 'Nivel incluido'], 'beneficios': ['Todo en uno', 'Alta durabilidad', 'Bien organizado', 'Portátil'], 'especificaciones': {'Piezas': '120', 'Material': 'Acero cromo-vanadio', 'Maletín': 'Aluminio reforzado', 'Dimensiones': '45x35x10 cm', 'Peso': '8 kg', 'Garantía': '5 años'}, 'resenas': [{'usuario': 'Manuel S.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '16 Nov 2025', 'comentario': 'Set muy completo y de buena calidad. Lo recomiendo.'}]},
            {'id': 3, 'nombre': 'Sierra Circular Profesional', 'precio': 199.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=400&h=300&fit=crop', 'categoria': 'Ferretería', 'icono': 'bi-tools', 'sku': 'FERR-003', 'descripcion': 'Sierra circular 1800W, disco 185mm, guía laser y profundidad ajustable 0-65mm.', 'descripcion_larga': 'Sierra circular profesional con motor de 1800W para cortes precisos en madera, plástico y aluminio. Disco de 185mm con 24 dientes. Sistema de guía láser para cortes rectos perfectos. Ajuste de profundidad 0-65mm y ángulo de bisel 0-45°. Empuñadura ergonómica con recubrimiento antideslizante. Incluye disco extra, guía paralela y llave Allen.', 'caracteristicas': ['1800W potencia', 'Disco 185mm 24T', 'Guía láser', 'Profundidad 0-65mm', 'Bisel 0-45°', 'Doble empuñadura', 'Disco extra incluido'], 'beneficios': ['Cortes precisos', 'Versatil', 'Segura', 'Profesional'], 'especificaciones': {'Potencia': '1800W', 'Disco': '185mm', 'Profundidad corte': '0-65mm', 'Velocidad': '5500 RPM', 'Bisel': '0-45°', 'Peso': '4.2 kg', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'Francisco M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Potente y precisa. El láser ayuda mucho en los cortes.'}]},
            {'id': 4, 'nombre': 'Escalera Telescópica 5m', 'precio': 299.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1513467535987-fd81bc7d62f8?w=400&h=300&fit=crop', 'categoria': 'Ferretería', 'icono': 'bi-tools', 'sku': 'FERR-004', 'descripcion': 'Escalera telescópica multiposición de aluminio, extensible hasta 5m, carga 150kg.', 'descripcion_larga': 'Escalera telescópica de aluminio aeronáutico ligero pero resistente. Se extiende sección por sección hasta 5 metros. Sistema de bloqueo de seguridad en cada peldaño. Pies antideslizantes. Multiposición: recta, tijera o andamio. Compacta al retraer (90cm). Certificación EN131. Perfecta para trabajos en altura con máxima seguridad.', 'caracteristicas': ['Extensible hasta 5m', 'Aluminio aeronáutico', 'Bloqueo seguridad', 'Multiposición', 'Pies antideslizantes', 'Compacta 90cm', 'Carga 150kg'], 'beneficios': ['Versátil', 'Fácil transporte', 'Muy segura', 'Resistente'], 'especificaciones': {'Altura máx': '5 metros', 'Material': 'Aluminio', 'Capacidad': '150 kg', 'Peldaños': '16', 'Compacta': '90 cm', 'Peso': '14 kg', 'Certificación': 'EN131', 'Garantía': '3 años'}, 'resenas': [{'usuario': 'Raúl T.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '14 Nov 2025', 'comentario': 'Muy práctica y segura. Fácil de guardar.'}]},
            {'id': 5, 'nombre': 'Compresor de Aire', 'precio': 249.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=400&h=300&fit=crop', 'categoria': 'Ferretería', 'icono': 'bi-tools', 'sku': 'FERR-005', 'descripcion': 'Compresor de aire 50L, 3HP, portátil con ruedas, incluye kit de 5 accesorios.', 'descripcion_larga': 'Compresor de aire profesional con tanque de 50 litros. Motor de 3HP (2200W) libre de aceite para bajo mantenimiento. Presión máxima 8 bar / 116 PSI. Manómetro dual para control preciso. Incluye kit de 5 accesorios: pistola inflado, manguera 5m, adaptadores y boquillas. Ruedas grandes para fácil transporte. Silencioso 75dB. Ideal para pintura, inflado y herramientas neumáticas.', 'caracteristicas': ['Tanque 50L', 'Motor 3HP libre aceite', 'Presión 8 bar / 116 PSI', 'Kit 5 accesorios', 'Ruedas portátil', 'Silencioso 75dB', 'Manómetro dual'], 'beneficios': ['Potente', 'Bajo mantenimiento', 'Portátil', 'Versátil'], 'especificaciones': {'Capacidad tanque': '50 litros', 'Motor': '3HP 2200W', 'Presión máx': '8 bar / 116 PSI', 'Caudal': '206 L/min', 'Ruido': '75 dB', 'Peso': '32 kg', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'Alberto C.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Excelente compresor! Potente y silencioso.'}]},
            {'id': 6, 'nombre': 'Nivel Láser Digital', 'precio': 129.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop', 'categoria': 'Ferretería', 'icono': 'bi-tools', 'sku': 'FERR-006', 'descripcion': 'Nivel láser autonivelante 360°, alcance 30m, verde, con trípode y control remoto.', 'descripcion_larga': 'Nivel láser profesional de líneas cruzadas 360° autonivelante. Láser verde 4 veces más visible que rojo. Alcance de 30m (60m con receptor). Precisión ±3mm a 10m. Se autonivela en segundos. Modo pulso para trabajo exterior con detector. Base magnética giratoria. Incluye trípode ajustable, control remoto, gafas de protección, objetivo y maletín.', 'caracteristicas': ['Líneas 360° autonivelante', 'Láser verde', 'Alcance 30m', 'Precisión ±3mm/10m', 'Base magnética', 'Trípode incluido', 'Control remoto'], 'beneficios': ['Alta precisión', 'Fácil de usar', 'Visible en exteriores', 'Completo'], 'especificaciones': {'Tipo': 'Líneas cruzadas 360°', 'Color láser': 'Verde', 'Alcance': '30m (60m con receptor)', 'Precisión': '±3mm a 10m', 'Autonivelación': 'Sí ±4°', 'Batería': 'Recargable litio', 'IP': 'IP54', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'Marcos V.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '15 Nov 2025', 'comentario': 'Muy preciso y fácil de usar. El láser verde se ve perfecto.'}]}
        ],
        'bebe': [
            {'id': 1, 'nombre': 'Coche para Bebé Premium', 'precio': 349.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños', 'icono': 'bi-balloon-heart', 'sku': 'BEBE-001', 'descripcion': 'Cochecito 3en1: coche, silla auto y capazo. Plegable, suspensión y accesorios incluidos.', 'descripcion_larga': 'Sistema de viaje completo 3 en 1: cochecito, silla de auto (grupo 0+) y capazo. Estructura de aluminio ligero pero resistente. Suspensión en las 4 ruedas para paseo suave. Ruedas giratorias con bloqueo. Capota extensible UPF 50+. Asiento reclinable en 4 posiciones. Plegado compacto con una mano. Incluye: bolso maternal, cubrepiés, mosquitero y protector de lluvia.', 'caracteristicas': ['Sistema 3en1', 'Aluminio ligero', 'Suspensión 4 ruedas', 'Capota UPF 50+', 'Plegado fácil', 'Accesorios incluidos', 'Reclinable 4 posiciones'], 'beneficios': ['Todo incluido', 'Máxima comodidad', 'Fácil transporte', 'Protección solar'], 'especificaciones': {'Tipo': '3 en 1', 'Edad': '0-36 meses', 'Peso máx': '15 kg', 'Marco': 'Aluminio', 'Plegado': 'Compacto una mano', 'Ruedas': 'Giratorias con bloqueo', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'María José P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente! Muy completo y de buena calidad.'}]},
            {'id': 2, 'nombre': 'Cuna Convertible', 'precio': 299.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños', 'icono': 'bi-balloon-heart', 'sku': 'BEBE-002', 'descripcion': 'Cuna convertible 4en1: cuna, mini cama, sofá y cama juvenil. Madera maciza de pino.', 'descripcion_larga': 'Cuna convertible que crece con tu bebé. 4 configuraciones: cuna de bebé, mini cama para niño pequeño, sofá juvenil y cama individual. Fabricada en madera maciza de pino natural. 3 alturas de colchón ajustables. Barandillas removibles. Diseño atemporal que se adapta a cualquier decoración. Incluye kit de conversión. Fácil montaje con herramientas incluidas. Colchón no incluido (tamaño estándar 120x60cm).', 'caracteristicas': ['Convertible 4en1', 'Madera pino maciza', '3 alturas colchón', 'Barandillas removibles', 'Kit conversión incluido', 'Diseño atemporal', 'Fácil montaje'], 'beneficios': ['Crece con el niño', 'Inversión a largo plazo', 'Madera natural', 'Versátil'], 'especificaciones': {'Material': 'Pino macizo', 'Dimensiones cuna': '125x65x85 cm', 'Colchón': '120x60 cm (no incluido)', 'Altura base': '3 posiciones', 'Peso máx': '50 kg', 'Edad': '0-12 años', 'Garantía': '3 años'}, 'resenas': [{'usuario': 'Carolina M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Hermosa cuna y muy práctica. La madera es de excelente calidad.'}]},
            {'id': 3, 'nombre': 'Monitor de Bebé con Cámara', 'precio': 129.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños', 'icono': 'bi-balloon-heart', 'sku': 'BEBE-003', 'descripcion': 'Monitor con cámara HD, visión nocturna, audio bidireccional, sensor temperatura y canciones.', 'descripcion_larga': 'Monitor de video digital con pantalla LCD 5" HD. Cámara giratoria remota 360° horizontal y 120° vertical. Visión nocturna infrarroja automática. Audio bidireccional para hablar con el bebé. Sensor de temperatura ambiente con alertas. Modo VOX activación por voz. 5 canciones de cuna incorporadas. Alcance hasta 300m en exteriores. Batería recargable de larga duración en unidad parental.', 'caracteristicas': ['Pantalla LCD 5" HD', 'Cámara giratoria 360°', 'Visión nocturna IR', 'Audio bidireccional', 'Sensor temperatura', 'Modo VOX', 'Canciones de cuna', 'Alcance 300m'], 'beneficios': ['Vigilancia completa', 'Visión clara noche', 'Comunicación fácil', 'Tranquilidad'], 'especificaciones': {'Pantalla': '5" LCD HD', 'Resolución': '720p', 'Visión nocturna': 'Infrarroja automática', 'Audio': 'Bidireccional', 'Alcance': '300 metros', 'Batería': 'Recargable 2000mAh', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Fernanda L.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '16 Nov 2025', 'comentario': 'Excelente calidad de imagen y sonido. Muy confiable.'}]},
            {'id': 4, 'nombre': 'Set de Alimentación', 'precio': 45.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños', 'icono': 'bi-balloon-heart', 'sku': 'BEBE-004', 'descripcion': 'Set completo alimentación: platos, vasos, cubiertos, babero y bowl. Libre de BPA.', 'descripcion_larga': 'Set de alimentación infantil de 7 piezas: 2 platos divididos con ventosa, 2 bowls, vaso entrenamiento con asas, juego de cubiertos ergonómicos y babero impermeable con bolsillo. Fabricado en silicona de grado alimenticio y plástico libre de BPA, ftalatos y PVC. Apto para microondas y lavavajillas. Colores alegres y diseño anti-derrames. Base con ventosa que se adhiere a la mesa. Perfecto para iniciar alimentación complementaria.', 'caracteristicas': ['7 piezas completas', 'Libre BPA/ftalatos', 'Silicona grado alimenticio', 'Ventosa anti-vuelco', 'Apto microondas/lavavajillas', 'Ergonómico', 'Colores alegres'], 'beneficios': ['100% seguro', 'Evita derrames', 'Fácil limpieza', 'Completo'], 'especificaciones': {'Piezas': '7', 'Material': 'Silicona + PP libre BPA', 'Edad': '6+ meses', 'Microondas': 'Sí', 'Lavavajillas': 'Sí', 'Certificación': 'FDA/LFGB', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Paola R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '15 Nov 2025', 'comentario': 'Excelente set! Los platos se pegan bien y son muy prácticos.'}]},
            {'id': 5, 'nombre': 'Juguete Educativo Musical', 'precio': 59.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1587818541473-f2e71229046f?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños', 'icono': 'bi-balloon-heart', 'sku': 'BEBE-005', 'descripcion': 'Mesa de actividades musical con luces, sonidos, formas y texturas. Bilingüe español-inglés.', 'descripcion_larga': 'Mesa de actividades multifuncional que estimula el desarrollo sensorial y cognitivo. Incluye: piano con 5 teclas iluminadas, tambor, guitarra, engranajes giratorios, teléfono y botones interactivos. Más de 100 canciones, melodías y frases en español e inglés. Luces LED de colores. Enseña números, letras, formas, colores y animales. Patas removibles para usar desde el suelo. Volumen ajustable. Desarrolla motricidad fina, coordinación y estimulación auditiva.', 'caracteristicas': ['6 áreas de juego', '100+ canciones/frases', 'Bilingüe ES/EN', 'Luces LED colores', 'Patas removibles', 'Volumen ajustable', 'Texturas variadas'], 'beneficios': ['Estimula desarrollo', 'Aprendizaje divertido', 'Crece con el bebé', 'Educativo'], 'especificaciones': {'Edad': '6-36 meses', 'Idiomas': 'Español/Inglés', 'Sonidos': '100+', 'Material': 'Plástico ABS seguro', 'Pilas': '3 AA (incluidas)', 'Dimensiones': '45x45x40 cm', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Claudia V.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'A mi bebé le encanta! Muy entretenido y educativo.'}]},
            {'id': 6, 'nombre': 'Pañalera de Viaje', 'precio': 79.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños', 'icono': 'bi-balloon-heart', 'sku': 'BEBE-006', 'descripcion': 'Mochila pañalera multifuncional con USB, aislante térmico, cambiador y ganchos coche.', 'descripcion_larga': 'Mochila pañalera de diseño moderno y funcional. Capacidad 30L con 16 bolsillos organizadores. Compartimento principal amplio. 2 bolsillos térmicos aislantes para biberones. Puerto USB externo para cargar celular. Cambiador plegable impermeable incluido. Correas acolchadas ajustables. Puede usarse como mochila, bolso de mano o colgarse del cochecito con ganchos incluidos. Material Oxford resistente al agua. Abertura amplia para fácil acceso.', 'caracteristicas': ['Capacidad 30L', '16 bolsillos', 'Puerto USB', 'Bolsillos térmicos', 'Cambiador incluido', '3 formas de uso', 'Impermeable', 'Ganchos coche'], 'beneficios': ['Súper organizada', 'Manos libres', 'Mantiene temperatura', 'Versátil'], 'especificaciones': {'Capacidad': '30 litros', 'Bolsillos': '16', 'Material': 'Oxford impermeable', 'Dimensiones': '40x28x20 cm', 'Peso': '650 g', 'Puerto USB': 'Sí (cable no incluido)', 'Color': 'Gris/Negro', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Verónica S.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Perfecta! Cabe todo y está muy bien organizada.'}]}
        ],
        'aire_libre': [
            {'id': i+1, 'nombre': p['nombre'], 'precio': p['precio'], 'descuento': p['descuento'], 'imagen': p['imagen'], 'categoria': 'Aire Libre', 'icono': 'bi-tree', 'sku': f'AIRE-{str(i+1).zfill(3)}', 'descripcion': desc[i], 'descripcion_larga': desc_larga[i], 'caracteristicas': caract[i], 'beneficios': benef[i], 'especificaciones': espec[i], 'resenas': [resena[i]]} 
            for i, p in enumerate([
                {'nombre': 'Bicicleta de Montaña Pro', 'precio': 599.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1541625602330-2277a4c46182?w=400&h=300&fit=crop'},
                {'nombre': 'Carpa Camping 6 Personas', 'precio': 249.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400&h=300&fit=crop'},
                {'nombre': 'Parrilla Portátil a Gas', 'precio': 179.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop'},
                {'nombre': 'Set de Pesca Completo', 'precio': 129.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1502139214982-d0ad755818d8?w=400&h=300&fit=crop'},
                {'nombre': 'Mochila Trekking 50L', 'precio': 99.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop'},
                {'nombre': 'Kayak Inflable 2 Personas', 'precio': 399.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop'}
            ]) if (desc := ['Bicicleta montaña aluminio 27.5", suspensión doble, 21 velocidades Shimano, frenos disco.', 'Carpa familiar 6 personas, impermeable 3000mm, 2 habitaciones, porche y ventanas mesh.', 'Parrilla gas portátil 2 quemadores, encendido automático, tapa, termómetro y ruedas.', 'Kit pesca completo: caña telescópica 2.7m, carrete, señuelos, anzuelos y accesorios.', 'Mochila trekking 50L impermeable, sistema ventilación, cinturón lumbar y cubierta lluvia.', 'Kayak inflable biplaza, PVC reforzado, asientos ajustables, remos, bomba y bolsa.']) and (desc_larga := ['Bicicleta de montaña profesional con cuadro de aluminio 6061 ligero y resistente. Ruedas 27.5" con llantas doble pared. Suspensión delantera con bloqueo y suspensión trasera con 100mm de recorrido. Sistema de cambios Shimano de 21 velocidades. Frenos de disco hidráulicos delanteros y traseros.', 'Carpa espaciosa para 6 personas con diseño de 2 habitaciones separadas más área común/porche. Tela exterior poliéster 190T con recubrimiento PU 3000mm resistente al agua. Piso de PE impermeable soldado. Estructura de fibra de vidrio flexible y resistente. 4 ventanas con malla mosquitera.', 'Parrilla portátil a gas propano con 2 quemadores independientes de acero inoxidable. Superficie de cocción de 50x35cm con parrilla de hierro fundido esmaltado. Encendido electrónico instantáneo. Tapa con termómetro integrado para control de temperatura.', 'Set completo de pesca ideal para principiantes y aficionados. Incluye: caña telescópica de fibra de carbono 2.7m (5 secciones), carrete spinning con freno ajustable, 100+ accesorios (señuelos variados, anzuelos, plomos, flotadores).', 'Mochila de trekking profesional 50 litros con sistema de carga ajustable. Panel posterior con ventilación Air Mesh. Cinturón lumbar acolchado con bolsillos. Correas pecho y compresión. Múltiples compartimentos.', 'Kayak inflable profesional para 2 personas con construcción de PVC super resistente de 3 capas. Capacidad de carga 180kg. Diseño aerodinámico para fácil manejo. 2 asientos inflables ajustables con respaldo alto.']) and (caract := [['Cuadro aluminio 6061', 'Suspensión doble 100mm', 'Shimano 21 velocidades', 'Frenos disco hidráulicos'], ['Capacidad 6 personas', '2 habitaciones + porche', 'Impermeable 3000mm', 'Montaje fácil 15min'], ['2 quemadores independientes', 'Encendido automático', 'Tapa con termómetro', 'Ruedas portátil'], ['Caña telescópica 2.7m', 'Carrete spinning', '100+ accesorios', 'Retrae a 58cm'], ['Capacidad 50L', 'Sistema ventilación', 'Múltiples compartimentos', 'Cubierta lluvia incluida'], ['Capacidad 2 personas', 'PVC reforzado 3 capas', 'Asientos ajustables', '2 remos aluminio']]) and (benef := [['Ligera y resistente', 'Comodidad en terrenos', 'Control total'], ['Espaciosa', 'Protección completa', 'Ventilación óptima'], ['Fácil de usar', 'Control temperatura', 'Portátil'], ['Kit completo', 'Fácil transporte', 'Para principiantes'], ['Cómoda para largas caminatas', 'Bien ventilada', 'Muy organizada'], ['Fácil transporte', 'Muy estable', 'Resistente']]) and (espec := [{'Material cuadro': 'Aluminio 6061', 'Ruedas': '27.5"', 'Velocidades': '21 Shimano', 'Garantía': '2 años'}, {'Capacidad': '6 personas', 'Impermeable': '3000mm', 'Dimensiones': '480x210x180 cm', 'Garantía': '1 año'}, {'Quemadores': '2 acero inoxidable', 'Potencia': '7 kW', 'Superficie': '50x35 cm', 'Garantía': '2 años'}, {'Caña': '2.7m telescópica', 'Material': 'Fibra carbono', 'Accesorios': '100+ piezas', 'Garantía': '1 año'}, {'Capacidad': '50 litros', 'Material': 'Nylon ripstop', 'Peso': '1.4 kg', 'Garantía': '2 años'}, {'Capacidad': '2 personas / 180kg', 'Material': 'PVC 3 capas', 'Dimensiones': '312x89 cm', 'Garantía': '1 año'}]) and (resena := [{'usuario': 'Mateo R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Excelente bici! Muy cómoda.'}, {'usuario': 'Rodrigo P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Súper espaciosa y fácil de armar.'}, {'usuario': 'Eduardo S.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente parrilla! Calienta rápido.'}, {'usuario': 'Gustavo L.', 'estrellas': 4, 'estrellas_range': range(4), 'fecha': '16 Nov 2025', 'comentario': 'Buen set para empezar.'}, {'usuario': 'Daniel M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Excelente mochila! Muy cómoda.'}, {'usuario': 'Sergio T.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Muy buen kayak! Estable.'}])
        ],
        'entretenimiento': [
            {'id': 1, 'nombre': 'Consola Gaming Next Gen', 'precio': 499.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1486401899868-0e435ed85128?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento', 'icono': 'bi-controller', 'sku': 'ENT-001', 'descripcion': 'Consola gaming de última generación con SSD 1TB, 4K 120fps, ray tracing y 2 controles.', 'descripcion_larga': 'Consola de videojuegos de nueva generación con procesador custom de 8 núcleos y GPU con ray tracing en tiempo real. SSD ultra rápido de 1TB para tiempos de carga mínimos. Soporte para resolución 4K a 120fps. Audio 3D inmersivo. Retrocompatibilidad con miles de juegos. 2 controles inalámbricos con feedback háptico y gatillos adaptativos. Conexión WiFi 6 y Bluetooth 5.1.', 'caracteristicas': ['SSD 1TB ultra rápido', 'GPU con ray tracing', '4K 120fps', 'Audio 3D', '2 controles incluidos', 'Retrocompatible', 'WiFi 6 + BT 5.1'], 'beneficios': ['Gráficos impresionantes', 'Carga instantánea', 'Librería enorme', 'Experiencia inmersiva'], 'especificaciones': {'CPU': '8 núcleos custom', 'GPU': 'Ray Tracing 10.28 TFLOPS', 'Memoria': '16GB GDDR6', 'Almacenamiento': '1TB SSD NVMe', 'Resolución': '4K 120Hz / 8K', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Ignacio F.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Impresionante! Los gráficos son increíbles.'}]},
            {'id': 2, 'nombre': 'Smart TV 55" 4K', 'precio': 699.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento', 'icono': 'bi-controller', 'sku': 'ENT-002', 'descripcion': 'Smart TV 55" 4K UHD, HDR10+, 120Hz, Google TV, Dolby Atmos y control por voz.', 'descripcion_larga': 'Smart TV de 55 pulgadas con panel 4K UHD (3840x2160) y tecnología QLED para colores vibrantes. Tasa de refresco 120Hz para imágenes fluidas. Compatible con HDR10+, Dolby Vision y HLG. Sistema operativo Google TV con miles de apps. Sonido Dolby Atmos. 4 entradas HDMI 2.1, 2 USB, WiFi 6 y Bluetooth. Control por voz Google Assistant y Alexa.', 'caracteristicas': ['55" 4K QLED', 'HDR10+ / Dolby Vision', '120Hz refresh rate', 'Google TV', 'Dolby Atmos', 'HDMI 2.1 x4', 'Control por voz'], 'beneficios': ['Imagen espectacular', 'Smart completo', 'Perfecto para gaming', 'Audio inmersivo'], 'especificaciones': {'Tamaño': '55 pulgadas', 'Resolución': '4K UHD 3840x2160', 'Panel': 'QLED', 'Refresh rate': '120Hz', 'Sistema': 'Google TV', 'Sonido': 'Dolby Atmos 30W', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'Cristian P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente TV! La calidad de imagen es impresionante.'}]},
            {'id': 3, 'nombre': 'Barra de Sonido Dolby', 'precio': 299.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento', 'icono': 'bi-controller', 'sku': 'ENT-003', 'descripcion': 'Barra de sonido 3.1.2 canales, Dolby Atmos, subwoofer inalámbrico, 400W y HDMI eARC.', 'descripcion_larga': 'Sistema de audio home theater 3.1.2 canales con Dolby Atmos y DTS:X para sonido tridimensional inmersivo. Barra principal de 3 canales + 2 altavoces verticales + subwoofer inalámbrico de 8". Potencia total 400W RMS. Conectividad HDMI eARC/ARC, óptico, Bluetooth 5.0 y WiFi. Compatible con streaming Spotify Connect, AirPlay 2 y Chromecast.', 'caracteristicas': ['Sistema 3.1.2 canales', 'Dolby Atmos + DTS:X', 'Subwoofer inalámbrico', 'Potencia 400W', 'HDMI eARC', 'Bluetooth/WiFi', 'App control'], 'beneficios': ['Sonido cinematográfico', 'Graves profundos', 'Fácil instalación', 'Streaming integrado'], 'especificaciones': {'Canales': '3.1.2', 'Potencia': '400W RMS', 'Dolby': 'Atmos + DTS:X', 'Subwoofer': '8" inalámbrico', 'Conectividad': 'HDMI eARC, BT, WiFi', 'Garantía': '2 años'}, 'resenas': [{'usuario': 'Hernán G.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Increíble sonido! Como estar en el cine.'}]},
            {'id': 4, 'nombre': 'Drone con Cámara 4K', 'precio': 449.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento', 'icono': 'bi-controller', 'sku': 'ENT-004', 'descripcion': 'Drone con cámara 4K gimbal 3 ejes, GPS, 28 minutos vuelo, modos inteligentes y mochila.', 'descripcion_larga': 'Drone profesional con cámara 4K UHD a 30fps en gimbal estabilizado de 3 ejes para videos ultra suaves. Sensor 1/2.3" de 12MP. GPS dual para vuelo preciso y retorno automático. Batería inteligente de 28 minutos. Transmisión de video hasta 4km. Modos inteligentes: Follow Me, Waypoints, Órbita, Panorama 360°. Sensores anti-colisión.', 'caracteristicas': ['Cámara 4K gimbal 3 ejes', 'GPS retorno auto', '28 min vuelo x2 baterías', 'Transmisión 4km', 'Modos inteligentes', 'Anti-colisión', '2 baterías + mochila'], 'beneficios': ['Videos profesionales', 'Fácil de volar', 'Muy estable', 'Completo'], 'especificaciones': {'Cámara': '4K 30fps / 12MP', 'Gimbal': '3 ejes', 'GPS': 'Dual', 'Batería': '28min x2', 'Alcance': '4 km', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Oscar V.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Espectacular! Videos súper estables.'}]},
            {'id': 5, 'nombre': 'Guitarra Eléctrica', 'precio': 379.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento', 'icono': 'bi-controller', 'sku': 'ENT-005', 'descripcion': 'Guitarra eléctrica stratocaster, 3 pastillas, amplificador 20W, afinador, cable y funda.', 'descripcion_larga': 'Guitarra eléctrica tipo Stratocaster con cuerpo de tilo y mástil de arce. Diapasón de palo rosa con 22 trastes. 3 pastillas single coil con selector de 5 posiciones para variedad tonal. Puente trémolo vintage. Incluye amplificador de 20W con overdrive, entrada auxiliar y auriculares. Afinador digital cromático clip-on. Cable profesional 3m. Todo listo para empezar a tocar.', 'caracteristicas': ['Cuerpo tilo / mástil arce', '3 pastillas single coil', 'Puente trémolo', 'Amplificador 20W', 'Afinador digital', 'Accesorios completos', 'Funda incluida'], 'beneficios': ['Paquete completo', 'Sonido versátil', 'Listo para usar', 'Gran calidad/precio'], 'especificaciones': {'Tipo': 'Stratocaster', 'Cuerpo': 'Tilo', 'Trastes': '22', 'Pastillas': '3 single coil', 'Amplificador': '20W con FX', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Emilio R.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '16 Nov 2025', 'comentario': 'Excelente para empezar! Buen sonido.'}]},
            {'id': 6, 'nombre': 'Set de Juegos de Mesa', 'precio': 89.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento', 'icono': 'bi-controller', 'sku': 'ENT-006', 'descripcion': 'Colección 10 juegos de mesa clásicos: ajedrez, damas, backgammon, póker, dominó y más.', 'descripcion_larga': 'Set premium de 10 juegos de mesa clásicos en elegante estuche de madera. Incluye: ajedrez con piezas de madera torneada, damas, backgammon, póker (100 fichas + 2 mazos), dominó, parchís, oca, mikado, dados y cartas. Tableros de madera grabados reversibles. Fichas y accesorios de calidad. Instrucciones en español para cada juego. Estuche portátil con asas.', 'caracteristicas': ['10 juegos incluidos', 'Estuche madera premium', 'Tableros grabados', 'Piezas calidad', '100 fichas póker', 'Instrucciones español', 'Portátil con asas'], 'beneficios': ['Variedad', 'Reuniones familiares', 'Calidad duradera', 'Educativo'], 'especificaciones': {'Juegos': '10 clásicos', 'Material estuche': 'Madera', 'Dimensiones': '40x40x6 cm', 'Peso': '3 kg', 'Jugadores': '1-6', 'Garantía': '1 año'}, 'resenas': [{'usuario': 'Beatriz H.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Excelente set! Perfecto para la familia.'}]}
        ],
        'salud': [
            {'id': i+1, 'nombre': p['nombre'], 'precio': p['precio'], 'descuento': p['descuento'], 'imagen': p['imagen'], 'categoria': 'Salud y Bienestar', 'icono': 'bi-heart-pulse', 'sku': f'SALUD-{str(i+1).zfill(3)}', 'descripcion': desc_salud[i], 'descripcion_larga': desc_larga_salud[i], 'caracteristicas': caract_salud[i], 'beneficios': benef_salud[i], 'especificaciones': espec_salud[i], 'resenas': [resena_salud[i]]} 
            for i, p in enumerate([
                {'nombre': 'Caminadora Eléctrica Pro', 'precio': 899.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400&h=300&fit=crop'},
                {'nombre': 'Set de Pesas Ajustables', 'precio': 199.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop'},
                {'nombre': 'Bicicleta Estática Smart', 'precio': 449.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400&h=300&fit=crop'},
                {'nombre': 'Mat de Yoga Premium', 'precio': 49.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400&h=300&fit=crop'},
                {'nombre': 'Masajeador Eléctrico', 'precio': 129.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop'},
                {'nombre': 'Monitor de Presión Digital', 'precio': 69.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=300&fit=crop'}
            ]) if (desc_salud := ['Caminadora eléctrica 3HP, velocidad 0.8-16km/h, inclinación 15 niveles, pantalla táctil y Bluetooth.', 'Par de mancuernas ajustables 2.5-24kg por unidad, selector dial, compactas con soporte.', 'Bicicleta estática magnética, 16 niveles resistencia, monitor LCD, Bluetooth y soporte tablet.', 'Esterilla yoga TPE eco 6mm, antideslizante doble cara, líneas alineación y bolsa transporte.', 'Masajeador percusión muscular, 6 cabezales, 30 velocidades, batería 6h y pantalla LED.', 'Tensiómetro digital brazo, detección arritmia, memoria 240 lecturas, validado clínicamente.']) and (desc_larga_salud := ['Caminadora profesional con motor de 3HP de corriente continua ultra silencioso. Velocidad ajustable de 0.8 a 16 km/h. Inclinación eléctrica de 15 niveles (0-15%). Superficie de carrera amplia 125x45cm. Pantalla táctil LCD 7" que muestra tiempo, distancia, calorías, velocidad y frecuencia cardíaca.', 'Sistema de pesas ajustables que reemplaza 15 pares de mancuernas en un set compacto. Cada mancuerna se ajusta de 2.5kg a 24kg con selector dial giratorio en incrementos de 2.5kg. Cambio instantáneo en 2 segundos sin necesidad de placas sueltas. Diseño compacto que ahorra espacio. Agarre ergonómico antideslizante.', 'Bicicleta estática indoor con sistema de resistencia magnética silencioso de 16 niveles. Volante de inercia de 8kg para pedaleo suave. Monitor LCD multifunción que muestra tiempo, velocidad, distancia, calorías y pulso. Sensores de frecuencia cardíaca en manillar. Conectividad Bluetooth con apps de entrenamiento.', 'Mat de yoga profesional de TPE (Thermoplastic Elastomer) ecológico, no tóxico, sin látex ni PVC. Grosor de 6mm para máxima comodidad y protección de articulaciones. Superficie antideslizante de doble cara con textura que proporciona agarre superior incluso con sudoración. Líneas de alineación corporal grabadas.', 'Pistola de masaje de percusión profesional con motor silencioso de alta torque. 30 niveles de velocidad ajustables (1200-3200 RPM) para masaje personalizado. 6 cabezales intercambiables para diferentes grupos musculares. Pantalla LED táctil que muestra velocidad y batería. Batería de litio de 2500mAh dura hasta 6 horas.', 'Monitor de presión arterial digital de brazo con tecnología Intellisense para medición precisa y cómoda. Pantalla LCD grande de fácil lectura. Detecta automáticamente arritmias cardíacas. Indicador de hipertensión según OMS. Memoria para 240 lecturas (2 usuarios x 120). Promedio de 3 últimas lecturas.']) and (caract_salud := [['Motor 3HP silencioso', 'Velocidad 0.8-16 km/h', 'Inclinación 15 niveles', 'Pantalla táctil 7"', 'App Bluetooth', '12 programas', 'Plegable con ruedas'], ['Ajuste 2.5-24kg', 'Selector dial rápido', 'Cambio en 2 segundos', 'Reemplazan 15 pares', 'Agarre ergonómico', 'Soporte incluido'], ['16 niveles resistencia', 'Volante 8kg', 'Monitor LCD', 'Bluetooth + apps', 'Sensores pulso', 'Asiento ajustable'], ['TPE ecológico', 'Grosor 6mm', 'Antideslizante doble cara', 'Líneas alineación', '183x61cm', 'Bolsa + correa'], ['30 velocidades (1200-3200 RPM)', '6 cabezales intercambiables', 'Motor silencioso <50dB', 'Batería 6 horas', 'Pantalla LED', 'Estuche rígido'], ['Detección arritmia', 'Pantalla LCD grande', 'Memoria 240 lecturas', 'Brazalete 22-42cm', 'Validado clínicamente', 'Estuche incluido']]) and (benef_salud := [['Gimnasio en casa', 'Protege articulaciones', 'Silenciosa', 'Seguimiento completo'], ['Ahorro espacio', 'Versátiles', 'Rápido ajuste', 'Gimnasio completo'], ['Entrenamiento efectivo', 'Silenciosa', 'Conectada', 'Ajustable'], ['Máximo confort', 'Agarre superior', 'Eco-friendly', 'Portátil'], ['Recuperación rápida', 'Alivia dolor muscular', 'Silencioso', 'Portátil'], ['Monitoreo preciso', 'Fácil de usar', 'Control salud', 'Certificado médico']]) and (espec_salud := [{'Motor': '3HP continua', 'Velocidad': '0.8-16 km/h', 'Inclinación': '15 niveles', 'Pantalla': '7" táctil', 'Capacidad': '150 kg', 'Garantía': '3 años motor'}, {'Peso por unidad': '2.5-24 kg', 'Incrementos': '2.5 kg', 'Sistema': 'Dial selector', 'Total set': '48 kg', 'Garantía': '2 años'}, {'Resistencia': '16 niveles magnéticos', 'Volante': '8 kg', 'Monitor': 'LCD + Bluetooth', 'Capacidad': '120 kg', 'Garantía': '2 años'}, {'Material': 'TPE ecológico', 'Grosor': '6 mm', 'Dimensiones': '183x61 cm', 'Peso': '1 kg', 'Garantía': '1 año'}, {'Velocidades': '30 (1200-3200 RPM)', 'Cabezales': '6 tipos', 'Batería': '2500mAh (6h)', 'Ruido': '<50 dB', 'Garantía': '2 años'}, {'Tipo': 'Brazo automático', 'Memoria': '240 lecturas', 'Brazalete': '22-42 cm', 'Precisión': '±3 mmHg', 'Garantía': '3 años'}]) and (resena_salud := [{'usuario': 'Gloria M.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Excelente! Muy silenciosa y robusta.'}, {'usuario': 'Raúl C.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Súper prácticas y ahorran espacio.'}, {'usuario': 'Silvia P.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '17 Nov 2025', 'comentario': 'Muy buena bici! Cómoda y silenciosa.'}, {'usuario': 'Adriana F.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '16 Nov 2025', 'comentario': 'Perfecta! Muy cómoda y no resbala.'}, {'usuario': 'Esteban J.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '19 Nov 2025', 'comentario': 'Me ha ayudado muchísimo post-entrenamiento.'}, {'usuario': 'Marta L.', 'estrellas': 5, 'estrellas_range': range(5), 'fecha': '18 Nov 2025', 'comentario': 'Muy preciso, igual que el del médico.'}])
        ]
    }
    
    # Buscar el producto
    categoria_productos = productos_db.get(categoria, [])
    producto = next((p for p in categoria_productos if p['id'] == producto_id), None)
    
    if not producto:
        messages.error(request, 'Producto no encontrado')
        return redirect('ventas:index')
    
    # Calcular precio final si hay descuento
    if producto['descuento'] > 0:
        precio_final = producto['precio'] * (1 - producto['descuento'] / 100)
        producto['precio_final'] = round(precio_final, 2)
        producto['ahorro'] = round(producto['precio'] - precio_final, 2)
    
    # Obtener URL de categoría
    categorias_urls = {
        'belleza': 'ventas:belleza',
        'tecnologia': 'ventas:tecnologia',
        'electrodomesticos': 'ventas:electrodomesticos',
        'ferreteria': 'ventas:ferreteria',
        'bebe': 'ventas:bebe',
        'aire_libre': 'ventas:aire_libre',
        'entretenimiento': 'ventas:entretenimiento',
        'salud': 'ventas:salud'
    }
    
    # Productos relacionados (otros productos de la misma categoría)
    productos_relacionados = [p for p in categoria_productos if p['id'] != producto_id][:4]
    for p in productos_relacionados:
        p['url'] = f'/detalle/{categoria}/{p["id"]}/'
    
    context = {
        'producto': producto,
        'categoria_url': categorias_urls.get(categoria, 'ventas:index'),
        'productos_relacionados': productos_relacionados
    }
    
    return render(request, 'ventas/detalle_producto.html', context)


@login_required
@require_POST
def agregar_favorito(request):
    """Vista para agregar un producto a favoritos (AJAX)"""
    try:
        producto_id = int(request.POST.get('producto_id'))
        producto_nombre = request.POST.get('producto_nombre')
        producto_precio = float(request.POST.get('producto_precio'))
        producto_descuento = int(request.POST.get('producto_descuento', 0))
        producto_imagen = request.POST.get('producto_imagen')
        producto_categoria = request.POST.get('producto_categoria')
        
        # Crear o verificar si ya existe
        favorito, created = Favorito.objects.get_or_create(
            user=request.user,
            producto_id=producto_id,
            producto_categoria=producto_categoria,
            defaults={
                'producto_nombre': producto_nombre,
                'producto_precio': producto_precio,
                'producto_descuento': producto_descuento,
                'producto_imagen': producto_imagen
            }
        )
        
        if created:
            return JsonResponse({'status': 'success', 'message': '¡Producto agregado a favoritos!', 'action': 'added'})
        else:
            return JsonResponse({'status': 'info', 'message': 'Este producto ya está en tus favoritos', 'action': 'exists'})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def quitar_favorito(request):
    """Vista para quitar un producto de favoritos (AJAX)"""
    try:
        producto_id = int(request.POST.get('producto_id'))
        producto_categoria = request.POST.get('producto_categoria')
        
        favorito = Favorito.objects.filter(
            user=request.user,
            producto_id=producto_id,
            producto_categoria=producto_categoria
        ).first()
        
        if favorito:
            favorito.delete()
            return JsonResponse({'status': 'success', 'message': 'Producto eliminado de favoritos', 'action': 'removed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Producto no encontrado en favoritos'}, status=404)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def lista_favoritos(request):
    """Vista para mostrar la lista de favoritos del usuario"""
    favoritos = Favorito.objects.filter(user=request.user)
    
    # Calcular precio final para cada favorito
    for fav in favoritos:
        if fav.producto_descuento > 0:
            precio_final = float(fav.producto_precio) * (1 - fav.producto_descuento / 100)
            fav.precio_final = round(precio_final, 2)
            fav.ahorro = round(float(fav.producto_precio) - precio_final, 2)
        else:
            fav.precio_final = float(fav.producto_precio)
            fav.ahorro = 0
    
    context = {
        'favoritos': favoritos,
        'total_favoritos': favoritos.count()
    }
    
    return render(request, 'ventas/favoritos.html', context)


@login_required
def checkout(request):
    """Vista para la página de checkout/pago"""
    perfil = request.user.perfil
    
    # Validar que el usuario tenga dirección completa
    if not perfil.direccion or not perfil.ciudad or not perfil.codigo_postal or not perfil.telefono:
        messages.warning(request, 'Por favor completa tu información de perfil antes de realizar un pedido')
        return redirect('ventas:editar_perfil')
    
    context = {
        'perfil': perfil,
        'metodos_pago': Pedido.METODO_PAGO_CHOICES
    }
    
    return render(request, 'ventas/checkout.html', context)


@login_required
@require_POST
def finalizar_compra(request):
    """Vista para finalizar la compra y crear el pedido"""
    try:
        import json
        
        # Obtener datos del carrito desde el POST
        carrito_json = request.POST.get('carrito')
        if not carrito_json:
            return JsonResponse({'status': 'error', 'message': 'El carrito está vacío'}, status=400)
        
        carrito = json.loads(carrito_json)
        
        if not carrito:
            return JsonResponse({'status': 'error', 'message': 'El carrito está vacío'}, status=400)
        
        # Obtener método de pago y notas
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        notas = request.POST.get('notas', '')
        
        # Obtener datos de envío del formulario (independientes del perfil)
        datos_envio_json = request.POST.get('datos_envio')
        if datos_envio_json:
            datos_envio = json.loads(datos_envio_json)
            direccion = datos_envio.get('direccion')
            ciudad = datos_envio.get('ciudad')
            codigo_postal = datos_envio.get('codigo_postal')
            telefono = datos_envio.get('telefono')
        else:
            # Fallback a datos del perfil si no se envían datos de envío
            perfil = request.user.perfil
            direccion = perfil.direccion
            ciudad = perfil.ciudad
            codigo_postal = perfil.codigo_postal
            telefono = perfil.telefono
        
        # Validar que haya dirección completa
        if not direccion or not ciudad or not codigo_postal or not telefono:
            return JsonResponse({
                'status': 'error',
                'message': 'Por favor completa todos los datos de envío antes de realizar el pedido'
            }, status=400)
        
        # Calcular el total
        total = 0
        for item in carrito:
            precio = float(item['precio'])
            descuento = int(item.get('descuento', 0))
            cantidad = int(item['cantidad'])
            
            if descuento > 0:
                precio_final = precio * (1 - descuento / 100)
            else:
                precio_final = precio
            
            total += precio_final * cantidad
        
        # Generar número de pedido único
        numero_pedido = f"PED-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        
        # Crear el pedido con los datos de envío del formulario
        pedido = Pedido.objects.create(
            user=request.user,
            numero_pedido=numero_pedido,
            total=round(total, 2),
            metodo_pago=metodo_pago,
            estado_pago=False,  # El pago está pendiente por defecto
            direccion_envio=direccion,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            telefono=telefono,
            estado='pendiente',
            notas=notas
        )
        
        # Crear los detalles del pedido
        for item in carrito:
            precio = float(item['precio'])
            descuento = int(item.get('descuento', 0))
            cantidad = int(item['cantidad'])
            
            if descuento > 0:
                precio_final = precio * (1 - descuento / 100)
            else:
                precio_final = precio
            
            subtotal = precio_final * cantidad
            
            # Descontar del stock
            try:
                producto_db = Producto.objects.get(producto_id=int(item.get('id', 0)))
                if producto_db.stock >= cantidad:
                    producto_db.stock -= cantidad
                    producto_db.save()
                else:
                    # Si no hay suficiente stock, continuar pero registrar advertencia
                    print(f"Advertencia: Stock insuficiente para {producto_db.nombre}. Stock actual: {producto_db.stock}, solicitado: {cantidad}")
            except Producto.DoesNotExist:
                # Si el producto no existe en la BD, continuar sin descontar
                print(f"Advertencia: Producto ID {item.get('id')} no encontrado en inventario")
            
            DetallePedido.objects.create(
                pedido=pedido,
                producto_id=int(item.get('id', 0)),
                producto_nombre=item['nombre'],
                producto_imagen=item['imagen'],
                producto_categoria=item.get('categoria', 'general'),
                precio_unitario=precio,
                descuento=descuento,
                cantidad=cantidad,
                subtotal=round(subtotal, 2)
            )
        
        # Enviar email de confirmación
        enviar_email_pedido(pedido)
        
        return JsonResponse({
            'status': 'success',
            'message': f'¡Pedido realizado con éxito! Número de pedido: {numero_pedido}',
            'numero_pedido': numero_pedido,
            'pedido_id': pedido.id
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error al procesar el pedido: {str(e)}'}, status=500)


@login_required
def mis_pedidos(request):
    """Vista para mostrar todos los pedidos del usuario"""
    # Excluir pedidos cancelados por defecto
    pedidos = Pedido.objects.filter(user=request.user).exclude(estado='cancelado').prefetch_related('items')
    
    # Agregar información adicional a cada pedido
    for pedido in pedidos:
        pedido.total_items = sum(item.cantidad for item in pedido.items.all())
    
    context = {
        'pedidos': pedidos,
        'total_pedidos': pedidos.count()
    }
    
    return render(request, 'ventas/mis_pedidos.html', context)


@login_required
def detalle_pedido(request, pedido_id):
    """Vista para mostrar el detalle de un pedido específico"""
    try:
        pedido = Pedido.objects.get(id=pedido_id, user=request.user)
        items = pedido.items.all()
        
        # Calcular totales
        subtotal = sum(item.subtotal for item in items)
        total_items = sum(item.cantidad for item in items)
        
        context = {
            'pedido': pedido,
            'items': items,
            'subtotal': subtotal,
            'total_items': total_items
        }
        
        return render(request, 'ventas/detalle_pedido.html', context)
    
    except Pedido.DoesNotExist:
        messages.error(request, 'Pedido no encontrado')
        return redirect('ventas:mis_pedidos')


@login_required
@require_POST
def cancelar_pedido(request, pedido_id):
    """Vista para cancelar un pedido"""
    try:
        pedido = Pedido.objects.get(id=pedido_id, user=request.user)
        
        # Solo se pueden cancelar pedidos pendientes o en procesamiento
        if pedido.estado not in ['pendiente', 'procesando']:
            return JsonResponse({
                'status': 'error',
                'message': f'No puedes cancelar un pedido que ya está {pedido.estado}'
            }, status=400)
        
        # Cambiar estado a cancelado
        pedido.estado = 'cancelado'
        pedido.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'El pedido {pedido.numero_pedido} ha sido cancelado exitosamente'
        })
    
    except Pedido.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Pedido no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error al cancelar el pedido: {str(e)}'
        }, status=500)


@login_required
@require_POST
def crear_preferencia_mercadopago(request):
    """Vista para crear una preferencia de pago en Mercado Pago"""
    try:
        # Verificar que las credenciales de Mercado Pago estén configuradas
        if not settings.MERCADOPAGO_ACCESS_TOKEN or settings.MERCADOPAGO_ACCESS_TOKEN == '':
            return JsonResponse({
                'status': 'error',
                'message': 'Mercado Pago no está configurado. Por favor contacta al administrador.'
            }, status=500)
        
        # Obtener datos del carrito y datos de envío
        carrito_json = request.POST.get('carrito')
        if not carrito_json:
            return JsonResponse({'status': 'error', 'message': 'El carrito está vacío'}, status=400)
        
        carrito = json.loads(carrito_json)
        
        if not carrito:
            return JsonResponse({'status': 'error', 'message': 'El carrito está vacío'}, status=400)
        
        # Obtener datos de envío del formulario o del perfil
        datos_envio_json = request.POST.get('datos_envio')
        perfil = request.user.perfil
        
        if datos_envio_json:
            datos_envio = json.loads(datos_envio_json)
            direccion = datos_envio.get('direccion') or perfil.direccion
            ciudad = datos_envio.get('ciudad') or perfil.ciudad
            codigo_postal = datos_envio.get('codigo_postal') or perfil.codigo_postal
            telefono = datos_envio.get('telefono') or perfil.telefono
        else:
            direccion = perfil.direccion
            ciudad = perfil.ciudad
            codigo_postal = perfil.codigo_postal
            telefono = perfil.telefono
        
        # Validar que haya información completa
        if not direccion or not ciudad or not codigo_postal or not telefono:
            return JsonResponse({
                'status': 'error',
                'message': 'Por favor completa todos los datos de envío antes de realizar el pedido'
            }, status=400)
        
        # Inicializar SDK de Mercado Pago
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        
        # Crear items para Mercado Pago
        items = []
        total = 0
        
        for item in carrito:
            precio = float(item['precio'])
            descuento = int(item.get('descuento', 0))
            cantidad = int(item['cantidad'])
            
            if descuento > 0:
                precio_final = precio * (1 - descuento / 100)
            else:
                precio_final = precio
            
            items.append({
                "title": item['nombre'],
                "quantity": cantidad,
                "unit_price": float(round(precio_final, 2)),
                "currency_id": "UYU"  # Peso uruguayo
            })
            
            total += precio_final * cantidad
        
        # Crear preferencia de pago con los datos de envío del formulario
        preference_data = {
            "items": items,
            "payer": {
                "name": request.user.first_name or request.user.username,
                "email": request.user.email or f"{request.user.username}@example.com",
                "phone": {
                    "number": str(telefono)
                },
                "address": {
                    "street_name": str(direccion)[:256],
                    "zip_code": str(codigo_postal)
                }
            },
            "back_urls": {
                "success": request.build_absolute_uri(reverse('ventas:pago_exitoso')),
                "failure": request.build_absolute_uri(reverse('ventas:pago_fallido')),
                "pending": request.build_absolute_uri(reverse('ventas:pago_pendiente'))
            },
            "statement_descriptor": "SUPERVENTAS",
            "external_reference": f"{request.user.id}_{uuid.uuid4().hex[:8]}"
        }
        
        # En desarrollo local (localhost), no incluir notification_url
        # porque Mercado Pago requiere una URL pública accesible
        # En producción, descomentar la siguiente línea:
        # preference_data["notification_url"] = request.build_absolute_uri(reverse('ventas:webhook_mercadopago'))
        
        print("=== Creando preferencia de Mercado Pago ===")
        print(f"Items: {len(items)}")
        print(f"Total: ${total}")
        print(f"Success URL: {preference_data['back_urls']['success']}")
        print(f"Failure URL: {preference_data['back_urls']['failure']}")
        print(f"Pending URL: {preference_data['back_urls']['pending']}")
        
        # Crear la preferencia con URLs corregidas
        preference_response = sdk.preference().create(preference_data)
        
        print(f"Respuesta de MP: {preference_response}")
        
        preference = preference_response.get("response")
        status_code = preference_response.get("status")
        
        if status_code == 201 and preference:
            return JsonResponse({
                'status': 'success',
                'preference_id': preference.get('id'),
                'init_point': preference.get('init_point'),
                'sandbox_init_point': preference.get('sandbox_init_point')
            })
        else:
            error_message = preference_response.get('response', {}).get('message', 'Error desconocido')
            print(f"Error de MP: {error_message}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error al crear la preferencia de pago: {error_message}'
            }, status=500)
    
    except json.JSONDecodeError as e:
        print(f"Error JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error al procesar el carrito'}, status=400)
    except json.JSONDecodeError as e:
        print(f"Error JSON: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Error al procesar el carrito'}, status=400)
    except Exception as e:
        print(f"Error en crear_preferencia_mercadopago: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'}, status=500)


@login_required
def pago_exitoso(request):
    """Vista para cuando el pago es exitoso"""
    # Obtener datos de Mercado Pago
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    
    if status == 'approved' and external_reference:
        # Aquí deberías crear el pedido con los datos del carrito guardados
        messages.success(request, f'¡Pago exitoso! ID de pago: {payment_id}')
    else:
        messages.warning(request, 'El pago está siendo procesado')
    
    return redirect('ventas:mis_pedidos')


@login_required
def test_mercadopago_config(request):
    """Vista para probar la configuración de Mercado Pago"""
    config_status = {
        'access_token_configurado': bool(settings.MERCADOPAGO_ACCESS_TOKEN),
        'public_key_configurado': bool(settings.MERCADOPAGO_PUBLIC_KEY),
        'access_token_preview': settings.MERCADOPAGO_ACCESS_TOKEN[:20] + '...' if settings.MERCADOPAGO_ACCESS_TOKEN else 'NO CONFIGURADO',
        'public_key_preview': settings.MERCADOPAGO_PUBLIC_KEY[:20] + '...' if settings.MERCADOPAGO_PUBLIC_KEY else 'NO CONFIGURADO',
    }
    
    # Intentar inicializar SDK
    try:
        if settings.MERCADOPAGO_ACCESS_TOKEN:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            config_status['sdk_inicializado'] = True
            config_status['mensaje'] = '✅ Mercado Pago está correctamente configurado'
        else:
            config_status['sdk_inicializado'] = False
            config_status['mensaje'] = '❌ Falta configurar ACCESS_TOKEN'
    except Exception as e:
        config_status['sdk_inicializado'] = False
        config_status['mensaje'] = f'❌ Error: {str(e)}'
    
    return JsonResponse(config_status)


@login_required
def pago_fallido(request):
    """Vista para cuando el pago falla"""
    messages.error(request, 'El pago no pudo ser procesado. Por favor intenta nuevamente.')
    return redirect('ventas:carrito')


@login_required
def pago_pendiente(request):
    """Vista para cuando el pago está pendiente"""
    messages.info(request, 'Tu pago está pendiente de confirmación. Te notificaremos cuando se complete.')
    return redirect('ventas:mis_pedidos')


@csrf_exempt
@require_POST
def webhook_mercadopago(request):
    """Webhook para recibir notificaciones de Mercado Pago"""
    try:
        data = json.loads(request.body)
        
        # Mercado Pago envía notificaciones sobre pagos
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            
            # Inicializar SDK
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            
            # Obtener información del pago
            payment_info = sdk.payment().get(payment_id)
            payment = payment_info['response']
            
            if payment['status'] == 'approved':
                # Obtener external_reference para identificar el pedido
                external_reference = payment.get('external_reference')
                
                if external_reference:
                    # Aquí deberías actualizar el estado del pedido
                    # Por ahora solo logueamos
                    print(f"Pago aprobado: {payment_id}, referencia: {external_reference}")
            
        return JsonResponse({'status': 'ok'})
    
    except Exception as e:
        print(f"Error en webhook_mercadopago: {str(e)}")
        return JsonResponse({'status': 'error'}, status=400)


# ============================================
# VISTAS PARA STRIPE (Pago con Tarjeta)
# ============================================

@login_required
@require_POST
def crear_checkout_stripe(request):
    """Crear sesión de checkout de Stripe"""
    try:
        # Configurar Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        if not stripe.api_key:
            return JsonResponse({
                'status': 'error',
                'message': 'Stripe no está configurado. Por favor contacta al administrador.'
            })
        
        # Obtener datos del carrito, método de pago y datos de envío
        carrito_json = request.POST.get('carrito', '[]')
        carrito = json.loads(carrito_json)
        metodo_pago = request.POST.get('metodo_pago', 'stripe')
        datos_envio_json = request.POST.get('datos_envio', '{}')
        
        if not carrito:
            return JsonResponse({
                'status': 'error',
                'message': 'El carrito está vacío'
            })
        
        # Crear items para Stripe
        line_items = []
        for item in carrito:
            # Stripe requiere el precio en centavos
            precio_centavos = int(float(item['precioFinal']) * 100)
            
            line_items.append({
                'price_data': {
                    'currency': 'uyu',  # Pesos uruguayos
                    'product_data': {
                        'name': item['nombre'],
                        'images': [request.build_absolute_uri(item['imagen'])],
                    },
                    'unit_amount': precio_centavos,
                },
                'quantity': int(item['cantidad']),
            })
        
        # Crear sesión de checkout
        # Nota: Google Pay se habilita automáticamente con 'card' cuando el navegador lo soporta
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card', 'link'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('ventas:pago_exitoso_stripe')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('ventas:checkout')),
            customer_email=request.user.email,
            metadata={
                'user_id': request.user.id,
                'carrito': carrito_json,
                'metodo_pago': metodo_pago,
                'datos_envio': datos_envio_json,
            }
        )
        
        return JsonResponse({
            'status': 'success',
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id
        })
    
    except Exception as e:
        print(f"Error creando checkout de Stripe: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': f'Error al procesar el pago: {str(e)}'
        })


@login_required
def pago_exitoso_stripe(request):
    """Vista cuando el pago con Stripe es exitoso"""
    session_id = request.GET.get('session_id')
    
    if not session_id:
        messages.error(request, 'No se pudo verificar el pago')
        return redirect('ventas:carrito')
    
    try:
        # Configurar Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Obtener la sesión de checkout
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            # Recuperar el carrito, método de pago y datos de envío del metadata
            carrito_json = session.metadata.get('carrito')
            carrito = json.loads(carrito_json)
            metodo_pago = session.metadata.get('metodo_pago', 'tarjeta')
            datos_envio_json = session.metadata.get('datos_envio', '{}')
            datos_envio = json.loads(datos_envio_json)
            
            # Usar datos de envío del formulario o fallback al perfil
            perfil = request.user.perfil
            direccion = datos_envio.get('direccion') or perfil.direccion or 'No especificada'
            ciudad = datos_envio.get('ciudad') or perfil.ciudad or 'No especificada'
            codigo_postal = datos_envio.get('codigo_postal') or perfil.codigo_postal or '00000'
            telefono = datos_envio.get('telefono') or perfil.telefono or 'No especificado'
            
            total = sum(float(item['precioFinal']) * int(item['cantidad']) for item in carrito)
            
            pedido = Pedido.objects.create(
                usuario=request.user,
                direccion_envio=direccion,
                ciudad=ciudad,
                codigo_postal=codigo_postal,
                telefono=telefono,
                total=total,
                metodo_pago=metodo_pago,
                estado_pago=True,  # Ya está pagado
                estado='procesando',
                notas=f'Pago con Stripe - Session ID: {session_id}'
            )
            
            # Crear detalles del pedido
            for item in carrito:
                # Descontar del stock
                try:
                    producto_db = Producto.objects.get(producto_id=int(item.get('id', 0)))
                    cantidad = int(item['cantidad'])
                    if producto_db.stock >= cantidad:
                        producto_db.stock -= cantidad
                        producto_db.save()
                    else:
                        print(f"Advertencia: Stock insuficiente para {producto_db.nombre}. Stock actual: {producto_db.stock}, solicitado: {cantidad}")
                except Producto.DoesNotExist:
                    print(f"Advertencia: Producto ID {item.get('id')} no encontrado en inventario")
                
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto_id=int(item.get('id', 0)),
                    producto_nombre=item['nombre'],
                    producto_imagen=item['imagen'],
                    producto_categoria=item['categoria'],
                    cantidad=int(item['cantidad']),
                    precio_unitario=float(item['precio']),
                    descuento=int(item.get('descuento', 0)),
                    subtotal=float(item['precioFinal']) * int(item['cantidad'])
                )
            
            # Enviar email de confirmación
            enviar_email_pedido(pedido)
            
            messages.success(request, f'¡Pago exitoso! Tu pedido #{pedido.numero_pedido} ha sido confirmado.')
            return redirect('ventas:detalle_pedido', pedido_id=pedido.id)
        else:
            messages.warning(request, 'El pago aún está siendo procesado.')
            return redirect('ventas:mis_pedidos')
            
    except Exception as e:
        print(f"Error verificando pago de Stripe: {str(e)}")
        messages.error(request, 'Hubo un error al verificar el pago')
        return redirect('ventas:carrito')


def test_stripe_config(request):
    """Verificar si Stripe está configurado correctamente"""
    configurado = bool(settings.STRIPE_PUBLIC_KEY and settings.STRIPE_SECRET_KEY)
    
    return JsonResponse({
        'stripe_configurado': configurado,
        'public_key': settings.STRIPE_PUBLIC_KEY if configurado else None
    })
