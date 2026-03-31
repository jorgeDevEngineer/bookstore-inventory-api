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