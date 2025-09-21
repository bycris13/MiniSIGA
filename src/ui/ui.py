# src/ui/ui.py
import tkinter as tk
from tkinter import messagebox

from src.ui.students_ui import menu_students
from src.ui.courses_ui import menu_courses
from src.ui.enrollments import menu_enrollments

def menu():
    root = tk.Tk()
    root.title("📚 MINI SIGA")
    root.geometry("400x300")

    # Título
    label = tk.Label(root, text="📚 MINI SIGA - Menú Principal", font=("Arial", 14, "bold"))
    label.pack(pady=20)

    # Botones
    btn_students = tk.Button(root, text="💾 Estudiantes", width=25, command=menu_students)
    btn_students.pack(pady=5)

    btn_courses = tk.Button(root, text="📚 Gestión de cursos", width=25, command=menu_courses)
    btn_courses.pack(pady=5)

    btn_enrollments = tk.Button(root, text="📝 Matrículas", width=25, command=menu_enrollments)
    btn_enrollments.pack(pady=5)

    btn_exit = tk.Button(root, text="❌ Salir", width=25, command=root.quit)
    btn_exit.pack(pady=20)

    root.mainloop()
