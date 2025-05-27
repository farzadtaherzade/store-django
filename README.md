# 📚 Django Bookstore

A simple bookstore web application built with **Django**, featuring:

* 📦 Product management via Django Admin
* ✉️ Email alerts for low stock using Celery
* 🐇 Background task queue with RabbitMQ
* 🧪 Email testing with smtp4dev
* 🐳 Full containerization with Docker Compose

---

## 👱️ Tech Stack

* **Django** – Web framework
* **Celery** – Task queue for background jobs
* **RabbitMQ** – Message broker for Celery
* **smtp4dev** – Development SMTP server
* **Docker Compose** – Multi-service orchestration

---

## 🚀 Getting Started

Follow these steps to run the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/bookstore.git
cd bookstore
```

### 2. Copy environment variables

```bash
cp .env.example .env
```

Make sure the following variables exist in `.env`:

```env
EMAIL_HOST=smtp4dev
EMAIL_PORT=25
CELERY_BROKER_URL=amqp://rabbitmq
```

### 3. Run the project with Docker Compose

```bash
docker compose up --build
```

---

## 🌐 Services & Ports

| Service      | URL                                                        | Notes                          |
| ------------ | ---------------------------------------------------------- | ------------------------------ |
| Django App   | [http://localhost:8000](http://localhost:8000)             | Main website                   |
| Django Admin | [http://localhost:8000/admin](http://localhost:8000/admin) | Manage books & stock           |
| smtp4dev UI  | [http://localhost:5000](http://localhost:5000)             | View test emails               |
| RabbitMQ UI  | [http://localhost:15672](http://localhost:15672)           | Username/password: guest/guest |

---

## 🔁 How Low Stock Email Alerts Work

1. You change a book's stock in Django Admin.
2. If the stock is below a threshold, a Celery task is triggered.
3. An email is sent to notify the manager.
4. The email can be viewed in the smtp4dev web interface.

---

## 🔪 Optional: Run Migrations or Create Superuser

If you need to access the Django admin:

```bash
docker compose exec django-app python manage.py createsuperuser
```

---

## ✅ To Do


---

## 📄 License

This project is licensed under the MIT License.
