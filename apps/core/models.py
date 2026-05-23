from django.db import models
from django.core.exceptions import ValidationError
from .utils import optimize_image

class TimeStampedModel(models.Model):
    """Modelo abstracto para guardar la fecha de creación y actualización."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        abstract = True

# 1. CARRUSEL PRINCIPAL (Hero)
class HeroImage(models.Model):
    title = models.CharField(max_length=100, blank=True, verbose_name="Título interno (opcional)")
    image = models.ImageField(upload_to='hero_gallery/', verbose_name="Imagen de Portada")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_active = models.BooleanField(default=True, verbose_name="¿Visible?")

    class Meta:
        verbose_name = "Imagen de Portada"
        verbose_name_plural = "Imágenes de Portada (Hero)"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.image and getattr(self.image, 'name', None):
            if not self.image.name.lower().endswith('.webp'):
                optimized_file = optimize_image(self.image, max_width=1600)
                if optimized_file:
                    self.image = optimized_file
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else f"Imagen Portada {self.id}"

# 2. CATEGORÍAS
class Category(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")
    slug = models.SlugField(unique=True, help_text="Ej: alfajores, tortas-a-pedido")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de aparición")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['order']

    def __str__(self):
        return self.name

# 3. PRODUCTOS
class Product(TimeStampedModel):
    COLOR_CHOICES = [
        ('bg-brand-cream', 'Crema (Clásico)'),
        ('bg-white', 'Blanco (Limpio)'),
        ('bg-brand-lightpurple', 'Lila Suave (Contraste)'),
        ('bg-brand-lila', 'Lila Fuerte (Acento)'),
        ('bg-[#efedea]', 'Gris Cálido (Minimalista)'),
    ]

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Categoría")
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    description = models.TextField(verbose_name="Descripción", blank=True)
    min_order = models.CharField(max_length=100, blank=True, verbose_name="Pedido Mínimo", help_text="Ej: 20 unidades")
    
    background_color = models.CharField(
        max_length=50,
        choices=COLOR_CHOICES,
        default='bg-brand-cream',
        verbose_name="Color de Fondo",
        help_text="Elige el color de fondo para la sección de este producto en la web."
    )

    is_active = models.BooleanField(default=True, verbose_name="¿Visible?")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

# 4. IMÁGENES DE PRODUCTOS (El Carrusel de cada producto)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_gallery/', verbose_name="Foto")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Galería del Producto"
        ordering = ['order']

    def __str__(self):
        return f"Imagen de {self.product.name}"

    def clean(self):
        if hasattr(self, 'product') and self.product_id:
            existing_images = ProductImage.objects.filter(product_id=self.product_id).count()
            if self.pk is None and existing_images >= 8:
                raise ValidationError("Límite alcanzado: Máximo 8 imágenes por carrusel")

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError:
            pass
        # OPTIMIZACIÓN DE IMAGEN
        if self.image:
            if not self.image.name.lower().endswith('.webp'):
                optimized_file = optimize_image(self.image, max_width=1200)
                if optimized_file:
                    self.image = optimized_file        
        
        super().save(*args, **kwargs)
# 5. PACKS / VARIANTES DE PRECIO
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Nombre del Pack", help_text="Ej: Pack 6 unidades")
    price = models.IntegerField(verbose_name="Precio", blank=True, null=True)
    
    class Meta:
        verbose_name = "Pack/Precio"
        verbose_name_plural = "Packs y Precios"
        ordering = ['price']

    def __str__(self):
        precio_str = f"${self.price}" if self.price else "A cotizar"
        return f"{self.product.name} - {self.name} ({precio_str})"

class Review(TimeStampedModel):
    client_name = models.CharField(max_length=100, verbose_name="Nombre/Tipo de Cliente", help_text="Ej: Javiera, Hospital de Talca")
    text = models.TextField(verbose_name="Comentario del cliente")
    image = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name="Foto del producto o captura")
    is_active = models.BooleanField(default=True, verbose_name="¿Visible?")

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas de Clientes"
        ordering = ['-created_at']

    
    def save(self, *args, **kwargs):
        if self.image and getattr(self.image, 'name', None):
            if not self.image.name.lower().endswith('.webp'):
                optimized_file = optimize_image(self.image, max_width=1600) 
                if optimized_file:
                    self.image = optimized_file
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reseña de {self.client_name}"