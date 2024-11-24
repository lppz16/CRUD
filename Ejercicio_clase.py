import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Crear la base de datos
def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_database()

# Clase principal
class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD con Tkinter y SQLite")
        self.root.geometry("820x400")
        self.selected_id = None  # Inicializar ID seleccionado como None

        # Barra de menú
        self.create_menu()

        # Etiquetas y campos de entrada
        tk.Label(root, text="Nombre").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Correo").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Teléfono").grid(row=2, column=0, padx=10, pady=5)

        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botones del CRUD y salir
        tk.Button(root, text="Agregar", command=self.add_user).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(root, text="Actualizar", command=self.update_user).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(root, text="Eliminar", command=self.delete_user).grid(row=3, column=2, padx=10, pady=5)
        tk.Button(root, text="Salir", command=root.quit).grid(row=3, column=3, padx=10, pady=5)

        # Tabla para mostrar datos
        self.tree = ttk.Treeview(root, columns=("ID", "NOMBRE", "CORREO", "TELEFONO"), show="headings")
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("NOMBRE", text="NOMBRE")
        self.tree.heading("CORREO", text="CORREO")
        self.tree.heading("TELEFONO", text="TELEFONO")
        self.tree.bind("<Double-1>", self.on_item_selected)

        # Carga los datos al iniciar
        self.load_data()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menú de Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        # Menú de Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de:", command=self.show_about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)

    def show_about(self):
        messagebox.showinfo("Acerca de", "CRUD App con Tkinter y SQLite\nCreado por: Frank López")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def add_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if name and email and phone:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(name, email, phone) VALUES (?,?,?)", (name, email, phone))
            conn.commit()
            conn.close()
            self.clear_entries()
            self.load_data()
            messagebox.showinfo("Éxito", "Usuario ingresado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def on_item_selected(self, event):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, "values")
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[3])
        self.selected_id = values[0]

    def update_user(self):
        if self.selected_id is not None:
            name = self.name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            if name and email and phone:
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET name = ?, email = ?, phone = ? WHERE id = ?",
                               (name, email, phone, self.selected_id))
                conn.commit()
                conn.close()
                self.load_data()
                self.clear_entries()
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para actualizar")

    def delete_user(self):
        if self.selected_id is not None:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (self.selected_id,))
            conn.commit()
            conn.close()
            self.load_data()
            self.clear_entries()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.selected_id = None

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
