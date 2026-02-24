# apps/core/utils.py
import os
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile

def optimize_image(image_field, max_width=1200):
    """
    Redimensiona la imagen, corrige la rotación del celular y la convierte a formato WebP.
    """
    if not image_field or not hasattr(image_field, 'file'):
        return None
    
    img = Image.open(image_field)
    
    # Corrige la rotación
    img = ImageOps.exif_transpose(img)

    if img.mode in ("P", "CMYK"):
        img = img.convert("RGB")

    # Redimensionar
    if img.width > max_width:
        ratio = max_width / float(img.width)
        height = int((float(img.height) * float(ratio)))
        img = img.resize((max_width, height), Image.Resampling.LANCZOS)

    # Comprimir a Webp
    buffer = BytesIO()
    img.save(buffer, format="WEBP", quality=85, optimize=True)
    buffer.seek(0)
    #Renombrar el archivo para que termine en .webp
    filename = os.path.basename(image_field.name)
    name, _ = os.path.splitext(filename)
    new_filename = f"{name}.webp"

    return ContentFile(buffer.read(), name=new_filename)