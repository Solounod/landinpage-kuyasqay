from django.contrib import admin
from .models import HeroImage, Category, Product, ProductImage, ProductVariant, Review

# --- INLINES ---
# Esto permite agregar variantes y fotos DENTRO de la pantalla del Producto

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Deja 1 fila vacía lista para llenar
    verbose_name = "Pack o Precio"
    verbose_name_plural = "Lista de Packs y Precios"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 8  # Límite de seguridad en el frontend del admin
    verbose_name = "Foto para el Carrusel"
    verbose_name_plural = "Galería de Imágenes (Máximo 8)"

# --- REGISTROS DE MODELOS ---

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'background_color')
    list_filter = ('category', 'is_active', 'background_color')
    search_fields = ('name', 'description')
    inlines = [ProductVariantInline, ProductImageInline]
    
    fields = ('category', 'name', 'description', 'background_color', 'min_order', 'is_active')
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)} # Autocompleta el slug al escribir el nombre
    ordering = ['order']

@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active') # Permite cambiar el orden sin entrar al detalle
    ordering = ['order']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('client_name', 'text')
