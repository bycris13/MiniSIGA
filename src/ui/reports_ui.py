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
     # --- Estadísticas en formato tabla ---
    frame_stats = tk.Frame(ventana, bd=1, relief="solid")
    frame_stats.pack(pady=15)

    # Encabezado
    tk.Label(
        frame_stats, text="📌 Estadística", bg="#4F81BD", fg="white",
        font=("Arial", 12, "bold"), width=20, padx=5, pady=5
    ).grid(row=0, column=0, sticky="nsew")

    tk.Label(
        frame_stats, text="Valor", bg="#4F81BD", fg="white",
        font=("Arial", 12, "bold"), width=20, padx=5, pady=5
    ).grid(row=0, column=1, sticky="nsew")

    # Filas con datos
    stats_data = [
        ("Promedio general", f"{resultados['promedio_general']:.2f}"),
        ("Nota mínima", f"{resultados['min']}"),
        ("Nota máxima", f"{resultados['max']}"),
    ]

    for i, (label, value) in enumerate(stats_data, start=1):
        bg_color = "#DCE6F1"  # gris claro
        tk.Label(
            frame_stats, text=label, bg=bg_color,
            font=("Arial", 11), width=20, padx=5, pady=5
        ).grid(row=i, column=0, sticky="nsew")

        tk.Label(
            frame_stats, text=value, bg=bg_color,
            font=("Arial", 11), width=20, padx=5, pady=5
        ).grid(row=i, column=1, sticky="nsew")


    # --- Frame para gráficos ---
    frame_graficos = tk.Frame(ventana)
    frame_graficos.pack(fill=tk.BOTH, expand=True)

    # --- Gráfico: Promedio por curso ---
    fig1, ax1 = plt.subplots(figsize=(5,4))  # un poco más ancho
    resultados["promedio_curso"].plot(kind="bar", color="skyblue", edgecolor="black", ax=ax1)
    ax1.set_title("Promedio de Notas por Curso")
    ax1.set_ylabel("Promedio")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right")  # rotar nombres
    plt.tight_layout()  # ajusta para que no se corte
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_graficos)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Guardar temporalmente este gráfico
    ruta_curso = os.path.join(tempfile.gettempdir(), "grafico_curso.png")
    fig1.savefig(ruta_curso, bbox_inches="tight")

    # --- Gráfico: Promedio por estudiante ---
    fig2, ax2 = plt.subplots(figsize=(5,4))  # un poco más ancho
    resultados["promedio_estudiante"].plot(kind="bar", color="lightgreen", edgecolor="black", ax=ax2)
    ax2.set_title("Promedio de Notas por Estudiante")
    ax2.set_ylabel("Promedio")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right")  # rotar nombres
    plt.tight_layout()  # 🔑 ajusta para que no se corte
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_graficos)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Guardar temporalmente este gráfico
    ruta_estudiante = os.path.join(tempfile.gettempdir(), "grafico_estudiante.png")
    fig2.savefig(ruta_estudiante, bbox_inches="tight")

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

