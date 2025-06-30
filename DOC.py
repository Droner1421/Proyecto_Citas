import tkinter as tk
from tkinter import ttk, messagebox
from conexionDB import conexionDB
from datetime import datetime, timedelta

class vistadoc:
    def __init__(self, id_doctor):
        self.id_doctor = id_doctor
        self.fecha_referencia = datetime.strptime("2025-06-21", "%Y-%m-%d")  # Para pruebas
        # self.fecha_referencia = datetime.now()

        # Dimensiones de la tabla
        self.filas = 8
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

        # Colores
        self.colores = {
            "encabezado": "#8FD3F4",
            "boton_op_bg": "#AAF0D1",
            "boton_op_fg": "#000000",
            "tabla_fondo": "#FFFFFF",
            "hora_fondo": "#E8F8EF",
            "hora_fg": "#2E8B57",
            "celda_fondo": "#D3D3D3",
            "pie_fondo": "#F5F5F5"
        }

        self.celdas = {}
        self.info_cita = {}

        self.raiz = tk.Tk()
        self.raiz.title("Próximas Citas")
        self.raiz.geometry("800x700")
        self.raiz.configure(bg="black")

        self.construir_interfaz()
        self.cargar_citas()
        self.raiz.mainloop()

    def construir_interfaz(self):
        self.construir_encabezado()
        self.construir_barra_superior()
        self.construir_area_principal()
        self.construir_pie()

    def construir_encabezado(self):
        encabezado = tk.Frame(self.raiz, bg=self.colores["encabezado"], height=60, bd=2, relief="groove")
        encabezado.pack(fill="x")
        lienzo_logo = tk.Canvas(encabezado, width=40, height=40, bg="white", highlightthickness=1)
        lienzo_logo.create_oval(5, 5, 35, 35)
        lienzo_logo.create_text(20, 20, text="L", font=("Arial", 14, "bold"))
        lienzo_logo.pack(side="left", padx=10, pady=10)
        tk.Label(encabezado, text="Logotipo", bg=self.colores["encabezado"], font=("Arial", 14, "bold")).pack(side="left")
        tk.Label(encabezado, text="Nombre institución", bg=self.colores["encabezado"], font=("Arial", 16, "bold")).pack(side="right", padx=20)

    def construir_barra_superior(self):
        barra = tk.Frame(self.raiz, bg=self.colores["pie_fondo"], height=90, bd=1, relief="groove")
        barra.pack(fill="x")

        btn_operaciones = tk.Menubutton(barra, text="Operaciones", bg=self.colores["boton_op_bg"], fg=self.colores["boton_op_fg"], font=("Arial", 10, "bold"))
        menu_op = tk.Menu(btn_operaciones, tearoff=0)
        menu_op.add_command(label="Buscar Cita", command=lambda: messagebox.showinfo("Buscar Cita", "Función no implementada"))
        btn_operaciones.config(menu=menu_op)
        btn_operaciones.pack(side="left", padx=20, pady=5)

        conexion = conexionDB()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM personal WHERE id = %s", (self.id_doctor,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado:
            nombre_medico = resultado[0]
            tk.Label(barra, text=f"Bienvenido doctor {nombre_medico}", bg=self.colores["pie_fondo"], font=("Arial", 10, "bold")).pack(side="left", padx=20)

        tk.Button(barra, text="Cerrar Sesión", bg="#FF6347", fg="white", font=("Arial", 10, "bold"), command=self.raiz.destroy).pack(side="right", padx=10, pady=5)

    def construir_area_principal(self):
        self.area = tk.Frame(self.raiz, bg=self.colores["tabla_fondo"])
        self.area.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(self.area, text="📞", font=("Arial", 18), bg=self.colores["tabla_fondo"]).pack(anchor="nw", pady=(10,0), padx=10)
        tk.Label(self.area, text="¡PRÓXIMAS CITAS!", font=("Arial", 18, "bold"), fg="#1DA1F2", bg=self.colores["tabla_fondo"]).pack(pady=(0,10))

        hoy_str = self.fecha_referencia.strftime("%d/%m/%Y")
        tk.Label(self.area, text=f"Fecha de hoy: {hoy_str}", font=("Arial", 10, "bold"), bg=self.colores["tabla_fondo"]).pack(anchor="ne", padx=10)

        self.construir_tabla()

    def construir_tabla(self):
        cuadro = tk.Frame(self.area, bg=self.colores["tabla_fondo"], bd=2, relief="groove")
        cuadro.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(cuadro, text="", bg=self.colores["tabla_fondo"]).grid(row=0, column=0, padx=5, pady=5)
        for i, dia in enumerate(self.dias, start=1):
            tk.Label(cuadro, text=dia, bg=self.colores["tabla_fondo"], font=("Arial", 10, "bold")).grid(row=0, column=i, padx=8, pady=5)

        horas = [(datetime.strptime("08:00", "%H:%M") + timedelta(minutes=30*(i-1))).strftime("%H:%M") for i in range(1, self.filas+1)]
        for f in range(1, self.filas+1):
            tk.Label(cuadro, text=horas[f-1], bg=self.colores["hora_fondo"], fg=self.colores["hora_fg"], font=("Arial", 10, "bold")).grid(row=f, column=0, padx=5, pady=5, sticky="nsew")
            for c in range(1, len(self.dias)+1):
                lbl = tk.Label(cuadro, text="", bg=self.colores["celda_fondo"], width=12, height=2, bd=1, relief="flat", cursor="hand2")
                lbl.grid(row=f, column=c, padx=4, pady=4, sticky="nsew")
                lbl.bind("<Button-1>", lambda e, fil=f, col=c: self.al_hacer_click(fil, col))
                self.celdas[(f, c)] = lbl

        for c in range(len(self.dias)+1):
            cuadro.grid_columnconfigure(c, weight=1)
        for f in range(self.filas+1):
            cuadro.grid_rowconfigure(f, weight=1)

    def construir_pie(self):
        pie = tk.Frame(self.raiz, bg=self.colores["pie_fondo"], height=40, bd=1, relief="groove")
        pie.pack(fill="x", side="bottom")
        tk.Label(pie, text="Pie de página", bg=self.colores["pie_fondo"], font=("Arial", 14, "bold")).pack(pady=5)

    def cargar_citas(self):
        bd = conexionDB()
        cursor = bd.cursor()
        inicio_sem = self.fecha_referencia - timedelta(days=self.fecha_referencia.weekday())
        fin_sem = inicio_sem + timedelta(days=5)

        cursor.execute("""
            SELECT p.nombre, p.telefono, p.direccion,
                   c.hora, c.fecha,
                   per.nombre AS doctor, per.tipo_usuario AS especialidad,
                   c.motivo
            FROM cita c
            JOIN paciente p ON c.id_paciente = p.id_paciente
            JOIN personal per ON p.id_personal = per.id
            WHERE per.id = %s AND c.fecha BETWEEN %s AND %s
        """, (self.id_doctor, inicio_sem.date(), fin_sem.date()))

        for nom, tel, direc, hora, fecha, doc, esp, motivo in cursor.fetchall():
            fecha_obj = fecha if not isinstance(fecha, str) else datetime.strptime(fecha, "%Y-%m-%d").date()
            hora_str = self.formatear_hora(hora)
            dia_idx = fecha_obj.weekday()
            if 0 <= dia_idx <= 5:
                delta = datetime.strptime(hora_str, "%H:%M") - datetime.strptime("08:00", "%H:%M")
                fil = int(delta.seconds / 1800) + 1
                col = dia_idx + 1
                lbl = self.celdas.get((fil, col))
                if lbl:
                    lbl.config(text=nom)
                    self.info_cita[(fil, col)] = {
                        "nombre": nom, "telefono": tel, "direccion": direc,
                        "doctor": doc, "especialidad": esp,
                        "motivo": motivo,
                        "fecha": fecha_obj.strftime("%d/%m/%Y"),
                        "hora": hora_str
                    }

        cursor.close()
        bd.close()

    def formatear_hora(self, hora):
        if isinstance(hora, str):
            return hora[:5]
        elif isinstance(hora, timedelta):
            secs = int(hora.total_seconds())
            h, m = divmod(secs, 3600)
            return f"{h:02}:{m//60:02}"
        else:
            return hora.strftime("%H:%M")

    def al_hacer_click(self, fila, col):
        datos = self.info_cita.get((fila, col))
        if datos:
            self.mostrar_detalle_cita(datos)

    def mostrar_detalle_cita(self, datos):
        ventana = tk.Toplevel(self.raiz)
        ventana.title("Detalles de la Cita")
        ventana.geometry("400x450")
        ventana.resizable(False, False)
        ventana.grab_set()
        ventana.configure(bg="#f0f0f0")

        cont = tk.Frame(ventana, bg="#f0f0f0", padx=20, pady=20)
        cont.pack(fill="both", expand=True)

        tk.Label(cont, text="DETALLES DEL PACIENTE", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(0,15))

    # Datos básicos paciente
        for etiqueta, val in [("Nombre:", datos["nombre"]), 
                          ("Teléfono:", datos["telefono"]), 
                          ("Dirección:", datos["direccion"]),
                          ("NSS:", datos.get("nss", "N/A")),
                          ("Temperatura:", datos.get("temperatura", "N/A")),
                          ("Peso:", datos.get("peso", "N/A")),
                          ("Edad:", datos.get("edad", "N/A")),
                          ("Talla:", datos.get("talla", "N/A"))]:
            fila_cont = tk.Frame(cont, bg="#f0f0f0")
        fila_cont.pack(fill="x", pady=2)
        tk.Label(fila_cont, text=etiqueta, width=12, anchor="e", bg="#f0f0f0").pack(side="left")
        tk.Label(fila_cont, text=val, bg="#f0f0f0").pack(side="left", padx=5)

        tk.Frame(cont, height=2, bg="gray").pack(fill="x", pady=10)
        tk.Label(cont, text="INFORMACIÓN DE LA CITA", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=(5,10))

    # Info cita
        for etiqueta, val in [("Fecha:", datos["fecha"]), 
                          ("Hora:", datos["hora"]),
                          ("Doctor:", f"{datos['doctor']} ({datos['especialidad']})"),
                          ("Motivo:", datos["motivo"])]:
            fila_cont = tk.Frame(cont, bg="#f0f0f0")
            fila_cont.pack(fill="x", pady=2)
            tk.Label(fila_cont, text=etiqueta, width=12, anchor="e", bg="#f0f0f0").pack(side="left")
            tk.Label(fila_cont, text=val, bg="#f0f0f0").pack(side="left", padx=5)

        botones = tk.Frame(cont, bg="#f0f0f0")
        botones.pack(pady=20)

        tk.Button(botones, text="Editar", width=10, bg="#007bff", fg="white", 
              command=lambda: messagebox.showinfo("Editar", "Función editar")).pack(side="left", padx=5)
    
        tk.Button(botones, text="Finalizar Cita", width=12, bg="#28a745", fg="white", 
              command=lambda: self.finalizar_cita(datos)).pack(side="left", padx=5)
    
        tk.Button(botones, text="Cerrar", width=10, command=ventana.destroy).pack(side="left", padx=5)

    def finalizar_cita(self, datos):
        messagebox.showinfo("Finalizar Cita", f"Cita de {datos['nombre']} finalizada.")


if __name__ == "__main__":
    vistadoc()
