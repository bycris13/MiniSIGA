# 🎓 MiniSIGA - Sistema de Gestión Académica en Python

MiniSIGA es una aplicación de consola desarrollada en Python que permite gestionar estudiantes, cursos y matrículas en una institución educativa. Este proyecto forma parte del taller **"Estructura de Datos y Persistencia en Python (Avanzado)"** de la asignatura *Nuevas Tecnologías de Desarrollo*.

---

## 🧠 Objetivos del proyecto

- Modelar información usando clases y estructuras de datos.
- Implementar operaciones CRUD con persistencia en SQLite.
- Realizar consultas filtradas y búsquedas eficientes.
- Manejar errores y validar entradas del usuario.
- Diseñar un menú interactivo por consola.
- Preparar exportación a JSON y pruebas con `assert`.

---

## 📦 Estructura del proyecto
src/
├── database.py     # Conexión a SQLite y creación de tablas
├── main.py         # Punto de entrada del sistema y ejecución del menú
├── models.py       # Clases: Student, Course, Enrollment
├── queries.py      # Funciones CRUD para estudiantes
├── ui.py           # Menú interactivo por consola
---

## 🐍 Preparar entorno virtual

Antes de ejecutar el proyecto, crea y activa un entorno virtual:

```bash
python -m venv env

✅ Funcionalidades implementadas
Estudiantes
- 💾 Registrar estudiante
- 🧾 Listar estudiantes
- 🔍 Buscar estudiante por documento
- 🗑️ Eliminar estudiante por ID

🛠️ Tecnologías utilizadas
- Python 3
- SQLite (persistencia de datos)
- Estructura modular por carpetas
- Menú interactivo en consola

👨‍💻 Autor
bycris13

