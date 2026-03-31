import re
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
def validate_isbn(value):
    """
    Validador personalizado para asegurar que el ISBN tenga 10 o 13 dígitos[cite: 72].
    Ignora los guiones para el conteo.
    """
    digits_only = re.sub(r'\D', '', value)
    if len(digits_only) not in (10, 13):
        raise ValidationError('El ISBN debe tener exactamente 10 o 13 dígitos.')

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    
    # unique=True garantiza que no se permitan libros duplicados con el mismo ISBN [cite: 73]
    isbn = models.CharField(max_length=20, unique=True, validators=[validate_isbn])
    
    # cost_usd debe ser mayor a 0 [cite: 70]
    cost_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)] 
    )
    
    # Puede ser null al inicio, ya que lo calcularemos después
    selling_price_local = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # stock_quantity no puede ser negativo [cite: 71]
    stock_quantity = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    
    category = models.CharField(max_length=100)
    supplier_country = models.CharField(max_length=2) # Ejemplo: "ES"
    
    # Campos de auditoría autogestionados por Django
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.isbn})"