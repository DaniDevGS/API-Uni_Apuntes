# SaaS Academic API (IUTIRLA)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](./LICENSE)

[Versión en Español](./README-es.md)

This is a robust API built with Django and Django REST Framework designed to manage student academic performance, specifically tailored to the IUTIRLA institutional rules.

## 🚀 Key Features

- **Real Multitenancy:** Secured data isolation for every student using `request.user`.
- **Stats Dashboard:** Automatic calculations of global averages, best subjects per trimester, and academic statuses (Passed, Recovery, Failed).
- **IUTIRLA Logic:** Automatic management of 4 "cortes" (25% each) and evaluation summations.
- **Library Module:** Dynamic file uploads (PDF/Images) organized by user and subject folders.
- **File Optimization:** Automatic Signals to delete obsolete or orphan files from the server/Cloudinary.
- **Security:** JWT (JSON Web Tokens) Authentication.

## 🛠 Tech Stack

- **Language:** Python 3.13+
- **Framework:** Django 5.2
- **API:** Django REST Framework (DRF)
- **Database:** PostgreSQL (Production) / SQLite (Local)
- **Storage:** Cloudinary (Media in Production)
- **Server:** Gunicorn & WhiteNoise

## 📦 Setup & Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repo>
    cd API_Movil
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # Windows
    source venv/bin/activate # Linux/Mac
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the root directory:

    ```env
    SECRET_KEY=your_secret
    DEBUG=True
    DATABASE_URL=postgres://user:pass@host:port/dbname
    CLOUDINARY_CLOUD_NAME=your_name
    CLOUDINARY_API_KEY=your_key
    CLOUDINARY_API_SECRET=your_secret
    ```

5.  **Migrate & Run:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## 🔗 Main Endpoints

| Route                          | Description               |
| :----------------------------- | :------------------------ |
| `/api/auth/login/`             | Obtain JWT Token          |
| `/api/estadisticas/dashboard/` | "Magic" performance data  |
| `/api/materias/`               | Manage user subjects      |
| `/api/apuntes/`                | File library (PDF/Images) |

## ⚖️ License

**PROPRIETARY PROPERTY.** All rights reserved by Daniel David. Unauthorized distribution, manipulation, or reproduction of this code is strictly prohibited without express written consent.
