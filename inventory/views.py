from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .services import PriceCalculationService

class BookViewSet(viewsets.ModelViewSet):
    # Ordenamos por ID descendente para que la paginación sea consistente
    queryset = Book.objects.all().order_by('-id')
    serializer_class = BookSerializer

    # Endpoint Opcional: Buscar por categoría
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            # icontains ignora mayúsculas/minúsculas
            queryset = queryset.filter(category__icontains=category)
        return queryset

    # Endpoint Opcional: Libros con stock bajo
    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        # Obtenemos el threshold de la URL o usamos 10 por defecto
        try:
            threshold = int(self.request.query_params.get('threshold', 10))
        except ValueError:
            threshold = 10
            
        books = Book.objects.filter(stock_quantity__lte=threshold).order_by('stock_quantity')
        
        # Aplicamos paginación también a este endpoint personalizado
        page = self.paginate_queryset(books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='calculate-price')
    def calculate_price(self, request, pk=None):
        """
        Calcula el precio de venta sugerido basado en la API externa.
        """
        # self.get_object() busca el libro por el ID (pk). 
        # Si no existe, DRF lanza automáticamente un error 404 Not Found.
        book = self.get_object()

        try:
            # Delegamos la lógica matemática y de red a nuestro servicio
            result = PriceCalculationService.calculate_and_update_price(book)
            
            # Retornamos el cálculo detallado con la estructura exacta [cite: 54-68]
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            # Manejamos errores inesperados con un 500 Internal Server Error 
            return Response(
                {"error": "Ocurrió un error interno al calcular el precio.", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )