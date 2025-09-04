import csv
import json
import os

# Rutas de archivos
BASE_PATH = "data"
STUDENTS_FILE = os.path.join(BASE_PATH, "students.csv")
COURSES_FILE = os.path.join(BASE_PATH, "courses.csv")
ENROLLMENTS_FILE = os.path.join(BASE_PATH, "enrollments.csv")

# ---------------------------
# Guardar en CSV
# ---------------------------
def save_to_csv(filename, data, headers):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

# ---------------------------
# Cargar desde CSV
# ---------------------------
def load_from_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

# ---------------------------
# Exportar a JSON
# ---------------------------
def export_to_json(data, filename="export.json"):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"✅ Datos exportados correctamente a {filename}")
