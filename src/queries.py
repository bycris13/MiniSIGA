from src.database import get_connection

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
        print(f"ID: {row[0]}, Documento: {row[1]}, Nombre: {row[2]} Apellido {row[3]}, Email: {row[4]}, Fecha de Nacimiento: {row[5]}")

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

def delete_stundent(student_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(""" DELETE FROM students WHERE student_id = ? """, (student_id,) )
        conn.commit()
        print("✅ Estudiante eliminado correctamente")
    except Exception as err:
        print(f"❌ Errror al eliminar estudiante: {err}")
    finally:
        conn.close()
