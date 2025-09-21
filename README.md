# 🎓 MiniSIGA - Sistema de Gestión Académica en Python

MiniSIGA es una aplicación de consola desarrollada en Python que permite gestionar estudiantes, cursos y matrículas en una institución educativa. Este proyecto forma parte del taller **"Estructura de Datos y Persistencia en Python (Avanzado)"** de la asignatura *Nuevas Tecnologías de Desarrollo*.

---

## 🧠 Objetivos del proyecto

- Modelar información usando clases y estructuras de datos.
- Implementar operaciones CRUD con persistencia en SQLite.
- Realizar consultas filtradas y búsquedas eficientes.
- Manejar errores y validar entradas del usuario.
- Diseñar un menú interactivo grafico (Tikinter).
- Preparar exportación a JSON y pruebas con `assert`.

---

## 📦 Estructura del proyecto
```plaintext
data/               # Archivos de persistencia
├── courses.csv
├── enrollments.csv
├── students.csv
src/
├── database.py     # Conexión a SQLite y creación de tablas
├── ui/
│   ├── courses_ui.py  # Menú gestion de cursos
│   └── enrollments.py # Menú de gestión de matriculas y notas
│   └── students_ui.py # Menú de gestión de estudiantes
│   └── ui.py # Menú interactivo grafico (Tikinter).
├── analytics.py   # Análisis de datos y generación de reportes
├── database.py    # Conexión a SQLite y creación de tablas
├── main.py        # Punto de entrada del sistema
├── models.py      # Clases: Student, Course, Enrollment
├── persistence.py # Funciones de persistencia CSV y JSON
├── queries.py     # Operaciones CRUD y consultas a BD
└── validation.py  # Validaciones
```
---

## 🐍 Preparar entorno virtual

Antes de ejecutar el proyecto, crea y activa un entorno virtual:

```bash
python -m venv env
