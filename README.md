# 💰 Expense Tracker – Backend API

<p align="center">
  <img src="https://img.shields.io/badge/Django-Backend-green?style=for-the-badge&logo=django" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql" />
  <img src="https://img.shields.io/badge/Deployed-Render-purple?style=for-the-badge" />
</p>

---

## 🚀 Live API

🔗 https://expense-tracker-be-pomq.onrender.com

---

## 📌 Overview

This is the Django REST API backend for the Expense Tracker application.
It handles authentication, transaction management, analytics, and database operations.

---

## 🏗 Architecture

Frontend → Next.js (Vercel)
Backend → Django REST Framework (Render)
Database → PostgreSQL

🔗 Frontend Repository:
https://github.com/alfin-joseph/expense_tracker_fe

---

## ✨ Features

* 🔐 JWT Authentication (Login / Register)
* 📊 Monthly Summary API
* 📈 Analytics Endpoints
* 🗂 CRUD for Transactions
* 🔎 Filtering by Month / Year
* 🔒 Secure CORS Configuration
* ⚡ Production Deployment with Gunicorn

---

## 🛠 Tech Stack

* Django
* Django REST Framework
* Simple JWT
* PostgreSQL
* Gunicorn

---

## ⚙️ Environment Variables

SECRET_KEY=your_secret_key
DEBUG=False
DATABASE_URL=your_internal_database_url

---

## 🚀 Run Locally

git clone https://github.com/alfin-joseph/expense_tracker_be 

cd expense_tracker_be

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

---

## 📌 API Endpoints

| Method | Endpoint           | Description        |
| ------ | ------------------ | ------------------ |
| POST   | /api/register/     | Register user      |
| POST   | /api/login/        | Login              |
| GET    | /api/transactions/ | List transactions  |
| POST   | /api/transactions/ | Create transaction |
| GET    | /api/summary/      | Monthly summary    |

---

## 👨‍💻 Author

Alfin Joseph

If you found this project helpful, please ⭐ the repo!
