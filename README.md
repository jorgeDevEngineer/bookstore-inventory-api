# 📚 Nextep - Bookstore Inventory API

Una solución robusta y moderna para la gestión de inventarios de librerías, construida con **Django 5.0** y **Django REST Framework**. Este proyecto permite administrar libros, controlar existencias y automatizar el cálculo de precios mediante la integración con APIs de tasas de cambio en tiempo real.

---

## ✨ Características Principales

*   **Gestión Completa (CRUD):** Registro, actualización, listado y eliminación de libros del inventario.
*   **Validación de Datos:** Validación rigurosa de formatos ISBN (10 o 13 dígitos) y prevención de duplicados.
*   **Cálculo de Precios Automatizado:** Integración con *ExchangeRate-API* para convertir costos de USD a moneda local (EUR) aplicando márgenes de ganancia configurables (40%).
*   **Filtros de Búsqueda:** Búsqueda avanzada por categoría con soporte para coincidencias parciales.
*   **Control de Stock:** Endpoint especializado para identificar productos con bajo inventario basado en umbrales dinámicos.
*   **Paginación:** Respuestas optimizadas con paginación integrada para grandes volúmenes de datos.
*   **Dockerizado:** Configuración lista para desplegar en cualquier entorno mediante contenedores.

---

## 🛠️ Tecnologías Utilizadas

*   **Python 3.11** - Lenguaje base.
*   **Django 5.0** - Web Framework.
*   **Django REST Framework 3.14** - Toolkit para la construcción de la API.
*   **Requests** - Interacción con APIs externas.
*   **Docker & Docker Compose** - Contenerización y orquestación.
*   **SQLite** - Base de datos ligera (por defecto).

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local sin necesidad de instalar dependencias globales:

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd bookstore-inventory-api
```

### 2. Levantar el entorno con Docker
Este comando construirá la imagen y levantará el contenedor de la API:
```bash
docker-compose up --build
```

### 3. Ejecutar Migraciones (Primer inicio)
En una nueva terminal, crea las tablas necesarias en la base de datos:
```bash
docker-compose exec web python manage.py migrate
```

### 4. Crear Superusuario (Opcional - para el Admin)
Si deseas acceder al panel de administración de Django:
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Acceder a la aplicación
*   **API Principal:** [http://localhost:8000/api/books/](http://localhost:8000/api/books/)
*   **Django Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📖 Documentación de Endpoints

### 📚 Libros (Inventory)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/books/` | Listar libros (paginado) |
| `POST` | `/api/books/` | Crear un nuevo libro |
| `GET` | `/api/books/{id}/` | Detalle de un libro |
| `PUT` | `/api/books/{id}/` | Actualización total |
| `PATCH` | `/api/books/{id}/` | Actualización parcial |
| `DELETE` | `/api/books/{id}/` | Eliminar libro |

### 🔍 Funciones Especiales
| Método | Endpoint | Acción |
| :--- | :--- | :--- |
| `GET` | `/api/books/?category={nombre}` | Buscar por categoría (parcial/case-insensitive) |
| `GET` | `/api/books/low-stock/?threshold=5` | Listar libros con existencias ≤ al umbral |
| `POST` | `/api/books/{id}/calculate-price/` | Calcula e inyecta el precio de venta local basado en API externa |

---

## 📮 Pruebas con Postman

Se incluye una colección de Postman preconfigurada para facilitar las pruebas de todos los endpoints:
📄 `Nextep - Bookstore Inventory API.postman_collection.json`

Solo importa el archivo en Postman y asegúrate de que el contenedor esté corriendo.

---

## 📝 Notas de Implementación

1.  **Manejo de Moneda:** Si la API externa de tasas de cambio no está disponible, el sistema utiliza un *fallback* automático (0.85 EUR/USD) para garantizar la continuidad operativa.
2.  **Precisión Matemática:** Se utiliza el tipo de dato `Decimal` en toda la lógica financiera para evitar errores de precisión de punto flotante.
3.  **Seguridad:** Los campos `created_at`, `updated_at` y `selling_price_local` son de solo lectura mediante el serializador para proteger la integridad de los datos.

---
© 2026 Nextep Solutions.