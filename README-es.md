# API Académica SaaS (IUTIRLA)

[![Versión](https://img.shields.io/badge/versión-1.0.0-blue.svg)](https://github.com/)
[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![Licencia](https://img.shields.io/badge/licencia-Privada-red.svg)](./LICENSE)

[English Version](./README.md)

Esta es una API robusta construida con Django y Django REST Framework diseñada para gestionar el rendimiento académico de estudiantes, específicamente adaptada a las reglas institucionales del IUTIRLA.

## 🚀 Características Principales

- **Multitenancy Real:** Los datos de cada estudiante están aislados de forma segura mediante `request.user`.
- **Dashboard de Estadísticas:** Cálculos automáticos de promedios globales, mejores materias por trimestre y estados académicos (Aprobada, Recuperatorio, Reprobada).
- **Lógica IUTIRLA:** Manejo automático de 4 cortes (25% cada uno) y sumatorias de evaluaciones.
- **Módulo de Biblioteca:** Subida dinámica de archivos (PDF/Imágenes) organizada por usuario y materia.
- **Optimización de Archivos:** Signals automáticas para borrar archivos obsoletos o huérfanos del servidor/Cloudinary.
- **Seguridad:** Autenticación vía JWT (JSON Web Tokens).

## 🛠 Entorno Tecnológico

- **Lenguaje:** Python 3.13+
- **Framework:** Django 5.2
- **API:** Django REST Framework (DRF)
- **Base de Datos:** PostgreSQL (Producción) / SQLite (Local)
- **Almacenamiento:** Cloudinary (Media en Producción)
- **Servidor:** Gunicorn & WhiteNoise

## 📦 Instalación y Configuración

1.  **Clonar el repositorio:**

    ```bash
    git clone <tu-repositorio>
    cd API_Movil
    ```

2.  **Crear entorno virtual:**

    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # Windows
    source venv/bin/activate # Linux/Mac
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz y añade:

    ```env
    SECRET_KEY=tu_secreto
    DEBUG=True
    DATABASE_URL=postgres://user:pass@host:port/dbname
    CLOUDINARY_CLOUD_NAME=tu_name
    CLOUDINARY_API_KEY=tu_key
    CLOUDINARY_API_SECRET=tu_secret
    ```

5.  **Migrar y Correr:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## 🔗 Endpoints Principales

| Ruta                           | Descripción                         |
| :----------------------------- | :---------------------------------- |
| `/api/auth/login/`             | Obtener token JWT                   |
| `/api/estadisticas/dashboard/` | Datos mágicos del rendimiento       |
| `/api/materias/`               | Gestión de materias del usuario     |
| `/api/apuntes/`                | Biblioteca de archivos PDF/Imágenes |

## ⚖️ Licencia

**PROPIEDAD PRIVADA.** Todos los derechos reservados por Daniel David. Queda estrictamente prohibida la distribución, manipulación o reproducción total o parcial de este código sin consentimiento expreso por escrito.
