import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime
from conexionDB import conexionDB

class CitaNueva(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Citas")
        self.geometry("750x700")
        self.configure(bg="#f0f8ff")
        self.crear_encabezado()
        self.crear_vista()

    def crear_encabezado(self):
        encabezado = tk.Frame(self, bg="#69BEF3", height=50)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="Nombre institución", bg="#81d4fa", fg="black",
                 font=("Helvetica", 14, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(encabezado, text="Gestión de Citas", bg="#81d4fa", fg="black",
                 font=("Helvetica", 12, "italic")).pack(side="right", padx=20)

    def crear_vista(self):
        contenido = tk.Frame(self, bg="#FFFFFF")
        contenido.pack(padx=20, pady=10, fill="both", expand=True)

        etiquetas = [
            ("ID Cita:", 0),
            ("Nombre(s):", 1),
            ("Apellido paterno:", 2),
            ("Apellido materno:", 3),
            ("Dirección:", 4),
            ("Teléfono:", 5),
            ("NSS:", 6),
            ("Temperatura:", 7),
            ("Peso:", 8),
            ("Edad:", 9),
            ("Talla:", 10),
            ("Hora (HH:MM:SS):", 11),
            ("Fecha (YYYY-MM-DD):", 12),
            ("Motivo:", 13)
        ]

        self.entries = {}

        for texto, fila in etiquetas:
            tk.Label(contenido, text=texto, bg="#f0f8ff", fg="#000000",
                     font=("Arial", 10, "bold")).grid(row=fila, column=0, sticky="e", padx=5, pady=5)
            if texto == "Fecha (YYYY-MM-DD):":
                entry = DateEntry(contenido, date_pattern="yyyy-mm-dd", background="#81d4fa", width=37)
            elif texto == "Hora (HH:MM:SS):":
                entry = tk.Entry(contenido, bg="white", width=40, state="readonly")
            else:
                entry = tk.Entry(contenido, bg="white", width=40)
            entry.grid(row=fila, column=1, padx=5, pady=5)
            self.entries[texto] = entry

        # Autocompletar al escribir o salir del campo Nombre(s)
        self.entries["Nombre(s):"].bind("<KeyRelease>", self.autocompletar_nombre)
        self.entries["Nombre(s):"].bind("<FocusOut>", self.autocompletar_nombre)

        # Botones de acción
        tk.Button(contenido, text="Guardar Cita", bg="#00796b", fg="white", font=("Arial", 10, "bold"),
                  command=self.guardar_cita).grid(row=14, column=1, pady=10)
        tk.Button(contenido, text="Actualizar Cita", bg="#ffa000", fg="white", font=("Arial", 10, "bold"),
                  command=self.actualizar_cita).grid(row=15, column=1, pady=5)
        tk.Button(contenido, text="Eliminar Cita", bg="#d32f2f", fg="white", font=("Arial", 10, "bold"),
                  command=self.eliminar_cita).grid(row=16, column=1, pady=5)

    def autocompletar_nombre(self, event=None):
        nombre = self.entries["Nombre(s):"].get()
        if not nombre:
            return
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_paciente, nombre, apellido_paterno, apellido_materno FROM paciente WHERE nombre LIKE %s",
            (nombre + "%",)
        )
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()

        if not resultados:
            self.limpiar_campos()
        elif len(resultados) == 1:
            paciente = resultados[0]
            self.entries["Nombre(s):"].delete(0, tk.END)
            self.entries["Nombre(s):"].insert(0, paciente[1])
            self.entries["Apellido paterno:"].delete(0, tk.END)
            self.entries["Apellido paterno:"].insert(0, paciente[2])
            self.entries["Apellido materno:"].delete(0, tk.END)
            self.entries["Apellido materno:"].insert(0, paciente[3])
            self.cargar_datos_paciente(paciente[0])
        else:
            opciones = [f"ID: {r[0]} - {r[1]} {r[2]} {r[3]}" for r in resultados]
            seleccion = simpledialog.askinteger(
                "Seleccionar Paciente",
                "Pacientes encontrados:\n" + "\n".join(opciones) + "\n\nIngresa el ID del paciente:"
            )
            if seleccion and any(r[0] == seleccion for r in resultados):
                self.cargar_datos_paciente(seleccion)

    def cargar_datos_paciente(self, id_paciente):
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla FROM paciente WHERE id_paciente=%s",
            (id_paciente,))
        paciente = cursor.fetchone()
        cursor.close()
        conn.close()

        # Limpia todos los campos menos los de cita
        for campo in self.entries:
            if campo not in ["ID Cita:", "Hora (HH:MM:SS):", "Fecha (YYYY-MM-DD):", "Motivo:"]:
                self.entries[campo].delete(0, tk.END)

        if paciente:
            claves = [
                "Nombre(s):", "Apellido paterno:", "Apellido materno:", "Dirección:", "Teléfono:", "NSS:", "Temperatura:", "Peso:", "Edad:", "Talla:"
            ]
            for i, clave in enumerate(claves):
                if paciente[i] is not None:
                    self.entries[clave].insert(0, paciente[i])

    def guardar_cita(self):
        nombre = self.entries["Nombre(s):"].get()
        apellido_paterno = self.entries["Apellido paterno:"].get()
        apellido_materno = self.entries["Apellido materno:"].get()
        direccion = self.entries["Dirección:"].get()
        telefono = self.entries["Teléfono:"].get()
        nss = self.entries["NSS:"].get()
        temperatura = self.entries["Temperatura:"].get()
        peso = self.entries["Peso:"].get()
        edad = self.entries["Edad:"].get()
        talla = self.entries["Talla:"].get()
        fecha = self.entries["Fecha (YYYY-MM-DD):"].get()
        motivo = self.entries["Motivo:"].get()

        # Hora automática
        hora_actual = datetime.now().strftime("%H:%M:%S")
        self.entries["Hora (HH:MM:SS):"].config(state="normal")
        self.entries["Hora (HH:MM:SS):"].delete(0, tk.END)
        self.entries["Hora (HH:MM:SS):"].insert(0, hora_actual)
        self.entries["Hora (HH:MM:SS):"].config(state="readonly")

        hora = hora_actual

        conn = conexionDB()
        cursor = conn.cursor()

        # Buscar paciente por nombre y apellidos exactos
        cursor.execute(
            "SELECT id_paciente FROM paciente WHERE nombre=%s AND apellido_paterno=%s AND apellido_materno=%s",
            (nombre, apellido_paterno, apellido_materno)
        )
        resultado = cursor.fetchone()

        if resultado:
            id_paciente = resultado[0]
            # Actualizar datos del paciente (con temperatura, peso, talla)
            cursor.execute("""
                UPDATE paciente SET direccion=%s, telefono=%s, nss=%s, temperatura=%s, peso=%s, edad=%s, talla=%s
                WHERE id_paciente=%s
            """, (direccion, telefono, nss, temperatura, peso, edad, talla, id_paciente))
        else:
            # Insertar nuevo paciente (con temperatura, peso, talla)
            cursor.execute("""
                INSERT INTO paciente (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla, id_personal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla))
            conn.commit()
            id_paciente = cursor.lastrowid

        # Insertar la cita (sin temperatura, peso, talla)
        cursor.execute("""
            INSERT INTO cita (id_paciente, hora, fecha, motivo)
            VALUES (%s, %s, %s, %s)
        """, (
            id_paciente,
            hora,
            fecha,
            motivo
        ))
        conn.commit()
        id_cita = cursor.lastrowid

        messagebox.showinfo("Éxito", f"Cita registrada correctamente. ID: {id_cita}")
        self.entries["ID Cita:"].delete(0, tk.END)
        self.entries["ID Cita:"].insert(0, id_cita)
        cursor.close()
        conn.close()
        # No limpiar campos para que se vea el ID

    def actualizar_cita(self):
        id_cita = self.entries["ID Cita:"].get()
        fecha = self.entries["Fecha (YYYY-MM-DD):"].get()
        hora = self.entries["Hora (HH:MM:SS):"].get()
        motivo = self.entries["Motivo:"].get()
        if not id_cita:
            messagebox.showerror("Error", "Debes ingresar el ID de la cita a actualizar.")
            return
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cita SET fecha=%s, hora=%s, motivo=%s
            WHERE id_cita=%s
        """, (fecha, hora, motivo, id_cita))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Cita actualizada correctamente.")

    def eliminar_cita(self):
        id_cita = self.entries["ID Cita:"].get()
        if not id_cita:
            messagebox.showerror("Error", "Debes ingresar el ID de la cita a eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que deseas eliminar esta cita?"):
            return
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cita WHERE id_cita=%s", (id_cita,))
        conn.commit()
        cursor.close()
        conn.close()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Cita eliminada correctamente.")

    def limpiar_campos(self):
        for campo in ["ID Cita:", "Dirección:", "Teléfono:", "NSS:", "Temperatura:", "Peso:", "Edad:", "Talla:", "Hora (HH:MM:SS):", "Fecha (YYYY-MM-DD):", "Motivo:"]:
            self.entries[campo].delete(0, tk.END)

# Para llamar desde otro archivo:
# from Nueva_cita import CitaNueva
# ventana_cita = CitaNueva(master=ventana_principal)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = CitaNueva(master=root)
    app.mainloop()