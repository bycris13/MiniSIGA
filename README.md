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
├── ui/                 # Interfaces gráficas (Tkinter)
│   ├── courses_ui.py   # Menú gestion de cursos
│   └── enrollments.py  # Menú de gestión de matriculas y notas
│   └── students_ui.py  # Menú de gestión de estudiantes
│   └──  reports_ui.py      # Visualización de reportes y exportación a PDF
│   └── ui.py   # Menú principal
├── analytics.py    # Análisis de datos y generación de reportes
├── database.py     # Conexión a SQLite y creación de tablas
├── main.py         # Punto de entrada del sistema
├── models.py       # Clases: Student, Course, Enrollment
├── persistence.py  # Funciones de persistencia CSV y JSON
├── queries.py      # Operaciones CRUD y consultas a BD
├── report.py       # Generación de reportes en PDF con ReportLab
└── validation.py   # Validaciones
```
---

## 🐍 Preparar entorno virtual

Antes de ejecutar el proyecto, crea y activa un entorno virtual:

```bash
python -m venv env
```

## 📚 Librerías utilizadas

El proyecto utiliza tanto librerías estándar de **Python** como externas:

### 🔹 Estándar de Python
- **sqlite3** → Base de datos local.  
- **tkinter** → Interfaz gráfica.  
- **os, json, csv** → Persistencia y manejo de archivos.  

### 🔹 Externas (requieren instalación)
- **pandas** → Procesamiento y análisis de datos.  
- **matplotlib** → Gráficas interactivas.  
- **reportlab** → Exportación de reportes en PDF. 

Instálalas con:

```bash
pip install pandas matplotlib reportlab
```


## ▶️ Ejecución

Dentro del entorno virtual, ejecuta:

```bash
py -m src.main
```
