import pandas as pd
from src.database import get_connection

def analyze_grades():
    """
    Analiza las notas almacenadas en la BD y devuelve estadísticas clave.
    """
    conn = get_connection()
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

    if df.empty:
        return None

    resultados = {
        "dataframe": df,
        "promedio_general": df["grade"].mean(),
        "min": df["grade"].min(),
        "max": df["grade"].max(),
        "promedio_curso": df.groupby("curso")["grade"].mean(),
        "promedio_estudiante": df.groupby("estudiante")["grade"].mean()
    }

    return resultados
