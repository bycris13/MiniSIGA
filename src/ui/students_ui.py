import tkinter as tk
from tkinter import ttk, messagebox
from src.queries import add_student, update_student, delete_stundent, find_student_by_document
from src.validation import valid_document, document_exists, valid_date, student_id_exists
from src.database import get_connection
from src.persistence import sync_students_to_csv, export_all_to_json


def menu_students():
    window = tk.Toplevel()
    window.title("📚 MINI SIGA - Menú Estudiantes")
    window.geometry("900x550")

    # --- Frame de formulario ---
    frame_form = tk.LabelFrame(window, text="Registrar / Editar estudiante")
    frame_form.pack(fill="x", padx=10, pady=5)

    labels = ["Documento:", "Nombre:", "Apellido:", "Correo:", "Nacimiento (YYYY-MM-DD):"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame_form, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(frame_form, width=40)
        entry.grid(row=i, column=1, padx=5, pady=2)
        entries[label] = entry

    # --- Frame de búsqueda ---
    frame_search = tk.LabelFrame(window, text="🔎 Buscar estudiante por documento")
    frame_search.pack(fill="x", padx=10, pady=5)

    entry_search = tk.Entry(frame_search, width=30)
    entry_search.pack(side="left", padx=5, pady=5)

    # --- Tabla ---
    frame_table = tk.Frame(window)
    frame_table.pack(fill="both", expand=True, padx=10, pady=5)

    cols = ("ID", "Documento", "Nombre", "Apellido", "Correo", "Nacimiento")
    tree = ttk.Treeview(frame_table, columns=cols, show="headings")

    # Ajustar ancho de columnas
    widths = [50, 120, 120, 120, 200, 120]
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
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        for r in rows:
            tree.insert("", "end", values=r)

    def clear_fields():
        """Limpia todos los campos del formulario"""
        for entry in entries.values():
            entry.delete(0, tk.END)

    def sync_and_refresh():
        """Sincroniza CSV y JSON tras cualquier operación"""
        sync_students_to_csv()
        export_all_to_json()
        refresh_table()
        clear_fields()

    def on_add():
        doc = entries["Documento:"].get().strip()
        name = entries["Nombre:"].get().strip()
        surname = entries["Apellido:"].get().strip()
        email = entries["Correo:"].get().strip()
        birthdate = entries["Nacimiento (YYYY-MM-DD):"].get().strip()

        # --- Validación de campos vacíos ---
        if not all([doc, name, surname, email, birthdate]):
            messagebox.showerror("Error", "❌ Todos los campos son obligatorios.")
            return

        # --- Validaciones específicas ---
        if not valid_document(doc):
            messagebox.showerror("Error", "❌ El documento debe tener 10 dígitos numéricos.")
            return
        if document_exists(doc):
            messagebox.showerror("Error", "❌ El documento ya existe en la base de datos.")
            return
        if not valid_date(birthdate):
            messagebox.showerror("Error", "❌ La fecha de nacimiento no es válida.")
            return

        add_student(doc, name, surname, email, birthdate)
        sync_and_refresh()

    def on_update():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Debe seleccionar un estudiante de la tabla para editar")
            return
        sid = tree.item(selected[0], "values")[0]
        doc = entries["Documento:"].get().strip()
        name = entries["Nombre:"].get().strip()
        surname = entries["Apellido:"].get().strip()
        email = entries["Correo:"].get().strip()
        birthdate = entries["Nacimiento (YYYY-MM-DD):"].get().strip()

        if not all([doc, name, surname, email, birthdate]):
            messagebox.showerror("Error", "❌ Todos los campos son obligatorios.")
            return

        if not student_id_exists(sid):
            messagebox.showerror("Error", "❌ El ID del estudiante no existe.")
            return
        if not valid_document(doc):
            messagebox.showerror("Error", "❌ El documento debe tener 10 dígitos numéricos.")
            return
        if not valid_date(birthdate):
            messagebox.showerror("Error", "❌ La fecha de nacimiento no es válida.")
            return

        update_student(sid, doc, name, surname, email, birthdate)
        sync_and_refresh()

    def on_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Debe seleccionar un estudiante de la tabla para eliminar")
            return
        sid = tree.item(selected[0], "values")[0]
        delete_stundent(sid)
        sync_and_refresh()

    def on_row_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            entries["Documento:"].delete(0, tk.END)
            entries["Documento:"].insert(0, values[1])
            entries["Nombre:"].delete(0, tk.END)
            entries["Nombre:"].insert(0, values[2])
            entries["Apellido:"].delete(0, tk.END)
            entries["Apellido:"].insert(0, values[3])
            entries["Correo:"].delete(0, tk.END)
            entries["Correo:"].insert(0, values[4])
            entries["Nacimiento (YYYY-MM-DD):"].delete(0, tk.END)
            entries["Nacimiento (YYYY-MM-DD):"].insert(0, values[5])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def on_search():
        doc = entry_search.get().strip()
        if not doc:
            messagebox.showerror("Error", "Ingrese un documento para buscar")
            return
        if not valid_document(doc):
            messagebox.showerror("Error", "❌ Documento inválido (deben ser 10 dígitos numéricos).")
            return

        rows = find_student_by_document(doc)

        for r in tree.get_children():
            tree.delete(r)

        if rows:
            for row in rows:
                tree.insert("", "end", values=row)
        else:
            messagebox.showinfo("Resultado", f"No se encontró estudiante con documento {doc}")

    tk.Button(frame_search, text="Buscar", command=on_search).pack(side="left", padx=5)
    tk.Button(frame_search, text="Mostrar todos", command=refresh_table).pack(side="left", padx=5)

    def go_back():
        window.destroy()

    # --- Botones ---
    frame_buttons = tk.Frame(window)
    frame_buttons.pack(fill="x", pady=5)

    tk.Button(frame_buttons, text="➕ Agregar", command=on_add).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="✏️ Editar", command=on_update).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🗑 Eliminar", command=on_delete).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🔄 Refrescar", command=refresh_table).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="🧹 Limpiar", command=clear_fields).pack(side="left", padx=5)
    tk.Button(frame_buttons, text="⬅️ Volver", command=go_back).pack(side="right", padx=5)

    refresh_table()
    window.mainloop()
