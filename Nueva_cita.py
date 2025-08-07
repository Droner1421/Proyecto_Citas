
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime
from conexionDB import conexionDB
import tkinter.ttk as ttk

class CitaNueva(tk.Toplevel):

    def __init__(self, master=None, on_save=None, id_cita=None):
        super().__init__(master)
        self.on_save = on_save
        self.title("Gestión de Citas")
        self.geometry("750x700")
        self.configure(bg="#f0f8ff")
        self.crear_encabezado()
        self.crear_vista()
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

        # --- Validadores ---
        def validar_numeros(texto):
            return texto.isdigit() or texto == ""
        

        def validar_letras(texto):
            return all(c.isalpha() or c.isspace() for c in texto) or texto == ""

        def validar_decimal(texto):
            if texto == "":
                return True
            try:
                float(texto)
                return True
            except ValueError:
                return False
         
        def validar_telefono(texto):
            return (texto.isdigit() or texto == "") and len(texto) <= 10

        def validar_nss(texto):
            return (texto.isdigit() or texto == "") and len(texto) <= 11

        def validar_edad(texto):
            if texto == "":
                return True
            if texto.isdigit():
                return 0 <= int(texto) <= 120
            return False

        vcmd_num = contenido.register(validar_numeros)
        vcmd_let = contenido.register(validar_letras)
        vcmd_dec = contenido.register(validar_decimal)
        vcmd_tel = contenido.register(validar_telefono)
        vcmd_nss = contenido.register(validar_nss)
        vcmd_edad = contenido.register(validar_edad)

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
            ("Hora:", 11),
            ("Fecha (YYYY-MM-DD):", 12),
            ("Motivo:", 13)
        ]

        self.entries = {}

        for texto, fila in etiquetas:
            tk.Label(contenido, text=texto, bg="#f0f8ff", fg="#000000",
                     font=("Arial", 10, "bold")).grid(row=fila, column=0, sticky="e", padx=10, pady=6)

            if texto == "ID Cita:":
                self.id_cita_label = tk.Label(contenido, text="", bg="white", fg="black", width=40, anchor="w", relief="sunken")
                self.id_cita_label.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")

            elif texto == "Fecha (YYYY-MM-DD):":
                entry = DateEntry(contenido, date_pattern="yyyy-mm-dd", background="#81d4fa", width=37)
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry
            elif texto in ["Apellido paterno:", "Apellido materno:"]:
                entry = tk.Entry(contenido, bg="white", width=40, validate="key", validatecommand=(vcmd_let, "%P"))
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

            elif texto == "Hora:":
                horarios = ["08:00:00", "08:30:00", "09:00:00", "09:30:00",
                            "10:00:00", "10:30:00", "11:00:00", "11:30:00"]
                self.hora_var = tk.StringVar()
                self.hora_combo = ttk.Combobox(contenido, textvariable=self.hora_var, values=horarios, width=37, state="readonly")
                self.hora_combo.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.hora_combo.current(0)
                self.entries[texto] = self.hora_combo

            elif texto == "Nombre(s):":
                entry = tk.Entry(contenido, bg="white", width=40, validate="key", validatecommand=(vcmd_let, "%P"))
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

                self.btn_buscar_usuario = tk.Button(contenido, text="Buscar usuarios", state="disabled", command=self.buscar_usuarios)
                self.btn_buscar_usuario.grid(row=fila, column=2, padx=10, pady=6, sticky="ew")
                entry.bind("<KeyRelease>", self._verificar_coincidencias)

            elif texto == "Teléfono:":
                entry = tk.Entry(contenido, bg="white", width=40, validate="key", validatecommand=(vcmd_tel, "%P"))
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

            elif texto == "NSS:":
                entry = tk.Entry(contenido, bg="white", width=40, validate="key", validatecommand=(vcmd_nss, "%P"))
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

            elif texto in ["Temperatura:", "Peso:", "Talla:"]:
                entry = tk.Entry(contenido, bg="white", width=40, validate="key", validatecommand=(vcmd_dec, "%P"))
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

            elif texto == "Edad:":
                entry = tk.Entry(contenido, bg="white", width=40, validate="key", validatecommand=(vcmd_edad, "%P"))
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

            else:
                entry = tk.Entry(contenido, bg="white", width=40)
                entry.grid(row=fila, column=1, padx=10, pady=6, sticky="ew")
                self.entries[texto] = entry

        # Doctor combobox alineado
        fila_doctor = len(etiquetas)
        tk.Label(contenido, text="Doctor:", bg="#f0f8ff", fg="#000000",
                 font=("Arial", 10, "bold")).grid(row=fila_doctor, column=0, sticky="e", padx=10, pady=6)
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(contenido, textvariable=self.doctor_var, width=37, state="readonly")
        self.doctor_combo.grid(row=fila_doctor, column=1, padx=10, pady=6, sticky="ew")

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

        self._set_hora_estatica()

        # Botones alineados en un frame
        fila_botones = fila_doctor + 1
        botones_frame = tk.Frame(contenido, bg="#FFFFFF")
        botones_frame.grid(row=fila_botones, column=0, columnspan=3, pady=15, sticky="ew")
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)
        botones_frame.columnconfigure(2, weight=1)

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
            self.id_cita_label.config(text=str(id_cita))
            self.entries["Fecha (YYYY-MM-DD):"].set_date(cita[1])
            if hasattr(self, 'hora_var'):
                self.hora_var.set(str(cita[2]))
            else:
                self.entries["Hora:"].delete(0, tk.END)
                self.entries["Hora:"].insert(0, cita[2])
            self.entries["Motivo:"].delete(0, tk.END)
            self.entries["Motivo:"].insert(0, cita[3])
            self.cargar_datos_paciente(cita[0])
        else:
            self.id_cita_label.config(text="")

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
            if campo not in ["Fecha (YYYY-MM-DD):", "Motivo:", "Hora:"]:
                self.entries[campo].delete(0, tk.END)

        if paciente:
            claves = [
                "Nombre(s):", "Apellido paterno:", "Apellido materno:", "Dirección:", "Teléfono:", "NSS:", "Temperatura:", "Peso:", "Edad:", "Talla:"
            ]
            for i, clave in enumerate(claves):
                if paciente[i] is not None:
                    self.entries[clave].insert(0, paciente[i])

    def guardar_cita(self):
        # Validar campos obligatorios
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
            ("Fecha (YYYY-MM-DD):", self.entries["Fecha (YYYY-MM-DD):"].get_date().strftime("%Y-%m-%d")),
            ("Motivo:", self.entries["Motivo:"].get())
        ]
        faltantes = [campo for campo, valor in campos_obligatorios if not valor]
        if faltantes:
            messagebox.showerror("Error", f"Faltan datos en los siguientes campos:\n{', '.join(faltantes)}")
            return

        # Validar campos específicos
        telefono = self.entries["Teléfono:"].get()
        if len(telefono) != 10:
            messagebox.showerror("Error", "El teléfono debe tener exactamente 10 dígitos.")
            return

        nss = self.entries["NSS:"].get()
        if len(nss) != 11:
            messagebox.showerror("Error", "El NSS debe tener exactamente 11 dígitos.")
            return

        temperatura_str = self.entries["Temperatura:"].get()
        if not temperatura_str or not temperatura_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Temperatura inválida.")
            return
        temperatura = float(temperatura_str)
        if not (30 <= temperatura <= 45):
            messagebox.showerror("Error", "La temperatura debe estar entre 30 y 45 °C.")
            return

        peso_str = self.entries["Peso:"].get()
        if not peso_str or not peso_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Peso inválido.")
            return
        peso = float(peso_str)
        if not (1 <= peso <= 500):
            messagebox.showerror("Error", "El peso debe estar entre 1 y 500 kg.")
            return

        talla_str = self.entries["Talla:"].get()
        if not talla_str or not talla_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Talla inválida.")
            return
        talla = float(talla_str)
        if not (0.3 <= talla <= 3):
            messagebox.showerror("Error", "La talla debe estar entre 0.3 y 3 metros.")
            return

        edad_str = self.entries["Edad:"].get()
        if not edad_str or not edad_str.isdigit():
            messagebox.showerror("Error", "Edad inválida.")
            return
        edad = int(edad_str)
        if not (0 <= edad <= 120):
            messagebox.showerror("Error", "La edad debe estar entre 0 y 120 años.")
            return
        
        # nombre y apellidos deben tener 3 caracteres como mínimo
        if len(self.entries["Nombre(s):"].get()) < 3:
            messagebox.showerror("Error", "Ingresa un nombre valido.")
            return
        if len(self.entries["Apellido paterno:"].get()) < 3:
            messagebox.showerror("Error", "Ingresa un apellido paterno valido.")
            return
        if len(self.entries["Apellido materno:"].get()) < 3:
            messagebox.showerror("Error", "Ingresa un apellido materno valido.")
            return
        # Validar dirección
        if len(self.entries["Dirección:"].get()) < 5:
            messagebox.showerror("Error", "Ingresa una direccion valida.")
            return
        fecha = self.entries["Fecha (YYYY-MM-DD):"].get_date().strftime("%Y-%m-%d")
        motivo = self.entries["Motivo:"].get()
        hora = self.hora_var.get()

        try:
            hora_dt = datetime.strptime(hora, "%H:%M:%S")
            if hora_dt.hour < 8 or (hora_dt.hour > 11 or (hora_dt.hour == 11 and hora_dt.minute > 30)):
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
            (self.entries["Nombre(s):"].get(), self.entries["Apellido paterno:"].get(), self.entries["Apellido materno:"].get())
        )
        resultado = cursor.fetchone()

        if resultado:
            id_paciente = resultado[0]
            cursor.execute("""
                UPDATE paciente SET direccion=%s, telefono=%s, nss=%s, temperatura=%s, peso=%s, edad=%s, talla=%s, id_personal=%s
                WHERE id_paciente=%s
            """, (self.entries["Dirección:"].get(), telefono, nss, temperatura, peso, edad, talla, id_doctor, id_paciente))
        else:
            cursor.execute("""
                INSERT INTO paciente (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla, id_personal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.entries["Nombre(s):"].get(),
                self.entries["Apellido paterno:"].get(),
                self.entries["Apellido materno:"].get(),
                self.entries["Dirección:"].get(),
                telefono,
                nss,
                temperatura,
                peso,
                edad,
                talla,
                id_doctor
            ))
            conn.commit()
            id_paciente = cursor.lastrowid

        cursor.execute(
            "INSERT INTO cita (id_paciente, fecha, hora, motivo) VALUES (%s, %s, %s, %s)",
            (id_paciente, fecha, hora, motivo)
        )
        conn.commit()
        id_cita = cursor.lastrowid

        messagebox.showinfo("Éxito", f"Cita registrada correctamente. ID: {id_cita}")
        self.id_cita_label.config(text=str(id_cita))
        cursor.close()
        conn.close()
        if self.on_save:
            self.on_save()
        self.destroy()

    def actualizar_cita(self):
        id_cita = self.id_cita_label.cget("text")
        if not id_cita:
            messagebox.showerror("Error", "No hay ID de cita para actualizar.")
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
        fecha = self.entries["Fecha (YYYY-MM-DD):"].get_date().strftime("%Y-%m-%d")
        hora = self.hora_var.get()
        motivo = self.entries["Motivo:"].get()
        doctor_nombre = self.doctor_var.get()
        id_doctor = self.doctores_dict.get(doctor_nombre)

        conn = conexionDB()
        cursor = conn.cursor()

        cursor.execute("SELECT id_paciente FROM cita WHERE id_cita=%s", (id_cita,))
        res = cursor.fetchone()
        if not res:
            messagebox.showerror("Error", "No se encontró la cita.")
            cursor.close()
            conn.close()
            return
        id_paciente = res[0]

        cursor.execute("""
            UPDATE paciente SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, direccion=%s, telefono=%s, nss=%s,
            temperatura=%s, peso=%s, edad=%s, talla=%s, id_personal=%s
            WHERE id_paciente=%s
        """, (nombre, apellido_paterno, apellido_materno, direccion, telefono, nss, temperatura, peso, edad, talla, id_doctor, id_paciente))

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
        id_cita = self.id_cita_label.cget("text")
        if not id_cita:
            messagebox.showerror("Error", "Debes seleccionar una cita para eliminar.")
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
        self.id_cita_label.config(text="")
        for campo in ["Dirección:", "Teléfono:", "NSS:", "Temperatura:", "Peso:", "Edad:", "Talla:", "Motivo:"]:
            self.entries[campo].delete(0, tk.END)
        self.entries["Nombre(s):"].delete(0, tk.END)
        self.entries["Apellido paterno:"].delete(0, tk.END)
        self.entries["Apellido materno:"].delete(0, tk.END)
        self.entries["Fecha (YYYY-MM-DD):"].set_date(datetime.now())
        self.hora_var.set("08:00:00")
        if self.doctor_combo['values']:
            self.doctor_combo.current(0)

def main():
    root = tk.Tk()
    root.withdraw()
    app = CitaNueva(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
