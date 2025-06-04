import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import mysql.connector
from conexionDB import conexionDB

def citas():
    for row in tree.get_children():
        tree.delete(row)
    try:
        conexion = conexionDB()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM citas")
        citas = cursor.fetchall()
        
        if not citas:
            messagebox.showinfo("Información", "No hay citas registradas.")
            return
        
        for cita in citas:
            tree.insert("", "end", values=(cita[0], cita[1], cita[2]))
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
    finally:
        if 'conexion' in locals():
            conexion.close()




windows = tk.Tk()
windows.title("Tabla de Citas")
windows.geometry("600x400")

columns = ("ID", "Nombre", "Dirección", "Teléfono")
tree = ttk.Treeview(windows, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)
tree.pack(fill="both", expand=True, padx=10, pady=10)

citas_button = tk.Button(windows, text="Mostrar Citas", command=citas)
citas_button.pack(pady=10)

windows.mainloop()
