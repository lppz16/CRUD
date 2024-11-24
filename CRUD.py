import tkinter as tk
from tkinter import ttk, messagebox, Menu
import sqlite3
import random

# Crear la base de datos
def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_database()

# Clase principal
class CRUDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD con Generador de Contraseñas")
        self.root.geometry("1020x450")

        # Paleta de colores
        bg_color = "#2b2b2b"  # Fondo principal
        header_color = "#1e90ff"  # Encabezados de la tabla (azul profundo)
        button_color = "#20b2aa"  # Botones (verde azulado)
        text_color = "#f8f8f2"  # Texto (gris claro)
        entry_bg_color = "#404040"  # Fondo de las entradas (gris oscuro)

        # Configuración general
        self.root.configure(bg=bg_color)
        self.selected_id = None

        # Menú superior
        menu = Menu(root, bg=bg_color, fg=text_color, activebackground=header_color, activeforeground=text_color)
        root.config(menu=menu)
        archivo_menu = Menu(menu, tearoff=0, bg=bg_color, fg=text_color)
        ayuda_menu = Menu(menu, tearoff=0, bg=bg_color, fg=text_color)
        menu.add_cascade(label="Archivo", menu=archivo_menu)
        menu.add_cascade(label="Ayuda", menu=ayuda_menu)
        archivo_menu.add_command(label="Salir", command=root.quit)
        ayuda_menu.add_command(label="Acerca de", command=self.show_help)

        # Etiquetas y campos de entrada
        tk.Label(root, text="Nombre", bg=bg_color, fg=text_color).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Correo", bg=bg_color, fg=text_color).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Teléfono", bg=bg_color, fg=text_color).grid(row=2, column=0, padx=10, pady=5)
        tk.Label(root, text="Contraseña", bg=bg_color, fg=text_color).grid(row=3, column=0, padx=10, pady=5)

        self.name_entry = tk.Entry(root, bg=entry_bg_color, fg=text_color, insertbackground=text_color)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.email_entry = tk.Entry(root, bg=entry_bg_color, fg=text_color, insertbackground=text_color)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.phone_entry = tk.Entry(root, bg=entry_bg_color, fg=text_color, insertbackground=text_color)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)
        self.password_entry = tk.Entry(root, bg=entry_bg_color, fg=text_color, insertbackground=text_color)
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Botones
        tk.Button(root, text="Generar Contraseña y Correo", bg=button_color, fg=text_color, command=self.generate_credentials).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(root, text="Agregar", bg=button_color, fg=text_color, command=self.add_user).grid(row=4, column=1, padx=10, pady=5)
        tk.Button(root, text="Actualizar", bg=button_color, fg=text_color, command=self.update_users).grid(row=4, column=2, padx=10, pady=5)
        tk.Button(root, text="Eliminar", bg=button_color, fg=text_color, command=self.delete_user).grid(row=4, column=3, padx=10, pady=5)

        # Tabla
        self.tree = ttk.Treeview(root, columns=("ID", "NOMBRE", "CORREO", "TELEFONO", "CONTRASEÑA"), show="headings")
        self.tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("NOMBRE", text="NOMBRE")
        self.tree.heading("CORREO", text="CORREO")
        self.tree.heading("TELEFONO", text="TELEFONO")
        self.tree.heading("CONTRASEÑA", text="CONTRASEÑA")
        self.tree.bind("<Double-1>", self.on_item_selected)

        self.style = ttk.Style()
        self.style.configure("Treeview", background=entry_bg_color, foreground=text_color, fieldbackground=entry_bg_color)
        self.style.configure("Treeview.Heading", background=header_color, foreground=text_color)

        self.load_data()

    def show_help(self):
        messagebox.showinfo("Acerca de", "CRUD con Generador de Contraseñas\nVersión 1.0\nDesarrollado por Yan Frank Ríos López")

    def generate_credentials(self):
        chars = '!"#$%&()*+,-./0123456789?@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        chars2 = '!"#$%&()*+,-./0123456789?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        password_length = 8
        email_length = 6
        dominio = ["gmail.com", "yahoo.com", "outlook.com", "custommail.com"]

        password = ''.join(random.choice(chars) for _ in range(password_length))
        email = ''.join(random.choice(chars2) for _ in range(email_length)) + "@" + random.choice(dominio)

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)

    def add_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        if name and email and phone and password:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
                           (name, email, phone, password))
            conn.commit()
            conn.close()
            self.clear_entries()
            self.load_data()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, values[3])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, values[4])
            self.selected_id = values[0]

    def update_users(self):
        # Primero eliminamos todos los usuarios
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()

        # Luego agregamos el nuevo usuario
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()

        if name and email and phone and password:
            cursor.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
                           (name, email, phone, password))
            conn.commit()
            self.load_data()
            self.clear_entries()
            messagebox.showinfo("Éxito", "¡Se ha actualizado correctamente!.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        conn.close()

    def delete_user(self):
        if self.selected_id is not None:
            confirm = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este usuario?")
            if confirm:
                try:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id = ?", (self.selected_id,))
                    conn.commit()
                    conn.close()
                    self.load_data()
                    self.clear_entries()
                    self.selected_id = None
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                except:
                    messagebox.showwarning("Error!", "EL CRUD SE ENCUNTRA CORRUPTO.")
            else:
                messagebox.showinfo("Desestimación Cancelada", "Ninguna fila ha resultado dañada")
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CRUDApp(root)
    root.mainloop()
