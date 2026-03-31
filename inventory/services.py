import requests
from django.utils import timezone
from decimal import Decimal

class PriceCalculationService:
    # URL de la API externa solicitada en la prueba
    EXCHANGE_RATE_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
    
    # Regla de negocio: Margen de ganancia del 40%
    MARGIN_PERCENTAGE = Decimal('40.0')
    
    # Regla de negocio: Si la API falla, usamos esta tasa por defecto (ej. EUR)
    DEFAULT_EXCHANGE_RATE = Decimal('0.85')
    DEFAULT_CURRENCY = 'EUR'

    @classmethod
    def get_exchange_rate(cls):
        """
        Se conecta a la API externa para obtener la tasa de cambio.
        Si la API falla (timeout, error 500, etc.), retorna los valores por defecto.
        """
        try:
            # Agregamos un timeout de 5 segundos para no dejar colgada la petición
            response = requests.get(cls.EXCHANGE_RATE_API_URL, timeout=5)
            response.raise_for_status() # Lanza error si el status no es 200
            
            data = response.json()
            # Asumimos que queremos convertir a EUR (puedes cambiarlo si prefieres otra moneda local)
            rate = data['rates'].get('EUR')
            
            if rate:
                return Decimal(str(rate)), 'EUR'
            
        except requests.RequestException:
            # Si hay CUALQUIER error de red, usamos el fallback (regla de negocio cumplida)
            pass
            
        return cls.DEFAULT_EXCHANGE_RATE, cls.DEFAULT_CURRENCY

    @classmethod
    def calculate_and_update_price(cls, book):
        """
        Aplica la lógica matemática para calcular el precio final y lo guarda.
        """
        exchange_rate, currency = cls.get_exchange_rate()
        
        # 1. Costo en USD a Decimal para precisión matemática
        cost_usd = Decimal(str(book.cost_usd))
        
        # 2. Costo local = Costo USD * Tasa de cambio
        cost_local = round(cost_usd * exchange_rate, 2)
        
        # 3. Precio de venta = Costo Local * (1 + Margen/100)
        margin_multiplier = Decimal('1') + (cls.MARGIN_PERCENTAGE / Decimal('100'))
        selling_price_local = round(cost_local * margin_multiplier, 2)
        
        # 4. Actualiza la base de datos
        book.selling_price_local = selling_price_local
        book.save()
        
        # 5. Estructura la respuesta exacta que pide la prueba
        return {
            "book_id": book.id,
            "cost_usd": float(cost_usd),
            "exchange_rate": float(exchange_rate),
            "cost_local": float(cost_local),
            "margin_percentage": int(cls.MARGIN_PERCENTAGE),
            "selling_price_local": float(selling_price_local),
            "currency": currency,
            "calculation_timestamp": timezone.now().isoformat()
        }