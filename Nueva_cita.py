import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime
from conexionDB import conexionDB
import tkinter.ttk as ttk

class CitaNueva(tk.Toplevel):
    def _bind_id_cita_lookup(self):
        entry_id = self.entries["ID Cita:"]
        entry_id.bind("<FocusOut>", self._on_id_cita_focus_out)
        entry_id.bind("<Return>", self._on_id_cita_focus_out)

    def _on_id_cita_focus_out(self, event=None):
        id_cita = self.entries["ID Cita:"].get()
        if id_cita and id_cita.isdigit():
            self.cargar_datos_de_cita(int(id_cita))

    def __init__(self, master=None, on_save=None, id_cita=None):
        super().__init__(master)
        self.on_save = on_save
        self.title("Gestión de Citas")
        self.geometry("750x700")
        self.configure(bg="#f0f8ff")
        self.crear_encabezado()
        self.crear_vista()
        self._bind_id_cita_lookup()
        if id_cita is not None:
            self.cargar_datos_de_cita(id_cita)

    def crear_encabezado(self):
        encabezado = tk.Frame(self, bg="#69BEF3", height=50)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="Casa de salud La Huanica", bg="#81d4fa", fg="black",
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
                entry = tk.Entry(contenido, bg="white", width=30, state="readonly")
                self.hora_var = tk.StringVar()
                entry.config(textvariable=self.hora_var)
                self.entries[texto] = entry
                entry.grid(row=fila, column=1, padx=5, pady=5)
                btn_reloj = tk.Button(contenido, text="Editar", command=self._editar_hora)
                btn_reloj.grid(row=fila, column=2, padx=5)
                continue
            elif texto == "Nombre(s):":
                entry = tk.Entry(contenido, bg="white", width=30)
                entry.grid(row=fila, column=1, padx=5, pady=5, sticky="w")
                self.entries[texto] = entry

                # Botón Buscar usuarios (deshabilitado por defecto)
                self.btn_buscar_usuario = tk.Button(contenido, text="Buscar usuarios", state="disabled", command=self.buscar_usuarios)
                self.btn_buscar_usuario.grid(row=fila, column=2, padx=5)
                # Habilita/deshabilita el botón según si hay coincidencias
                entry.bind("<KeyRelease>", self._verificar_coincidencias)
                continue
            else:
                entry = tk.Entry(contenido, bg="white", width=40)
            entry.grid(row=fila, column=1, padx=5, pady=5)
            self.entries[texto] = entry

        # Sección para elegir el doctor (después de los campos de cita)
        fila_doctor = len(etiquetas)
        tk.Label(contenido, text="Doctor:", bg="#f0f8ff", fg="#000000",
                 font=("Arial", 10, "bold")).grid(row=fila_doctor, column=0, sticky="e", padx=5, pady=5)
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(contenido, textvariable=self.doctor_var, width=37, state="readonly")
        self.doctor_combo.grid(row=fila_doctor, column=1, padx=5, pady=5)

        # Cargar lista de doctores desde la base de datos
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM personal WHERE tipo_usuario='medico'")
        doctores = cursor.fetchall()
        cursor.close()
        conn.close()
        self.doctores_dict = {f"{nombre} (ID:{id})": id for id, nombre in doctores}
        self.doctor_combo['values'] = list(self.doctores_dict.keys())
        if self.doctor_combo['values']:
            self.doctor_combo.current(0)

        # Poner la hora actual 
        self._set_hora_estatica()

        # Botones de acción
        fila_botones = fila_doctor + 1
        tk.Button(contenido, text="Guardar Cita", bg="#00796b", fg="white", font=("Arial", 10, "bold"),
                  command=self.guardar_cita).grid(row=fila_botones, column=1, pady=10)
        tk.Button(contenido, text="Actualizar Cita", bg="#ffa000", fg="white", font=("Arial", 10, "bold"),
                  command=self.actualizar_cita).grid(row=fila_botones+1, column=1, pady=5)
        tk.Button(contenido, text="Eliminar Cita", bg="#d32f2f", fg="white", font=("Arial", 10, "bold"),
                  command=self.eliminar_cita).grid(row=fila_botones+2, column=1, pady=5)

    def _verificar_coincidencias(self, event=None):
        nombre = self.entries["Nombre(s):"].get()
        if not nombre:
            self.btn_buscar_usuario.config(state="disabled")
            return
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_paciente FROM paciente WHERE nombre LIKE %s",
            (nombre + "%",)
        )
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        if resultados:
            self.btn_buscar_usuario.config(state="normal")
        else:
            self.btn_buscar_usuario.config(state="disabled")

    def buscar_usuarios(self):
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
            messagebox.showinfo("Sin resultados", "No se encontraron usuarios con ese nombre.")
            return
        # Muestra una lista para seleccionar el paciente
        opciones = [f"ID: {r[0]} - {r[1]} {r[2]} {r[3]}" for r in resultados]
        seleccion = simpledialog.askinteger(
            "Seleccionar Paciente",
            "Pacientes encontrados:\n" + "\n".join(opciones) + "\n\nIngresa el ID del paciente:"
        )
        if seleccion and any(r[0] == seleccion for r in resultados):
            self.cargar_datos_paciente(seleccion)

    def _set_hora_estatica(self):
        if hasattr(self, 'hora_var'):
            self.hora_var.set(datetime.now().strftime("%H:%M:%S"))

    def _editar_hora(self):
        def guardar():
            valor = entry.get()
            try:
                datetime.strptime(valor, "%H:%M:%S")
                self.hora_var.set(valor)
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Formato inválido. Usa HH:MM:SS")
        win = tk.Toplevel(self)
        win.title("Editar Hora")
        win.geometry("220x100")
        win.resizable(False, False)
        tk.Label(win, text="Nueva hora (HH:MM:SS):").pack(pady=10)
        entry = tk.Entry(win, width=10)
        entry.pack(pady=5)
        entry.insert(0, self.hora_var.get())
        tk.Button(win, text="Guardar", command=guardar).pack(pady=5)

    def cargar_datos_de_cita(self, id_cita):
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_paciente, fecha, hora, motivo FROM cita WHERE id_cita=%s",
            (id_cita,))
        cita = cursor.fetchone()
        cursor.close()
        conn.close()

        if cita:
            self.entries["ID Cita:"].delete(0, tk.END)
            self.entries["ID Cita:"].insert(0, id_cita)
            self.entries["Fecha (YYYY-MM-DD):"].delete(0, tk.END)
            self.entries["Fecha (YYYY-MM-DD):"].insert(0, cita[1])
            if hasattr(self, 'hora_var'):
                self.hora_var.set(str(cita[2]))
            else:
                self.entries["Hora (HH:MM:SS):"].delete(0, tk.END)
                self.entries["Hora (HH:MM:SS):"].insert(0, cita[2])
            self.entries["Motivo:"].delete(0, tk.END)
            self.entries["Motivo:"].insert(0, cita[3])
            self.cargar_datos_paciente(cita[0])

    def cargar_datos_paciente(self, id_paciente):
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla FROM paciente WHERE id_paciente=%s",
            (id_paciente,))
        paciente = cursor.fetchone()
        cursor.close()
        conn.close()

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
        campos_obligatorios = [
            ("Nombre(s):", self.entries["Nombre(s):"].get()),
            ("Apellido paterno:", self.entries["Apellido paterno:"].get()),
            ("Apellido materno:", self.entries["Apellido materno:"].get()),
            ("Dirección:", self.entries["Dirección:"].get()),
            ("Teléfono:", self.entries["Teléfono:"].get()),
            ("NSS:", self.entries["NSS:"].get()),
            ("Temperatura:", self.entries["Temperatura:"].get()),
            ("Peso:", self.entries["Peso:"].get()),
            ("Edad:", self.entries["Edad:"].get()),
            ("Talla:", self.entries["Talla:"].get()),
            ("Fecha (YYYY-MM-DD):", self.entries["Fecha (YYYY-MM-DD):"].get()),
            ("Motivo:", self.entries["Motivo:"].get())
        ]
        faltantes = [campo for campo, valor in campos_obligatorios if not valor]
        if faltantes:
            messagebox.showerror("Error", f"Faltan datos en los siguientes campos:\n{', '.join(faltantes)}")
            return
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
        hora = self.entries["Hora (HH:MM:SS):"].get()
        try:
            hora_dt = datetime.strptime(hora, "%H:%M:%S")
            if hora_dt.hour > 11 or (hora_dt.hour == 11 and hora_dt.minute > 30):
                messagebox.showerror("Error", "La hora debe estar entre las 08:00:00 y las 11:30:00.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de hora inválido. Usa HH:MM:SS")
            return

        doctor_nombre = self.doctor_var.get()
        id_doctor = self.doctores_dict.get(doctor_nombre)
        if not id_doctor:
            messagebox.showerror("Error", "Debes seleccionar un doctor.")
            return

        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_cita FROM cita WHERE fecha=%s AND hora=%s",
            (fecha, hora)
        )
        cita_existente = cursor.fetchone()
        if cita_existente:
            messagebox.showerror("Error", "Ya hay una cita registrada en esa hora y fecha. Por favor ingresa una hora y fecha diferentes.")
            cursor.close()
            conn.close()
            return

        cursor.execute(
            "SELECT id_paciente FROM paciente WHERE nombre=%s AND apellido_paterno=%s AND apellido_materno=%s",
            (nombre, apellido_paterno, apellido_materno)
        )
        resultado = cursor.fetchone()
        
        if resultado:
            id_paciente = resultado[0]
            cursor.execute("""
                UPDATE paciente SET direccion=%s, telefono=%s, nss=%s, temperatura=%s, peso=%s, edad=%s, talla=%s, id_personal=%s
                WHERE id_paciente=%s
            """, (direccion, telefono, nss, temperatura, peso, edad, talla, id_doctor, id_paciente))
        else:
            cursor.execute("""
                INSERT INTO paciente (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla, id_personal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla, id_doctor))
            conn.commit()
            id_paciente = cursor.lastrowid

        cursor.execute(
            "INSERT INTO cita (id_paciente, fecha, hora, motivo) VALUES (%s, %s, %s, %s)",
            (id_paciente, fecha, hora, motivo)
        )
        conn.commit()
        id_cita = cursor.lastrowid

        messagebox.showinfo("Éxito", f"Cita registrada correctamente. ID: {id_cita}")
        self.entries["ID Cita:"].delete(0, tk.END)
        self.entries["ID Cita:"].insert(0, id_cita)
        cursor.close()
        conn.close()
        if self.on_save:
            self.on_save()
        self.destroy()

    def actualizar_cita(self):
        id_cita = self.entries["ID Cita:"].get()
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
        hora = self.entries["Hora (HH:MM:SS):"].get()
        motivo = self.entries["Motivo:"].get()
        doctor_nombre = self.doctor_var.get()
        id_doctor = self.doctores_dict.get(doctor_nombre)

        if not id_cita:
            messagebox.showerror("Error", "Debes ingresar el ID de la cita a actualizar.")
            return

        conn = conexionDB()
        cursor = conn.cursor()

        # Obtener el id_paciente de la cita
        cursor.execute("SELECT id_paciente FROM cita WHERE id_cita=%s", (id_cita,))
        res = cursor.fetchone()
        if not res:
            messagebox.showerror("Error", "No se encontró la cita.")
            cursor.close()
            conn.close()
            return
        id_paciente = res[0]

        # Actualizar datos del paciente
        cursor.execute("""
            UPDATE paciente SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, direccion=%s, telefono=%s, nss=%s,
            temperatura=%s, peso=%s, edad=%s, talla=%s, id_personal=%s
            WHERE id_paciente=%s
        """, (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla, id_doctor, id_paciente))

        # Actualizar datos de la cita
        cursor.execute("""
            UPDATE cita SET fecha=%s, hora=%s, motivo=%s
            WHERE id_cita=%s
        """, (fecha, hora, motivo, id_cita))

        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Cita y datos del paciente actualizados correctamente.")
        if self.on_save:
            self.on_save()
        self.destroy()

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
        if self.on_save:
            self.on_save()
        self.destroy()

    def limpiar_campos(self):
        for campo in ["ID Cita:", "Dirección:", "Teléfono:", "NSS:", "Temperatura:", "Peso:", "Edad:", "Talla:", "Hora (HH:MM:SS):", "Fecha (YYYY-MM-DD):", "Motivo:"]:
            self.entries[campo].delete(0, tk.END)

def main():
    root = tk.Tk()
    root.withdraw()
    app = CitaNueva(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()