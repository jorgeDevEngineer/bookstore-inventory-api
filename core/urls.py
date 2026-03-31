from django.contrib import admin
from django.urls import path, include # <-- Asegúrate de que 'include' esté importado

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí estamos diciendo: "Toda ruta que empiece con 'api/' mándala a inventory.urls"
    path('api/', include('inventory.urls')), 
]