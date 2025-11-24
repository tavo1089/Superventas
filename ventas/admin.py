from django.contrib import admin
from django.utils.html import format_html
from .models import Producto, Perfil, Favorito, Pedido, DetallePedido


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'descuento', 'stock_badge', 'activo', 'fecha_actualizacion']
    search_fields = ['nombre', 'categoria', 'producto_id']
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    list_editable = ['activo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('producto_id', 'nombre', 'categoria', 'descripcion', 'imagen_url', 'activo')
        }),
        ('Precios', {
            'fields': ('precio', 'descuento')
        }),
        ('Inventario', {
            'fields': ('stock', 'stock_minimo'),
            'description': 'Gestiona el stock disponible y el nivel mínimo de alerta'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_badge(self, obj):
        """Mostrar stock con colores según disponibilidad"""
        if obj.sin_stock:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 5px 12px; border-radius: 3px; font-weight: bold;">❌ SIN STOCK</span>'
            )
        elif obj.stock_bajo:
            return format_html(
                '<span style="background-color: #ff9800; color: white; padding: 5px 12px; border-radius: 3px; font-weight: bold;">⚠️ BAJO ({} unidades)</span>',
                obj.stock
            )
        else:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 5px 12px; border-radius: 3px; font-weight: bold;">✓ {} unidades</span>',
                obj.stock
            )
    stock_badge.short_description = 'Estado de Stock'
    stock_badge.admin_order_field = 'stock'
    
    # Acciones masivas
    actions = ['marcar_sin_stock', 'activar_productos', 'desactivar_productos']
    
    def marcar_sin_stock(self, request, queryset):
        updated = queryset.update(stock=0)
        self.message_user(request, f'{updated} producto(s) marcado(s) sin stock')
    marcar_sin_stock.short_description = '📦 Marcar como Sin Stock'
    
    def activar_productos(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(request, f'{updated} producto(s) activado(s)')
    activar_productos.short_description = '✅ Activar productos'
    
    def desactivar_productos(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(request, f'{updated} producto(s) desactivado(s)')
    desactivar_productos.short_description = '❌ Desactivar productos'


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono', 'ciudad', 'pais']
    search_fields = ['user__username', 'user__email', 'telefono', 'ciudad']
    list_filter = ['pais', 'ciudad']

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ['user', 'producto_nombre', 'producto_categoria', 'producto_precio', 'fecha_agregado']
    search_fields = ['user__username', 'producto_nombre', 'producto_categoria']
    list_filter = ['producto_categoria', 'fecha_agregado']
    readonly_fields = ['fecha_agregado']


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['producto_nombre', 'producto_imagen', 'producto_categoria', 'precio_unitario', 'descuento', 'cantidad', 'subtotal']
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'user', 'fecha_pedido', 'estado_badge', 'pago_badge', 'metodo_pago', 'total', 'ciudad']
    search_fields = ['numero_pedido', 'user__username', 'user__email', 'telefono', 'ciudad', 'direccion_envio']
    list_filter = ['estado', 'metodo_pago', 'estado_pago', 'fecha_pedido', 'ciudad']
    readonly_fields = ['numero_pedido', 'fecha_pedido', 'total', 'ver_detalles_envio']
    inlines = [DetallePedidoInline]
    date_hierarchy = 'fecha_pedido'
    list_per_page = 20
    
    # Acciones personalizadas
    actions = ['marcar_como_procesando', 'marcar_como_enviado', 'marcar_como_entregado']
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('numero_pedido', 'user', 'fecha_pedido', 'estado', 'total')
        }),
        ('Información de Pago', {
            'fields': ('metodo_pago', 'estado_pago')
        }),
        ('Información de Envío', {
            'fields': ('ver_detalles_envio', 'direccion_envio', 'ciudad', 'codigo_postal', 'telefono')
        }),
        ('Notas del Cliente', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    def estado_badge(self, obj):
        """Mostrar estado con colores"""
        colors = {
            'pendiente': '#6c757d',
            'procesando': '#17a2b8',
            'enviado': '#007bff',
            'entregado': '#28a745',
            'cancelado': '#dc3545',
        }
        color = colors.get(obj.estado, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def pago_badge(self, obj):
        """Mostrar estado de pago con colores"""
        if obj.estado_pago:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">✓ PAGADO</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #6c757d; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">⏳ PENDIENTE</span>'
            )
    pago_badge.short_description = 'Pago'
    
    def ver_detalles_envio(self, obj):
        """Mostrar detalles de envío formateados"""
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff;">'
            '<strong style="font-size: 14px;">📦 Información para el Envío</strong><br><br>'
            '<strong>Cliente:</strong> {}<br>'
            '<strong>Teléfono:</strong> <a href="tel:{}">{}</a><br>'
            '<strong>Email:</strong> <a href="mailto:{}">{}</a><br><br>'
            '<strong>Dirección:</strong><br>{}<br>'
            '<strong>Ciudad:</strong> {}<br>'
            '<strong>Código Postal:</strong> {}<br>'
            '</div>',
            obj.user.get_full_name() or obj.user.username,
            obj.telefono, obj.telefono,
            obj.user.email, obj.user.email,
            obj.direccion_envio,
            obj.ciudad,
            obj.codigo_postal
        )
    ver_detalles_envio.short_description = 'Datos de Envío'
    
    # Acciones masivas
    def marcar_como_procesando(self, request, queryset):
        updated = queryset.update(estado='procesando')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como PROCESANDO')
    marcar_como_procesando.short_description = '🔄 Marcar como Procesando'
    
    def marcar_como_enviado(self, request, queryset):
        updated = queryset.update(estado='enviado')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como ENVIADO')
    marcar_como_enviado.short_description = '📦 Marcar como Enviado'
    
    def marcar_como_entregado(self, request, queryset):
        updated = queryset.update(estado='entregado')
        self.message_user(request, f'{updated} pedido(s) marcado(s) como ENTREGADO')
    marcar_como_entregado.short_description = '✅ Marcar como Entregado'
    
    def get_list_display_links(self, request, list_display):
        return ['numero_pedido']
