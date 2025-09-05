# /src/ui/courses_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.queries import add_course, list_course, find_course_by_id, edit_course, delete_course
from src.validation import valid_credits, course_id_exists
from src.database import get_connection


def menu_courses():
    window = tk.Toplevel()
    window.title("📚 MINI SIGA - Menú Cursos")
    window.geometry("800x500")

    # --- Frame formulario ---
    frame_form = tk.LabelFrame(window, text="Registrar / Editar curso")
    frame_form.pack(fill="x", padx=10, pady=5)

    labels = ["Nombre:", "Docente:", "Créditos:"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame_form, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(frame_form, width=40)
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries[label] = entry

    # --- Frame búsqueda ---
    frame_search = tk.LabelFrame(window, text="🔎 Buscar curso por ID")
    frame_search.pack(fill="x", padx=10, pady=5)

    entry_search = tk.Entry(frame_search, width=20)
    entry_search.pack(side="left", padx=5, pady=5)

    # --- Tabla ---
    frame_table = tk.Frame(window)
    frame_table.pack(fill="both", expand=True, padx=10, pady=5)

    cols = ("ID", "Nombre", "Docente", "Créditos")
    tree = ttk.Treeview(frame_table, columns=cols, show="headings")

    widths = [50, 200, 200, 80]
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
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        conn.close()
        for r in rows:
            tree.insert("", "end", values=r)

    def clear_fields():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def on_add():
        name = entries["Nombre:"].get().strip()
        teacher = entries["Docente:"].get().strip()
        try:
            credits = int(entries["Créditos:"].get().strip())
        except ValueError:
            messagebox.showerror("Error", "❌ Los créditos deben ser un número entero.")
            return

        if not name or not teacher:
            messagebox.showerror("Error", "❌ Todos los campos son obligatorios.")
            return
        if not valid_credits(credits):
            messagebox.showerror("Error", "❌ Los créditos deben estar entre 1 y 10.")
            return

        add_course(name, teacher, credits)
        refresh_table()
        clear_fields()

    def on_update():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Debe seleccionar un curso de la tabla")
            return
        cid = tree.item(selected[0], "values")[0]

        name = entries["Nombre:"].get().strip()
        teacher = entries["Docente:"].get().strip()
        try:
            credits = int(entries["Créditos:"].get().strip())
        except ValueError:
            messagebox.showerror("Error", "❌ Los créditos deben ser un número entero.")
            return

        if not course_id_exists(cid):
            messagebox.showerror("Error", "❌ El ID del curso no existe.")
            return
        if not name or not teacher:
            messagebox.showerror("Error", "❌ Todos los campos son obligatorios.")
            return
        if not valid_credits(credits):
            messagebox.showerror("Error", "❌ Los créditos deben estar entre 1 y 10.")
            return

        edit_course(cid, name, teacher, credits)
        refresh_table()
        clear_fields()

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Debe seleccionar un curso para eliminar")
            return
        cid = tree.item(selected[0], "values")[0]
        delete_course(cid)
        refresh_table()
        clear_fields()

    def on_row_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            entries["Nombre:"].delete(0, tk.END)
            entries["Nombre:"].insert(0, values[1])
            entries["Docente:"].delete(0, tk.END)
            entries["Docente:"].insert(0, values[2])
            entries["Créditos:"].delete(0, tk.END)
            entries["Créditos:"].insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def on_search():
        cid = entry_search.get().strip()
        if not cid.isdigit():
            messagebox.showerror("Error", "Ingrese un ID válido")
            return
        rows = find_course_by_id(int(cid))
        for r in tree.get_children():
            tree.delete(r)
        if rows:
            for row in rows:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Resultado", f"No se encontró curso con ID {cid}")

    def go_back():
        window.destroy()

    # --- Botones ---
    frame_buttons = tk.Frame(window)
    frame_buttons.pack(fill="x", pady=5)

    tk.Button(frame_search, text="Buscar", command=on_search).pack(side="left", padx=5)
    tk.Button(frame_search, text="Mostrar todos", command=refresh_table).pack(side="left", padx=5)

    tk.Button(frame_buttons, text="➕ Agregar", command=on_add).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="✏️ Editar", command=on_update).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🗑 Eliminar", command=on_delete).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🔄 Refrescar", command=refresh_table).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🧹 Limpiar", command=clear_fields).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="⬅️ Volver", command=go_back).pack(side="right", padx=5)

    refresh_table()
    window.mainloop()
