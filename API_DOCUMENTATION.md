# 📚 Documentación de la API - UniApuntes (DaniDevGS)

Esta documentación proporciona toda la información necesaria para que el equipo de Frontend pueda integrar y consumir los servicios de la API de UniApuntes.

## 🚀 Información General

- **Base URL:** `http://localhost:8000/` (o la URL de producción correspondiente)
- **Formato de Datos:** JSON
- **Codificación:** UTF-8

---

## 🔐 Autenticación

La API utiliza **JWT (JSON Web Tokens)** para manejar la autenticación. La mayoría de los endpoints requieren que el token se envíe en los encabezados de la solicitud.

### 1. Iniciar Sesión (Obtener Token)
- **URL:** `/api/auth/login/`
- **Método:** `POST`
- **Body:**
  ```json
  {
    "username": "tu_usuario",
    "password": "tu_password"
  }
  ```
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "refresh": "token_de_refresco",
    "access": "token_de_acceso"
  }
  ```

### 2. Refrescar Token
- **URL:** `/api/auth/refresh/`
- **Método:** `POST`
- **Body:**
  ```json
  {
    "refresh": "token_de_refresco_obtenido_en_login"
  }
  ```
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "access": "nuevo_token_de_acceso"
  }
  ```

> [!IMPORTANT]
> Para todas las peticiones protegidas, se debe incluir el encabezado:
> `Authorization: Bearer <tu_access_token>`

---

## ⚠️ Manejo de Errores

La API devuelve errores estandarizados según el código de estado HTTP:

- **400 Bad Request:** Error en los datos enviados (validación).
  ```json
  {
    "campo": ["Mensaje de error descriptivo"]
  }
  ```
- **401 Unauthorized:** El token es inválido o ha expirado.
- **403 Forbidden:** No tienes permiso para acceder a este recurso.
- **404 Not Found:** El recurso solicitado no existe o no pertenece al usuario.
- **500 Internal Server Error:** Error inesperado en el servidor.

---

## 📁 Módulos de la API

### 1. Gestión de Usuarios
Endpoint para registro y gestión de perfiles.

| Método | Endpoint | Acción | Privacidad |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/usuario/` | Registrar nuevo usuario | Público |
| `GET` | `/api/usuario/` | Listar usuarios | Público |
| `GET` | `/api/usuario/{id}/` | Detalle de usuario | Requiere Token |

---

### 2. Dashboard de Estadísticas (Especial)
Este endpoint centraliza toda la información analítica que necesita el Dashboard principal.

- **URL:** `/api/estadisticas/dashboard/`
- **Método:** `GET`
- **Respuesta (200 OK):**
  ```json
  {
    "promedio_global": 48.5,
    "materias_aprobadas": 5,
    "materias_peligro": 2,
    "materias_reprobadas": 1,
    "mejor_materia_absoluta": "Matemática discreta",
    "mejores_materias_por_trimestre": [
      {
        "trimestre": 1,
        "materia_nombre": "Programación I",
        "nota_final": 95.0
      }
    ],
    "detalle_materias": [
      {
        "materia_id": 12,
        "nombre": "Estructura de Datos",
        "nota_final": 52.0,
        "estado": "Aprobada",
        "cortes": [
          { "corte_numero": 1, "nota_acumulada": 18.5, "maximo_posible": 25.0 },
          { "corte_numero": 2, "nota_acumulada": 20.0, "maximo_posible": 25.0 }
        ]
      }
    ]
  }
  ```

---

### 3. Profesores
Gestiona los profesores asignados a las materias del estudiante.

| Método | Endpoint | Campos Body (POST/PUT) |
| :--- | :--- | :--- |
| `GET` | `/api/profesores/` | N/A |
| `POST` | `/api/profesores/` | `{"nombre": "Nombre del Prof"}` |
| `PUT/PATCH` | `/api/profesores/{id}/` | `{"nombre": "Nuevo Nombre"}` |
| `DELETE` | `/api/profesores/{id}/` | N/A |

---

### 4. Materias
Las materias son el núcleo del sistema.

- **POST /api/materias/**
  ```json
  {
    "nombre": "Algoritmos",
    "descripcion": "Opcional",
    "profesor": 1 // ID del profesor
  }
  ```
- **Respuesta (GET):** Incluye `profesor_nombre` para facilitar el renderizado sin peticiones extra.

---

### 5. Trimestres
Organiza las materias por periodos académicos.

- **Estructura del Body (POST):**
  ```json
  {
    "numero_trimestre": 1,
    "descripcion": "Primer Trimestre 2024",
    "materias": [1, 2, 3] // Lista de IDs de materias
  }
  ```

---

### 6. Sistema de Notas y Evaluación (Jerarquía)
La estructura sigue esta jerarquía: **Materia -> Cortes -> Notas -> Evaluaciones**.

#### Cortes (Fases de la materia)
- **POST /api/cortes/**: `{"numero": 1, "materia": 12}` (Normalmente 3 cortes por materia).

#### Notas (Cabecera de calificación)
- **POST /api/notas/**: `{"valor": 0, "descripcion": "Actividad", "corte": 5}` (El valor se autocalcula con las evaluaciones).

#### Evaluaciones (Detalle técnico)
- **POST /api/evaluaciones/**:
  ```json
  {
    "tipo": "Examen",
    "puntuacion": 15.5,
    "nota": 2, // ID de la Nota
    "archivo": null // Soporta carga de archivos
  }
  ```

---

### 7. Biblioteca (Apuntes)
Para el manejo de documentos y material de estudio.

- **POST /api/apuntes/** (Soporta `multipart/form-data` si hay archivo):
  ```json
  {
    "titulo": "Resumen Tema 1",
    "materia": 1,
    "descripcion": "Notas de clase",
    "archivo": (file)
  }
  ```

---

## 💡 Tips para el Frontend

1. **Jerarquía de Carga:** Al crear una Nota, primero debes tener el ID del Corte. Al crear un Corte, debes tener el ID de la Materia.
2. **Carga de Archivos:** Para los endpoints de `apuntes` y `evaluaciones`, asegúrate de usar un objeto `FormData` en Javascript si vas a enviar archivos.
3. **Paginación:** Los endpoints de lista pueden devolver datos paginados. Busca las claves `next`, `previous` y `results` en la respuesta.
4. **Estados IUTIRLA:** En el Dashboard, los estados se definen como:
   - `nf >= 50`: Aprobada
   - `nf >= 45`: Recuperatorio (Peligro)
   - `nf < 45`: Reprobada

---
*Documentación generada por Antigravity AI - Daniel David*
