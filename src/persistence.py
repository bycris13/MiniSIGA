import csv
import json
import os
from src.database import get_connection

# Archivos CSV
STUDENTS_FILE = "data/students.csv"
COURSES_FILE = "data/courses.csv"
ENROLLMENTS_FILE = "data/enrollments.csv"

# -------------------------------
# Guardar datos en CSV
# -------------------------------
def save_to_csv(filename, fieldnames, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# -------------------------------
# Sincronización desde SQLite → CSV
# -------------------------------
def sync_students_to_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, document, name, surname, email, birthdate FROM students")
    rows = cursor.fetchall()
    conn.close()

    fieldnames = ["student_id", "document", "name", "surname", "email", "birthdate"]
    data = [dict(zip(fieldnames, row)) for row in rows]
    save_to_csv(STUDENTS_FILE, fieldnames, data)


def sync_courses_to_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_id, name, teacher, credits FROM courses")
    rows = cursor.fetchall()
    conn.close()

    fieldnames = ["course_id", "name", "teacher", "credits"]
    data = [dict(zip(fieldnames, row)) for row in rows]
    save_to_csv(COURSES_FILE, fieldnames, data)


def sync_enrollments_to_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            e.enrollment_id,
            e.student_id,
            s.name || ' ' || s.surname AS student_name,
            e.course_id,
            c.name AS course_name,
            e.date_enrollment,
            e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
    """)
    rows = cursor.fetchall()
    conn.close()

    fieldnames = ["enrollment_id", "student_id", "student_name", "course_id", "course_name", "date_enrollment", "grade"]
    data = [dict(zip(fieldnames, row)) for row in rows]
    save_to_csv(ENROLLMENTS_FILE, fieldnames, data)


# -------------------------------
# Exportar todo a JSON
# -------------------------------
def export_all_to_json():
    files = {
        "students": STUDENTS_FILE,
        "courses": COURSES_FILE,
        "enrollments": ENROLLMENTS_FILE
    }

    for name, filename in files.items():
        if os.path.exists(filename):
            with open(filename, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data = list(reader)

            with open(f"{name}.json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
