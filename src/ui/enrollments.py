import tkinter as tk
from tkinter import ttk, messagebox
from src.queries import add_enrollment, update_grade, delete_enrollment
from src.database import get_connection
from src.persistence import (
    sync_students_to_csv,
    sync_courses_to_csv,
    sync_enrollments_to_csv,
    export_all_to_json
)

def menu_enrollments():
    window = tk.Toplevel()
    window.title("📚 MINI SIGA - Menú Matrículas")
    window.geometry("1000x600")

    # --- Frame formulario ---
    frame_form = tk.LabelFrame(window, text="Registrar matrícula")
    frame_form.pack(fill="x", padx=10, pady=5)

    # --- Combobox Estudiantes ---
    tk.Label(frame_form, text="Estudiante:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    student_combo = ttk.Combobox(frame_form, width=40, state="readonly")
    student_combo.grid(row=0, column=1, padx=5, pady=2)

    # --- Combobox Cursos ---
    tk.Label(frame_form, text="Curso:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    course_combo = ttk.Combobox(frame_form, width=40, state="readonly")
    course_combo.grid(row=1, column=1, padx=5, pady=2)

    # --- Cargar datos para los combos ---
    def load_students_courses():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT student_id, name, surname, email FROM students")
        students = cursor.fetchall()
        student_combo["values"] = [f"{s[1]} {s[2]} ({s[3]})" for s in students]

        cursor.execute("SELECT course_id, name, teacher FROM courses")
        courses = cursor.fetchall()
        course_combo["values"] = [f"{c[1]} - {c[2]}" for c in courses]

        conn.close()
        return students, courses

    students, courses = load_students_courses()

    # --- Frame búsqueda ---
    frame_search = tk.LabelFrame(window, text="🔍 Buscar Matrícula")
    frame_search.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_search, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5)
    search_type = ttk.Combobox(frame_search, values=["Estudiante", "Curso"], state="readonly")
    search_type.current(0)
    search_type.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_search, text="Criterio:").grid(row=0, column=2, padx=5, pady=5)
    entry_search = tk.Entry(frame_search, width=30)
    entry_search.grid(row=0, column=3, padx=5, pady=5)

    def on_search():
        criterio = search_type.get()
        term = entry_search.get().strip()

        if not term:
            messagebox.showerror("Error", "Debe ingresar un criterio de búsqueda")
            return

        for row in tree.get_children():
            tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        if criterio == "Estudiante":
            cursor.execute("""
                SELECT 
                    e.enrollment_id,
                    s.name || ' ' || s.surname AS estudiante,
                    s.email AS correo,
                    c.name AS curso,
                    e.date_enrollment,
                    e.grade
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                WHERE s.name LIKE ? OR s.surname LIKE ?
            """, (f"%{term}%", f"%{term}%"))
        else:  # Curso
            cursor.execute("""
                SELECT 
                    e.enrollment_id,
                    s.name || ' ' || s.surname AS estudiante,
                    s.email AS correo,
                    c.name AS curso,
                    e.date_enrollment,
                    e.grade
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                WHERE c.name LIKE ?
            """, (f"%{term}%",))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Sin resultados", "⚠️ No se encontraron matrículas.")
            return

        for r in rows:
            tree.insert("", "end", values=r)

    tk.Button(frame_search, text="Buscar", command=on_search).grid(row=0, column=4, padx=5, pady=5)

    # --- Frame tabla ---
    frame_table = tk.Frame(window)
    frame_table.pack(fill="both", expand=True, padx=10, pady=5)

    cols = ("ID", "Estudiante", "Correo", "Curso", "Fecha", "Nota")
    tree = ttk.Treeview(frame_table, columns=cols, show="headings")

    widths = [50, 200, 200, 200, 120, 80]
    for col, w in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w)

    tree.pack(fill="both", expand=True)

    # --- Funciones internas ---
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT 
            e.enrollment_id,
            s.name || ' ' || s.surname AS estudiante,
            s.email AS correo,
            c.name AS curso,
            e.date_enrollment,
            e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses c ON e.course_id = c.course_id
        """)
        rows = cursor.fetchall()
        conn.close()
        for r in rows:
            tree.insert("", "end", values=r)

    def clear_fields():
        student_combo.set("")
        course_combo.set("")

    def sync_and_refresh():
        """Sincroniza SQLite → CSV/JSON y refresca la tabla"""
        sync_students_to_csv()
        sync_courses_to_csv()
        sync_enrollments_to_csv()
        export_all_to_json()
        refresh_table()
        clear_fields()

    def on_add():
        student_index = student_combo.current()
        course_index = course_combo.current()

        if student_index == -1 or course_index == -1:
            messagebox.showerror("Error", "❌ Debe seleccionar un estudiante y un curso.")
            return

        sid = students[student_index][0]  # student_id real
        cid = courses[course_index][0]    # course_id real

        add_enrollment(sid, cid)
        sync_and_refresh()
        messagebox.showinfo("Éxito", "✅ Matrícula registrada")

    def on_update_grade():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione una matrícula de la tabla")
            return
        eid = tree.item(selected[0], "values")[0]

        grade_win = tk.Toplevel(window)
        grade_win.title("Registrar nota")

        tk.Label(grade_win, text="Nota (0.0 - 5.0):").pack(padx=10, pady=5)
        entry_grade = tk.Entry(grade_win, width=10)
        entry_grade.pack(padx=10, pady=5)

        def save_grade():
            try:
                grade = float(entry_grade.get().strip())
                if grade < 0 or grade > 5:
                    raise ValueError
                update_grade(eid, grade)
                sync_and_refresh()
                grade_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "❌ La nota debe estar entre 0.0 y 5.0")

        tk.Button(grade_win, text="Guardar", command=save_grade).pack(pady=5)

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione una matrícula de la tabla")
            return
        eid = int(tree.item(selected[0], "values")[0])
        if delete_enrollment(eid):
            sync_and_refresh()
            messagebox.showinfo("Éxito", "✅ Matrícula eliminada correctamente")
        else:
            messagebox.showerror("Error", "❌ No se encontró matrícula con ese ID")

    def go_back():
        window.destroy()

    # --- Botones ---
    frame_buttons = tk.Frame(window)
    frame_buttons.pack(fill="x", pady=5)

    tk.Button(frame_buttons, text="➕ Matricular", command=on_add).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🧮 Registrar Nota", command=on_update_grade).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🗑 Eliminar", command=on_delete).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🔄 Refrescar", command=sync_and_refresh).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🧹 Limpiar", command=clear_fields).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="⬅️ Volver", command=go_back).pack(side="right", padx=5)

    sync_and_refresh()
    window.mainloop()
