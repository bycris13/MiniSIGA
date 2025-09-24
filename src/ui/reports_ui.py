import tkinter as tk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tempfile
from src.analytics import analyze_grades
from src.report import report_generator_pdf
import os

def menu_reports():
    resultados = analyze_grades()
    if resultados is None:
        messagebox.showwarning("Aviso", "⚠️ No hay notas registradas.")
        return

    # Crear ventana
    ventana = tk.Toplevel()
    ventana.title("📊 Reportes de Notas")
    ventana.geometry("950x650")

    # --- Estadísticas ---
    lbl_stats = tk.Label(
        ventana,
        text=f"""
        📊 Estadísticas Generales:
        Promedio General: {resultados['promedio_general']:.2f}
        Nota Mínima: {resultados['min']}
        Nota Máxima: {resultados['max']}
        """,
        justify="left",
        font=("Arial", 12)
    )
    lbl_stats.pack(pady=10)

    # --- Frame para gráficos ---
    frame_graficos = tk.Frame(ventana)
    frame_graficos.pack(fill=tk.BOTH, expand=True)

    # --- Gráfico: Promedio por curso ---
    fig1, ax1 = plt.subplots(figsize=(4,3))
    resultados["promedio_curso"].plot(kind="bar", color="skyblue", edgecolor="black", ax=ax1)
    ax1.set_title("Promedio de Notas por Curso")
    ax1.set_ylabel("Promedio")
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_graficos)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Guardar temporalmente este gráfico
    ruta_curso = os.path.join(tempfile.gettempdir(), "grafico_curso.png")
    fig1.savefig(ruta_curso)

    # --- Gráfico: Promedio por estudiante ---
    fig2, ax2 = plt.subplots(figsize=(4,3))
    resultados["promedio_estudiante"].plot(kind="bar", color="lightgreen", edgecolor="black", ax=ax2)
    ax2.set_title("Promedio de Notas por Estudiante")
    ax2.set_ylabel("Promedio")
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_graficos)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Guardar temporalmente este gráfico
    ruta_estudiante = os.path.join(tempfile.gettempdir(), "grafico_estudiante.png")
    fig2.savefig(ruta_estudiante)

    # Agregar las rutas de los gráficos al diccionario resultados
    resultados["grafico_curso"] = ruta_curso
    resultados["grafico_estudiante"] = ruta_estudiante

    # --- Botón para exportar a PDF ---
    def exportar_pdf():
        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte como..."
        )
        if ruta:
            report_generator_pdf(resultados, output_file=ruta)  # Guardar en la ruta elegida
            messagebox.showinfo("Éxito", f"✅ Reporte guardado en:\n{ruta}")

    btn_pdf = tk.Button(
        ventana,
        text="📄 Generar Reporte en PDF",
        command=exportar_pdf,
        bg="lightblue",
        font=("Arial", 12, "bold")
    )
    btn_pdf.pack(pady=15)

