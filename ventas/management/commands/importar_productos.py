from django.core.management.base import BaseCommand
from ventas.models import Producto


class Command(BaseCommand):
    help = 'Importa todos los productos de las categorías a la base de datos'

    def handle(self, *args, **kwargs):
        # Base de datos completa de productos
        productos_data = []
        
        # Productos de Belleza
        productos_data.extend([
            {'id': 1, 'nombre': 'Crema Facial Hidratante', 'precio': 25.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
            {'id': 2, 'nombre': 'Set de Maquillaje Profesional', 'precio': 89.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
            {'id': 3, 'nombre': 'Perfume Elegance 100ml', 'precio': 65.00, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
            {'id': 4, 'nombre': 'Serum Anti-Edad', 'precio': 45.50, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
            {'id': 5, 'nombre': 'Plancha de Cabello Profesional', 'precio': 75.00, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
            {'id': 6, 'nombre': 'Kit de Cuidado de Uñas', 'precio': 35.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400&h=300&fit=crop', 'categoria': 'Belleza'},
        ])
        
        # Productos de Tecnología (offset 100)
        productos_data.extend([
            {'id': 101, 'nombre': 'Smartphone Galaxy Pro', 'precio': 899.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 102, 'nombre': 'Laptop Gaming RGB', 'precio': 1299.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 103, 'nombre': 'Tablet Pro 12"', 'precio': 599.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 104, 'nombre': 'Auriculares Bluetooth Premium', 'precio': 399.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 105, 'nombre': 'Smartwatch Ultra', 'precio': 399.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 106, 'nombre': 'Teclado Mecánico RGB', 'precio': 129.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 107, 'nombre': 'Mouse Gamer Inalámbrico', 'precio': 79.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
            {'id': 108, 'nombre': 'Monitor 4K Ultra HD 27"', 'precio': 499.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=300&fit=crop', 'categoria': 'Tecnología'},
        ])
        
        # Productos de Electrodomésticos (offset 200)
        productos_data.extend([
            {'id': 201, 'nombre': 'Refrigeradora Smart 500L', 'precio': 1499.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
            {'id': 202, 'nombre': 'Lavadora Automática 18kg', 'precio': 899.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
            {'id': 203, 'nombre': 'Microondas Digital 30L', 'precio': 199.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
            {'id': 204, 'nombre': 'Aspiradora Robot Inteligente', 'precio': 349.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
            {'id': 205, 'nombre': 'Licuadora Pro 2000W', 'precio': 129.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
            {'id': 206, 'nombre': 'Cafetera Espresso Automática', 'precio': 299.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=300&fit=crop', 'categoria': 'Electrodomésticos'},
        ])
        
        # Productos de Moda (offset 300)
        productos_data.extend([
            {'id': 301, 'nombre': 'Zapatillas Deportivas Running', 'precio': 89.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop', 'categoria': 'Moda'},
            {'id': 302, 'nombre': 'Chaqueta de Cuero Premium', 'precio': 199.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=300&fit=crop', 'categoria': 'Moda'},
            {'id': 303, 'nombre': 'Jeans Clásicos Slim Fit', 'precio': 59.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop', 'categoria': 'Moda'},
            {'id': 304, 'nombre': 'Vestido Elegante Noche', 'precio': 129.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400&h=300&fit=crop', 'categoria': 'Moda'},
            {'id': 305, 'nombre': 'Reloj Análogo Clásico', 'precio': 149.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop', 'categoria': 'Moda'},
            {'id': 306, 'nombre': 'Bolso de Mano Premium', 'precio': 179.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=300&fit=crop', 'categoria': 'Moda'},
        ])
        
        # Productos de Hogar (offset 400)
        productos_data.extend([
            {'id': 401, 'nombre': 'Juego de Sábanas King Size', 'precio': 79.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400&h=300&fit=crop', 'categoria': 'Hogar'},
            {'id': 402, 'nombre': 'Set de Toallas Premium 6 Piezas', 'precio': 49.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=400&h=300&fit=crop', 'categoria': 'Hogar'},
            {'id': 403, 'nombre': 'Lámpara de Pie Moderna', 'precio': 99.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=400&h=300&fit=crop', 'categoria': 'Hogar'},
            {'id': 404, 'nombre': 'Alfombra Decorativa 2x3m', 'precio': 159.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1600166898405-da9535204843?w=400&h=300&fit=crop', 'categoria': 'Hogar'},
            {'id': 405, 'nombre': 'Espejo Decorativo Grande', 'precio': 89.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=300&fit=crop', 'categoria': 'Hogar'},
            {'id': 406, 'nombre': 'Set de Vajilla 24 Piezas', 'precio': 129.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1578916171728-46686eac8d58?w=400&h=300&fit=crop', 'categoria': 'Hogar'},
        ])
        
        # Productos de Ferretería (offset 500)
        productos_data.extend([
            {'id': 501, 'nombre': 'Taladro Inalámbrico 20V', 'precio': 149.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1504148455328-c376907d081c?w=400&h=300&fit=crop', 'categoria': 'Ferretería y Construcción'},
            {'id': 502, 'nombre': 'Set de Herramientas 120 Piezas', 'precio': 89.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=400&h=300&fit=crop', 'categoria': 'Ferretería y Construcción'},
            {'id': 503, 'nombre': 'Sierra Circular Profesional', 'precio': 199.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1572981779307-38b8cabb2407?w=400&h=300&fit=crop', 'categoria': 'Ferretería y Construcción'},
            {'id': 504, 'nombre': 'Escalera Telescópica 5m', 'precio': 299.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1513467535987-fd81bc7d62f8?w=400&h=300&fit=crop', 'categoria': 'Ferretería y Construcción'},
            {'id': 505, 'nombre': 'Compresor de Aire', 'precio': 249.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1581092918056-0c4c3acd3789?w=400&h=300&fit=crop', 'categoria': 'Ferretería y Construcción'},
            {'id': 506, 'nombre': 'Nivel Láser Digital', 'precio': 129.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=400&h=300&fit=crop', 'categoria': 'Ferretería y Construcción'},
        ])
        
        # Productos de Bebé (offset 600)
        productos_data.extend([
            {'id': 601, 'nombre': 'Coche para Bebé Premium', 'precio': 349.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños'},
            {'id': 602, 'nombre': 'Cuna Convertible', 'precio': 299.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños'},
            {'id': 603, 'nombre': 'Monitor de Bebé con Cámara', 'precio': 129.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños'},
            {'id': 604, 'nombre': 'Set de Alimentación', 'precio': 45.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños'},
            {'id': 605, 'nombre': 'Juguete Educativo Musical', 'precio': 59.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1587818541473-f2e71229046f?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños'},
            {'id': 606, 'nombre': 'Pañalera de Viaje', 'precio': 79.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=300&fit=crop', 'categoria': 'Bebé y Niños'},
        ])
        
        # Productos de Aire Libre (offset 700)
        productos_data.extend([
            {'id': 701, 'nombre': 'Bicicleta de Montaña Pro', 'precio': 599.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1541625602330-2277a4c46182?w=400&h=300&fit=crop', 'categoria': 'Aire Libre'},
            {'id': 702, 'nombre': 'Carpa Camping 6 Personas', 'precio': 249.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=400&h=300&fit=crop', 'categoria': 'Aire Libre'},
            {'id': 703, 'nombre': 'Parrilla Portátil a Gas', 'precio': 179.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=300&fit=crop', 'categoria': 'Aire Libre'},
            {'id': 704, 'nombre': 'Set de Pesca Completo', 'precio': 129.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1502139214982-d0ad755818d8?w=400&h=300&fit=crop', 'categoria': 'Aire Libre'},
            {'id': 705, 'nombre': 'Mochila Trekking 50L', 'precio': 99.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop', 'categoria': 'Aire Libre'},
            {'id': 706, 'nombre': 'Kayak Inflable 2 Personas', 'precio': 399.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop', 'categoria': 'Aire Libre'},
        ])
        
        # Productos de Entretenimiento (offset 800)
        productos_data.extend([
            {'id': 801, 'nombre': 'Consola Gaming Next Gen', 'precio': 499.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1486401899868-0e435ed85128?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento'},
            {'id': 802, 'nombre': 'Smart TV 55" 4K', 'precio': 699.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento'},
            {'id': 803, 'nombre': 'Barra de Sonido Dolby', 'precio': 299.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento'},
            {'id': 804, 'nombre': 'Drone con Cámara 4K', 'precio': 449.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento'},
            {'id': 805, 'nombre': 'Guitarra Eléctrica', 'precio': 379.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento'},
            {'id': 806, 'nombre': 'Set de Juegos de Mesa', 'precio': 89.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop', 'categoria': 'Entretenimiento'},
        ])
        
        # Productos de Salud (offset 900)
        productos_data.extend([
            {'id': 901, 'nombre': 'Caminadora Eléctrica Pro', 'precio': 899.99, 'descuento': 20, 'imagen': 'https://images.unsplash.com/photo-1538805060514-97d9cc17730c?w=400&h=300&fit=crop', 'categoria': 'Salud y Bienestar'},
            {'id': 902, 'nombre': 'Set de Pesas Ajustables', 'precio': 199.99, 'descuento': 25, 'imagen': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop', 'categoria': 'Salud y Bienestar'},
            {'id': 903, 'nombre': 'Bicicleta Estática Smart', 'precio': 449.99, 'descuento': 15, 'imagen': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=400&h=300&fit=crop', 'categoria': 'Salud y Bienestar'},
            {'id': 904, 'nombre': 'Mat de Yoga Premium', 'precio': 49.99, 'descuento': 30, 'imagen': 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=400&h=300&fit=crop', 'categoria': 'Salud y Bienestar'},
            {'id': 905, 'nombre': 'Masajeador Eléctrico', 'precio': 129.99, 'descuento': 10, 'imagen': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop', 'categoria': 'Salud y Bienestar'},
            {'id': 906, 'nombre': 'Monitor de Presión Digital', 'precio': 69.99, 'descuento': 0, 'imagen': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=300&fit=crop', 'categoria': 'Salud y Bienestar'},
        ])
        
        # Contador de importaciones
        creados = 0
        actualizados = 0
        
        for producto_data in productos_data:
            producto, created = Producto.objects.update_or_create(
                producto_id=producto_data['id'],
                defaults={
                    'nombre': producto_data['nombre'],
                    'categoria': producto_data['categoria'],
                    'precio': producto_data['precio'],
                    'descuento': producto_data['descuento'],
                    'imagen_url': producto_data['imagen'],
                    'stock': 50,  # Stock inicial de 50 unidades
                    'stock_minimo': 10,  # Alerta cuando haya menos de 10
                    'activo': True,
                }
            )
            
            if created:
                creados += 1
            else:
                actualizados += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Importación completada:\n'
                f'   - {creados} productos creados\n'
                f'   - {actualizados} productos actualizados\n'
                f'   - Total: {len(productos_data)} productos'
            )
        )
