# Nextep - Bookstore Inventory API

REST API for a bookstore inventory management system, including real-time price validation.

---

## 🚀 Prerequisites

To run this project locally without affecting your environment, you need to have the following installed:

- **Docker**
- **Docker Compose**

---

## ⚙️ Installation & Setup

The project is fully dockerized for easy deployment.

### 1. Clone the repository

```bash
git clone <repository-url>
cd bookstore-inventory-api
```

### 2. Build and run the containers

```bash
docker-compose up --build
```

### 3. Apply migrations

Open a new terminal and run:

```bash
docker-compose exec web python manage.py migrate
```

### 4. Access the API

The API will be available at:

[http://localhost:8000](http://localhost:8000)

---

## 📝 Notes

- It is necessary to run migrations before using the API.
- Ensure Docker is running correctly before starting.

---

## 🛠️ Endpoints de la API

### Libros (Inventory)
- [cite_start]**Listar todos:** `GET /api/books/` [cite: 38]
- [cite_start]**Crear libro:** `POST /api/books/` [cite: 37]
- [cite_start]**Detalle de libro:** `GET /api/books/<id>/` [cite: 38]
- [cite_start]**Búsqueda por categoría:** `GET /api/books/?category=Literatura` [cite: 42]
- [cite_start]**Stock Bajo:** `GET /api/books/low-stock/?threshold=5` [cite: 43]