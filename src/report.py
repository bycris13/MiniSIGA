from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def report_generator_pdf(resultados, output_file="reporte_notas.pdf"):
    styles = getSampleStyleSheet()
    story = []

    # --- Título ---
    story.append(Paragraph("📊 Reporte de Notas", styles["Title"]))
    story.append(Spacer(1, 20))

    # --- Introducción ---
    story.append(Paragraph(
        "Este reporte contiene un análisis general de las calificaciones registradas en el sistema. "
        "Incluye un resumen estadístico con los valores más relevantes, así como gráficas comparativas "
        "que permiten visualizar los promedios de notas por curso y por estudiante.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    # --- Texto antes de la tabla ---
    story.append(Paragraph(
        "📌 <b>Tabla 1. Estadísticas Generales</b><br/>"
        "En esta tabla se muestran tres métricas principales: "
        "el promedio general de todas las notas, la nota más baja registrada y la nota más alta registrada. "
        "Estos datos permiten tener una visión clara del desepeño de los estudiantes.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    # --- Tabla con estadísticas generales ---
    data = [
        ["Estadística", "Valor"],
        ["Promedio general", f"{resultados['promedio_general']:.2f}"],
        ["Nota mínima", f"{resultados['min']}"],
        ["Nota máxima", f"{resultados['max']}"],
    ]

    tabla = Table(data, colWidths=[200, 150])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),  # Encabezado azul
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#DCE6F1")),  # Fondo claro
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(tabla)
    story.append(Spacer(1, 30))

    # --- Texto antes del gráfico por curso ---
    story.append(Paragraph(
        "📊 <b>Gráfico 1. Promedio de Notas por Curso</b><br/>"
        "En este gráfico se observa el promedio de calificaciones de cada curso. "
        "Esto permite identificar los cursos con mejor rendimiento academico"
        "y en cuáles podría ser necesario reforzar los contenidos o estrategias de enseñanza.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    # --- Gráfico: Promedio por curso ---
    story.append(Image(resultados["grafico_curso"], width=400, height=250))
    story.append(Spacer(1, 30))

    # --- Texto antes del gráfico por estudiante ---
    story.append(Paragraph(
        "📊 <b>Gráfico 2. Promedio de Notas por Estudiante</b><br/>"
        "Este gráfico muestra el promedio individual de cada estudiante. "
        "Es útil para detectar tanto a los estudiantes con mejor desempeño "
        "como aquellos que podrían requerir apoyo adicional.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    # --- Gráfico: Promedio por estudiante ---
    story.append(Image(resultados["grafico_estudiante"], width=400, height=250))

    # --- Conclusión ---
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "En conclusión, este reporte ofrece una visión global del rendimiento académico, "
        "facilitando la identificación de fortalezas y áreas de mejora tanto a nivel de cursos "
        "como de estudiantes.",
        styles["Normal"]
    ))

    # --- Guardar PDF ---
    doc = SimpleDocTemplate(output_file)
    doc.build(story)
    print(f"✅ Reporte generado en {output_file}")
