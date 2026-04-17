# Guía de Construcción para el Frontend (App Móvil)

---

## 1. Arquitectura de Pantallas (Flujo de Usuario)

Para mantenerlo como un verdadero MVP (Minimum Viable Product), te sugiero limitarte estrictamente a estas pantallas principales con una navegación por pestañas inferiores (Bottom Tab Navigation):

### 1.1 - Pantallas de Autenticación (Auth Stack)

- **Login / Register Screen:** Una pantalla minimalista donde puedan iniciar sesión. Al darle a Entrar, tu App mandará el HTTP POST a `/api/auth/login/` devolviendo el JWT. Guardarás ese `access_token` en el SecureStorage del teléfono.

### 1.2 - Pantalla Principal: "Mi Rendimiento" (Home Tab)

Aquí es donde usarás el endpoint maestro que creaste (`/api/estadisticas/`).

- **Header "Hero":** Un circulo o barra circular de progreso gigante mostrando el `"promedio_global"`.
- **Tarjetas de Estado:** 3 cuadritos lado a lado mostrando: "Aprobadas", "Reprobadas" y "En Peligro".
- **Widget de Mejor Materia:** Una tarjetita felicitando al estudiante mostrando "Mejor materia actual: X".
- **Feed Inferior:** Una lista scrolleable que muestre las materias actuales y su nota final actual.

### 1.3 - Pantalla: "Gestor Curricular" (Materias Tab)

Aquí harás las consultas a `GET /api/materias/`.

- Un listado limpio tipo acordeón. Al desplegar una `Materia`, mostrará sus `Cortes` y al presionar un corte desplegará las `Notas`.
- **Botón Flotante (FAB):** Un botón redondo con el símbolo "+" en la esquina inferior derecha para abrir el Modal que servirá para "Agregar Materia", "Añadir Profesor", etc.

### 1.4 - Pantalla de Archivos (Biblioteca Tab)

Basado en tu modelo actual, como unificaste el archivo directamente dentro de `Evaluacion` a través del serializador, harás llamadas listando todas las evaluaciones con sus docs.

- Mostrará tarjetas con el título y el ícono del archivo descargable (PDF, Foto).

### 1.5 - Pantalla de Configuración y Pagos (Perfil Tab)

- Mostrará el correo del estudiante y los días restantes que le quedan de su prueba de 14 días.
- Tendrá el botón call-to-action resaltado: **"Pagar mi membresía ($25)"**.

---

## 2. Pila Tecnológica Recomendada para el Frontend

- **UI Framework:** Expo + React Native o Flutter (Permiten crear app para iOS y Android con el mismo código de una sola vez).
- **Gestor de estado:** `Zustand` (en React) para guardar el estado del Usuario global o `Provider` en Flutter.
- **Axios / HTTP:** Para enviar en cada petición a tu backend de Django tu Header de autorización:
  ```json
  { "Authorization": "Bearer <tu_token_aqui>" }
  ```

---

## 3. Consejos de Experiencia de Usuario (UX)

Ya que va dirigido a los estudiantes del UITIRLA de materias como Marketing y Diseño gráfico, **la App tiene que verse moderna y premium sino se aburrirán rápido**.

- **Esquema de Colores:** Usa "Dark Mode" por defecto (Fondos en negros o gris muy oscuro `#121212`) acompañado de colores Neón o pasteles (Lila o Verde Esmeralda) para botones. Los elementos de cristal (Glassmorphism) agradan mucho visualmente.
- **Micro-interacciones:** Añade vibraciones hápticas en el celular cuando el estudiante registre una materia nueva o vea que salvó el trimestre.
- **Cero Tablas Aburridas:** No diseñes las notas como si fuera un cuadro de Excel, diseña las notas como tarjetas independientes, con barras de progreso redondeadas.

---
