import tkinter as tk
from tkinter import messagebox
from conexionDB import conexionDB
from tkcalendar import DateEntry
from datetime import datetime

class RegistroCitaVentana:
    def __init__(self, parent, on_close=None):
        self.on_close = on_close
        self.master = tk.Toplevel(parent)
        self.master.title("Registro de Citas")
        self.master.geometry("500x600")
        self.master.configure(bg="white")

        self.crear_interfaz()

    def crear_interfaz(self):
        titulo = tk.Label(self.master, text="Registrar Cita", font=("Arial", 20, "bold"), bg="#ADD8E6")
        titulo.pack(fill=tk.X)

        self.form_frame = tk.Frame(self.master, padx=20, pady=20, bg="white")
        self.form_frame.pack(pady=10)

        # Variables
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.nss_var = tk.StringVar()
        self.peso_var = tk.StringVar()
        self.altura_var = tk.StringVar()
        self.temperatura_var = tk.StringVar()
        self.hora_var = tk.StringVar()

        # Fecha actual
        self.fecha_actual = datetime.today().date()

        self.campos = [
            ("Nombre", self.nombre_var),
            ("Apellido", self.apellido_var),
            ("Teléfono", self.telefono_var),
            ("NSS", self.nss_var),
            ("Peso (kg)", self.peso_var),
            ("Altura (m)", self.altura_var),
            ("Temperatura (°C)", self.temperatura_var),
        ]

        for texto, variable in self.campos:
            tk.Label(self.form_frame, text=texto + ":", anchor="w", bg="white").pack(fill=tk.X, pady=2)
            tk.Entry(self.form_frame, textvariable=variable).pack(fill=tk.X, pady=2)

        # Campo de fecha con calendario
        tk.Label(self.form_frame, text="Fecha de la cita:", anchor="w", bg="white").pack(fill=tk.X, pady=2)
        self.fecha_entry = DateEntry(self.form_frame, width=18, background='darkblue',
                                     foreground='white', borderwidth=2, year=self.fecha_actual.year,
                                     month=self.fecha_actual.month, day=self.fecha_actual.day, date_pattern='yyyy-mm-dd')
        self.fecha_entry.pack(fill=tk.X, pady=2)

        # Campo de hora (editable manualmente)
        tk.Label(self.form_frame, text="Hora (HH:MM):", anchor="w", bg="white").pack(fill=tk.X, pady=2)
        tk.Entry(self.form_frame, textvariable=self.hora_var).pack(fill=tk.X, pady=2)

        # Botones
        btn_frame = tk.Frame(self.master, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Registrar", command=self.registrar_cita, bg="lightgreen").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos, bg="lightcoral").pack(side=tk.LEFT, padx=10)

    def registrar_cita(self):
        try:
            conn = conexionDB()
            cur = conn.cursor()

            sql = """
            INSERT INTO citas (
                Nombre_paciente, Apellido_paciente, telefono_paciente, NSS_paciente,
                Peso_paciente, Altura_paciente, temperatura_paciente, fecha_cita, hora_cita
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            datos = (
                self.nombre_var.get(),
                self.apellido_var.get(),
                self.telefono_var.get(),
                self.nss_var.get(),
                float(self.peso_var.get()),
                float(self.altura_var.get()),
                float(self.temperatura_var.get()),
                self.fecha_entry.get_date(),  # del calendario
                self.hora_var.get()
            )

            cur.execute(sql, datos)
            conn.commit()
            messagebox.showinfo("Éxito", "Cita registrada correctamente.")
            self.limpiar_campos()

            # Llama al callback para actualizar la tabla de citas
            if self.on_close:
                self.on_close()
            self.master.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la cita:\n{e}")
        finally:
            if conn:
                cur.close()
                conn.close()

    def limpiar_campos(self):
        for _, var in self.campos:
            var.set("")
        self.hora_var.set("")
        self.fecha_entry.set_date(datetime.today().date())