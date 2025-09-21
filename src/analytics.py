import pandas as pd
from src.database import get_connection

def analizar_notas():
    conn = get_connection()

    # Cargar las matrículas con estudiante y curso
    query = """
    SELECT 
        s.student_id,
        s.name || ' ' || s.surname AS estudiante,
        c.course_id,
        c.name AS curso,
        e.grade
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    WHERE e.grade IS NOT NULL
    """
    df = pd.read_sql(query, conn)
    conn.close()

    print("\n📊 Primeras filas:")
    print(df.head())

    # Promedio de todas las notas
    print("\n✅ Promedio general de notas:", df["grade"].mean())

    # Nota mínima y máxima
    print("\n🔽 Nota mínima:", df["grade"].min())
    print("🔼 Nota máxima:", df["grade"].max())

    # Promedio por curso
    print("\n📚 Promedio por curso:")
    print(df.groupby("curso")["grade"].mean())

    # Promedio por estudiante
    print("\n👨‍🎓 Promedio por estudiante:")
    print(df.groupby("estudiante")["grade"].mean())
