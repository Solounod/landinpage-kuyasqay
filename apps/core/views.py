from django.shortcuts import render
from django.db.models import Prefetch
from .models import Category, Product, HeroImage, Review

def home(request):
    """
    Vista principal de la Landing Page.
    Altamente optimizada con Prefetch para evitar el problema de N+1 queries.
    """

    hero_images = HeroImage.objects.filter(is_active=True).order_by('order')
    active_products = Product.objects.filter(is_active=True).prefetch_related(
        'images',   # Carga las imágenes (ProductImage)
        'variants'  # Carga los precios/packs (ProductVariant)
    )

    categories = Category.objects.prefetch_related(
        Prefetch('products', queryset=active_products)
    ).order_by('order')

    reviews = Review.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'hero_images': hero_images,
        'categories': categories,
        'reviews': reviews,
    }

    return render(request, 'core/home.html', context)