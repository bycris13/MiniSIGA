from src.database import get_connection
from src.validation import enrollment_exists, course_id_exists, student_id_exists
from datetime import datetime
# Colsultas de la tabla students
def add_student(document, name, surname, email, birthdate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (document, name, surname, email, birthdate)
            VALUES (?, ?, ?, ?, ?)
        """, (document, name, surname, email, birthdate))
        conn.commit()
        print("✅ Estudiante agregado correctamente.")
    except Exception as e:
        print(f"❌ Error al agregar estudiante: {e}")
    finally:
        conn.close()


def list_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()

    print("📋 Lista de estudiantes:")
    for row in rows:
        print(f"ID: {row[0]}, Documento: {row[1]}, Nombre: {row[2]} Apellido: {row[3]}, Email: {row[4]}, Fecha de Nacimiento: {row[5]}")

def find_student_by_document(document):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE document = ?", (document,))
        rows = cursor.fetchall()
        # Lista de la tabla students
        for row in rows:
            print(f" ✅ Estudiante Encontrado! \n Id: {row[0]} Documento: {row[1]} Nombre: {row[2]} Apellido {row[3]} Email: {row[4]} Fecha de Nacimiento: {row[5]}")    
        if not rows:
            print(f"No existe estudiante con ese documento: {document}")
    except Exception as err:
        print(f"❌ Ocurrio un error al bucar el estudiante por el documento: {err}")
    finally:
        conn.close()

def update_student(student_id,document, name, surname, email, birthdate):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET document = ?, name = ?, surname = ?, email = ?,birthdate = ?  WHERE student_id = ? ", (document, name, surname, email, birthdate, student_id))
        conn.commit()
        print("✅ Estudiante actualizado correctamente.")
    except Exception as err:
          print(f"❌ Error al actualizar estudiante: {err}")
    finally:
        conn.close()

def delete_stundent(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM students WHERE student_id = ? """, (student_id,) )
        conn.commit()
        if cursor.rowcount == 0:  # no eliminó ninguna fila
            print("❌ No se encontró estudiante con ese ID.")
        else:
            print("✅ Estudiante eliminado correctamente")
    except Exception as err:
        print(f"❌ Errror al eliminar estudiante: {err}")
    finally:
        conn.close()

# Colsultas de la tabla courses
def add_course(name, teacher, credits):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (name, teacher, credits) VALUES (?, ?, ?)", (name, teacher, credits))
        conn.commit()
        print("✅ Curso agregado exitosamente.")
    except Exception as err:
        print(f"❌ Error al guardar el curso {err}")
    finally:
        conn.close()

def list_course():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    cursor.close()
    print("📋 Lista de cursos:")
    for row in rows:
        print(f"ID: {row[0]}, Nombre del curso: {row[1]}, Docente: {row[2]}, Creditos: {row[3]}")

def find_course_by_id(course_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses WHERE course_id = ?",(course_id,))
    rows = cursor.fetchall()
    cursor.close()
    if not rows: # Aquí validamos si está vacío
        print("❌ No se encontró curso con ese ID.")
    else:
        print('✅ Curso encontrado.')
    for row in rows:
        print(f"ID: {row[0]}, Nombre del curso: {row[1]}, Docente: {row[2]} Creditos {row[3]}")
    
def edit_course(course_id, name, teacher, credits):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE courses SET name = ?, teacher = ?, credits = ? WHERE course_id = ?", (name, teacher, credits, course_id))
        conn.commit()
        print("✅ Curso actualizado corectamente")
    except Exception as err:
        print(f"❌ No se pudo actualizar correctamente. {err}")
    finally:
        conn.close()

def delete_course(course_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE course_id = ? ", (course_id,))
        conn.commit()
        if cursor.rowcount == 0:
            print("❌ No se encontro el curso con ese ID")
        else:
            print("✅ Curso eliminado exitosamente")
    except Exception as err:
        print(f"❌ Error al eliminar el curso: {err}")
    finally:
        conn.close()

def add_enrollment(student_id, course_id):
    date_enrollment = datetime.today().strftime("%Y-%m-%d")
    if enrollment_exists(student_id, course_id):
        print("❌ Ya existe esta matricula")
        return
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO enrollments (student_id, course_id,  date_enrollment) VALUES (?, ?, ?)", (student_id, course_id,  date_enrollment))
        conn.commit()
        print("✅ Maricula registrada corectamente")
    except Exception as err:
        print(f"Error al registar matricula: {err}")
    finally:
        conn.close()

def list_enrollments():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        e.enrollment_id,
        s.name || ' ' || s.surname AS estudiante,
        s.email AS correo,
        c.name AS curso,
        e.date_enrollment,
        e.grade
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    """)
    rows = cursor.fetchall()
    conn.close() 
    print("📋 Lista de matrículas:")
    for row in rows:
        print(f"ID: {row[0]} | 👤 Estudiante: {row[1]} | ✉️   Correo: {row[2]} | 📚 Curso: {row[3]} | 📆 Fecha: {row[4]} | Nota: 🧮 {row[5]} ")

def find_enrollments():
    conn = get_connection()
    cursor = conn.cursor()

    print("🔎 Buscar matrícula:")
    criterio = input("¿Desea buscar por estudiante (E) o curso (C)? ").strip().upper()

    if criterio == "E":
        name = input("Ingrese el nombre o apellido del estudiante: ")
        cursor.execute("""
        SELECT 
            e.enrollment_id,
            s.name || ' ' || s.surname AS estudiante,
            s.email AS correo,
            c.name AS curso,
            e.date_enrollment
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE s.name LIKE ? OR s.surname LIKE ?
        """, (f"%{name}%", f"%{name}%"))

    elif criterio == "C":
        course = input("Ingrese el nombre del curso: ")
        cursor.execute("""
        SELECT 
            e.enrollment_id,
            s.name || ' ' || s.surname AS estudiante,
            s.email AS correo,
            c.name AS curso,
            e.date_enrollment
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        WHERE c.name LIKE ?
        """, (f"%{course}%",))

    else:
        print("❌ Opción no válida.")
        conn.close()
        return

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("⚠️ No se encontraron matrículas.")
        return

    print("📋 Resultados de la búsqueda:")
    for row in rows:
        print(f"ID: {row[0]} | 👤 Estudiante: {row[1]} | ✉️ {row[2]} | 📚 Curso: {row[3]} | | 📆 Fecha: {row[4]}")

def update_grade(enrollment_id, grade):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE enrollments 
            SET grade = ? 
            WHERE enrollment_id = ?
        """, (grade, enrollment_id))
        conn.commit()

        if cursor.rowcount == 0:
            print("❌ No se encontró matrícula con ese ID.")
        else:
            print("✅ Nota registrada correctamente.")
    except Exception as err:
        print(f"❌ Error al registrar nota: {err}")
    finally:
        conn.close()
