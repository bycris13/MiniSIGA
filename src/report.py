from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def report_generator_pdf(resultados, output_file="reporte_notas.pdf"):
    styles = getSampleStyleSheet()
    story = []

    # Título
    story.append(Paragraph("📊 Reporte de Notas", styles["Title"]))
    story.append(Spacer(1, 20))

    # Estadísticas
    texto = f"""
    <b>Promedio general:</b> {resultados['promedio_general']:.2f}<br/>
    <b>Nota mínima:</b> {resultados['min']}<br/>
    <b>Nota máxima:</b> {resultados['max']}<br/>
    """
    story.append(Paragraph(texto, styles["Normal"]))
    story.append(Spacer(1, 20))

    # Gráficas
    story.append(Paragraph("<b>Promedio por curso</b>", styles["Heading2"]))
    story.append(Image(resultados["grafico_curso"], width=400, height=250))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Promedio por estudiante</b>", styles["Heading2"]))
    story.append(Image(resultados["grafico_estudiante"], width=400, height=250))

    # Guardar PDF en la ruta elegida
    doc = SimpleDocTemplate(output_file)
    doc.build(story)
    print(f"✅ Reporte generado en {output_file}")
