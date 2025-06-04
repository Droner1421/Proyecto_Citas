import tkinter as tk
import tkinter.messagebox as messagebox
import mysql.connector
from conexionDB import conexionDB
from datetime import datetime
import random

def guardar_paciente():
    id = random.randint(1000, 9999)  
    nombre = entry_nombre.get()
    documento = entry_documento.get()
    fecha_cita = entry_fecha_cita.get()
    hora_cita = entry_hora_cita.get()
    especialidad = entry_especialidad.get()
    medico = entry_medico.get()
    motivo = entry_motivo.get()
    estado = entry_estado.get()
    telefono = entry_telefono.get()
    observaciones = entry_observaciones.get()
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tipo_cita = entry_tipo_cita.get()

    conexion = conexionDB()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO citas
            (id, nombre, documento, fecha_cita, hora_cita, especialidad, medico, motivo, estado, telefono, observaciones, fecha_creacion, tipo_cita)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, nombre, documento, fecha_cita, hora_cita, especialidad, medico, motivo, estado, telefono, observaciones, fecha_creacion, tipo_cita))
        conexion.commit()
        messagebox.showinfo("Éxito", "Paciente guardado correctamente")
        for entry in entries:
            entry.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al guardar el paciente: {err}")
    finally:
        cursor.close()
        conexion.close()

windows = tk.Tk()
windows.title("Formulario de Pacientes")
windows.geometry("500x700")
windows.configure(bg='white')

labels = [
    "Nombre:",
    "Documento de identidad:",
    "Fecha de la cita (YYYY-MM-DD):",
    "Hora de la cita (HH:MM):",
    "Especialidad médica:",
    "Nombre del médico tratante:",
    "Motivo de la consulta:",
    "Estado de la cita:",
    "Teléfono o medio de contacto:",
    "Observaciones adicionales:",
    "Tipo de cita (presencial, virtual, telefónica):"
]

entries = []

for label_text in labels:
    label = tk.Label(windows, text=label_text, bg='white')
    label.pack(pady=3)
    entry = tk.Entry(windows)
    entry.pack(pady=3)
    entries.append(entry)

(entry_nombre, entry_documento, entry_fecha_cita, entry_hora_cita, entry_especialidad,
 entry_medico, entry_motivo, entry_estado, entry_telefono, entry_observaciones, entry_tipo_cita) = entries

guardar_button = tk.Button(windows, text="Guardar Paciente", command=guardar_paciente)
guardar_button.pack(pady=20)


windows.mainloop()