# /src/ui/enrollments_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.queries import add_enrollment, update_grade, delete_enrollment
from src.queries import student_id_exists, course_id_exists
from src.database import get_connection


def menu_enrollments():
    window = tk.Toplevel()
    window.title("📚 MINI SIGA - Menú Matrículas")
    window.geometry("1000x600")

    # --- Frame formulario ---
    frame_form = tk.LabelFrame(window, text="Registrar matrícula")
    frame_form.pack(fill="x", padx=10, pady=5)

    labels = ["ID Estudiante:", "ID Curso:"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame_form, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(frame_form, width=30)
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries[label] = entry

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
        for entry in entries.values():
            entry.delete(0, tk.END)

    def on_add():
        try:
            sid = int(entries["ID Estudiante:"].get().strip())
            cid = int(entries["ID Curso:"].get().strip())
        except ValueError:
            messagebox.showerror("Error", "❌ IDs deben ser números enteros.")
            return

        if not student_id_exists(sid):
            messagebox.showerror("Error", f"❌ No existe estudiante con ID {sid}")
            return
        if not course_id_exists(cid):
            messagebox.showerror("Error", f"❌ No existe curso con ID {cid}")
            return

        add_enrollment(sid, cid)
        refresh_table()
        clear_fields()

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
                refresh_table()
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
            messagebox.showinfo("Éxito", "✅ Matrícula eliminada correctamente")
        else:
            messagebox.showerror("Error", "❌ No se encontró matrícula con ese ID")
        refresh_table()

    def go_back():
        window.destroy()

    # --- Botones ---
    frame_buttons = tk.Frame(window)
    frame_buttons.pack(fill="x", pady=5)

    tk.Button(frame_buttons, text="➕ Matricular", command=on_add).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🧮 Registrar Nota", command=on_update_grade).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🗑 Eliminar", command=on_delete).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🔄 Refrescar", command=refresh_table).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🧹 Limpiar", command=clear_fields).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="⬅️ Volver", command=go_back).pack(side="right", padx=5)

    refresh_table()
    window.mainloop()
