import sqlite3

# Función para conectarse a la base de datos
def get_connection():
    return sqlite3.connect("universidad.db")

# Función para crear las tablas
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students ( 
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        document TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        birthdate TEXT
    );
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher TEXT NOT NULL,
        credits INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments( 
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        grade REAL,
        date_enrollment TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    );
    """)

    conn.commit()  # Guardar cambios
    conn.close()   # Cerrar conexión

if __name__ == "__main__":
    create_tables()
    print("✅ Base de datos y tablas creadas correctamente.")
