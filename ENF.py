import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from conexionDB import conexionDB
from Nueva_cita import CitaNueva

HEADER_BG = '#8FD3F4'
BUTTON_OP_BG = '#AAF0D1'
BUTTON_OP_FG = '#000000'
TABLE_BG = '#FFFFFF'
TIME_BG = '#E8F8EF'
TIME_FG = '#2E8B57'
CELL_BG = '#D3D3D3'
FOOTER_BG = '#F5F5F5'
DETAIL_BG = "#f0f0f0"
EDIT_BTN_BG = "#007bff"
CLOSE_BTN_BG = "#FF6347"

class ProximasCitasVentana:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.fecha_test = None  # fecha para probar, o None para hoy
        self.root = tk.Tk()
        self.root.title("Próximas Citas")
        self.root.geometry("900x720")
        self.root.configure(bg='black')

        self.celdas = {}
        self.detalles = {}

        self._crear_interfaz()
        self._cargar_citas()
        self.root.mainloop()

    def _crear_interfaz(self):
        self._crear_header()
        self._crear_topbar()
        self._crear_tabla_citas()
        self._crear_footer()

    def _crear_header(self):
        header = tk.Frame(self.root, bg=HEADER_BG, height=60, bd=2, relief='groove')
        header.pack(fill='x', side='top')

        logo = tk.Canvas(header, width=40, height=40, bg='white', highlightthickness=1)
        logo.create_oval(5, 5, 35, 35)
        logo.create_text(20, 20, text="L", font=("Arial", 14, "bold"))
        logo.pack(side='left', padx=10, pady=10)

        tk.Label(header, text="Logotipo", bg=HEADER_BG, fg='black',
                 font=("Arial", 14, "bold")).pack(side='left')
        tk.Label(header, text="Nombre institución", bg=HEADER_BG, fg='black',
                 font=("Arial", 16, "bold")).pack(side='right', padx=20)

    def _crear_topbar(self):
        topbar = tk.Frame(self.root, bg=FOOTER_BG, height=90, bd=1, relief='groove')
        topbar.pack(fill='x')



        # Submenus 
        op_btn = tk.Menubutton(topbar, text="Operaciones", bg=BUTTON_OP_BG,
                               fg=BUTTON_OP_FG, font=("Arial", 10, "bold"), relief='raised')
        op_menu = tk.Menu(op_btn, tearoff=0)
        op_menu.add_command(label="Nueva Cita", command=lambda: messagebox.showinfo("Nueva Cita", "No implementado"))
        op_menu.add_command(label="Buscar Cita", command=lambda: messagebox.showinfo("Buscar Cita", "No implementado"))
        op_btn.config(menu=op_menu)
        op_btn.pack(side='left', padx=20, pady=5)





        nombre = self._obtener_nombre_usuario()
        tk.Label(topbar, text="Bienvenido " + nombre, bg=FOOTER_BG, fg='black',
                 font=("Arial", 10, "bold")).pack(side='left', padx=20)

        tk.Label(topbar, text="Fecha (dd/mm/yyyy):", bg=FOOTER_BG).pack(side='left', padx=(20, 5))
        self.entry_fecha = tk.Entry(topbar, width=12)
        self.entry_fecha.pack(side='left')

        tk.Button(topbar, text="Cargar", command=self._actualizar_fecha).pack(side='left', padx=5)

        tk.Button(topbar, text="Cerrar Sesión", bg=CLOSE_BTN_BG, fg='white',
                  font=("Arial", 10, "bold"), command=self.root.destroy).pack(side='right', padx=10, pady=5)

    def _crear_tabla_citas(self):
        main_frame = tk.Frame(self.root, bg=TABLE_BG)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        semana_text = self._texto_semana()
        self.lbl_fecha = tk.Label(main_frame, text="Citas para la semana: " + semana_text,
                                 font=("Arial", 10, "bold"), bg=TABLE_BG)
        self.lbl_fecha.pack(pady=(10, 0), anchor='ne', padx=10)

        tk.Label(main_frame, text="¡PRÓXIMAS CITAS!", font=("Arial", 18, "bold"),
                 fg="#1DA1F2", bg=TABLE_BG).pack(pady=(0, 10))

        table_frame = tk.Frame(main_frame, bg=TABLE_BG, bd=2, relief='groove')
        table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.filas = 8
        self.horas = [(datetime.strptime("08:00", "%H:%M") + timedelta(minutes=30 * (i - 1))).strftime("%H:%M")
                      for i in range(1, self.filas + 1)]

        tk.Label(table_frame, text="", bg=TABLE_BG).grid(row=0, column=0, padx=5, pady=5)
        for i, dia in enumerate(self.dias, start=1):
            tk.Label(table_frame, text=dia, bg=TABLE_BG, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i, padx=8, pady=5)

        for r in range(1, self.filas + 1):
            tk.Label(table_frame, text=self.horas[r - 1], bg=TIME_BG, fg=TIME_FG,
                     font=("Arial", 10, "bold"))\
                .grid(row=r, column=0, padx=5, pady=5, sticky='nsew')
            for c in range(1, len(self.dias) + 1):
                celda = tk.Label(table_frame, text="", bg=CELL_BG, width=12, height=2,
                                 bd=1, relief='flat', cursor="hand2")
                celda.grid(row=r, column=c, padx=4, pady=4, sticky='nsew')
                celda.bind("<Button-1>", lambda e, rr=r, cc=c: self._on_cell_click(rr, cc))
                self.celdas[(r, c)] = celda

        for c in range(len(self.dias) + 1):
            table_frame.grid_columnconfigure(c, weight=1)
        for r in range(self.filas + 1):
            table_frame.grid_rowconfigure(r, weight=1)

    def _crear_footer(self):
        footer = tk.Frame(self.root, bg=FOOTER_BG, height=40, bd=1, relief='groove')
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="Pie de página", bg=FOOTER_BG,
                 font=("Arial", 14, "bold")).pack(pady=5)

    def _obtener_nombre_usuario(self):
        conexion = conexionDB()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM personal WHERE id = %s", (self.id_usuario,))
        result = cursor.fetchone()
        cursor.close()
        conexion.close()
        return result[0] if result else "Desconocido"

    def _actualizar_fecha(self):
        entrada = self.entry_fecha.get()
        try:
            self.fecha_test = datetime.strptime(entrada, "%d/%m/%Y").date()
            self.lbl_fecha.config(text="Citas para la semana: " + self._texto_semana())
            self._limpiar_tabla()
            self._cargar_citas()
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida. Usa el formato dd/mm/yyyy.")

    def _limpiar_tabla(self):
        for cel in self.celdas.values():
            cel.config(text="")
        self.detalles.clear()

    def _texto_semana(self):
        fecha = self.fecha_test or datetime.now().date()
        lunes = fecha - timedelta(days=fecha.weekday())  # lunes de esa semana
        sabado = lunes + timedelta(days=5)
        return f"{lunes.strftime('%d/%m/%Y')} - {sabado.strftime('%d/%m/%Y')}"

    def _cargar_citas(self):
        db = conexionDB()
        cursor = db.cursor()
        fecha = self.fecha_test or datetime.now().date()
        lunes = fecha - timedelta(days=fecha.weekday())
        sabado = lunes + timedelta(days=5)

        cursor.execute("SELECT tipo_usuario FROM personal WHERE id = %s", (self.id_usuario,))
        tipo = cursor.fetchone()
        es_recepcionista = tipo and tipo[0].lower() == "recepcionista"

        if es_recepcionista:
            cursor.execute("""
                SELECT 
                p.nombre, p.telefono, p.direccion,
                c.hora, c.fecha,
                per.nombre AS doctor, per.tipo_usuario AS especialidad,
                c.motivo
                FROM cita c
                JOIN paciente p ON c.id_paciente = p.id_paciente
                JOIN personal per ON p.id_personal = per.id
                WHERE c.fecha BETWEEN %s AND %s
            """, (lunes, sabado))
        else:
            cursor.execute("""
                SELECT 
                p.nombre, p.telefono, p.direccion,
                c.hora, c.fecha,
                per.nombre AS doctor, per.tipo_usuario AS especialidad,
                c.motivo
                FROM cita c
                JOIN paciente p ON c.id_paciente = p.id_paciente
                JOIN personal per ON p.id_personal = per.id
                WHERE c.fecha BETWEEN %s AND %s AND per.id = %s
            """, (lunes, sabado, self.id_usuario))

        for nombre, telefono, direccion, hora, fecha_cita, doctor, especialidad, motivo in cursor.fetchall():
            fecha_obj = fecha_cita if not isinstance(fecha_cita, str) else datetime.strptime(fecha_cita, "%Y-%m-%d").date()
            # calcular columna día (lunes=1,... sábado=6)
            dia_semana = fecha_obj.weekday()  # 0=Lun ... 5=Sab ... 6=Dom (no usado)
            if dia_semana > 5:
                continue
            col = dia_semana + 1

            # calcular fila según hora
            if isinstance(hora, str):
                hora_str = hora[:5]
            elif isinstance(hora, timedelta):
                segundos = int(hora.total_seconds())
                h = segundos // 3600
                m = (segundos % 3600) // 60
                hora_str = f"{h:02d}:{m:02d}"
            else:
                hora_str = hora.strftime("%H:%M")

            inicio_hora = datetime.strptime("08:00", "%H:%M")
            hora_cita = datetime.strptime(hora_str, "%H:%M")
            diferencia_minutos = (hora_cita - inicio_hora).total_seconds() / 60
            fila = int(diferencia_minutos // 30) + 1

            celda = self.celdas.get((fila, col))
            if celda:
                celda.config(text=nombre)
                self.detalles[(fila, col)] = {
                    "nombre": nombre,
                    "telefono": telefono,
                    "direccion": direccion,
                    "doctor": doctor,
                    "especialidad": especialidad,
                    "motivo": motivo,
                    "fecha": fecha_obj.strftime("%d/%m/%Y"),
                    "hora": hora_str
                }
        cursor.close()
        db.close()

    def _on_cell_click(self, r, c):
        data = self.detalles.get((r, c))
        if data:
            self._mostrar_detalles(data)

    def _mostrar_detalles(self, d):
        top = tk.Toplevel(self.root)
        top.title("Detalles de la Cita")
        w, h = 400, 350
        x = self.root.winfo_rootx() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.resizable(False, False)
        top.grab_set()
        top.configure(bg=DETAIL_BG)

        frm = tk.Frame(top, bg=DETAIL_BG, padx=20, pady=20)
        frm.pack(fill='both', expand=True)

        tk.Label(frm, text="DETALLES DEL PACIENTE", font=("Arial", 14, "bold"), bg=DETAIL_BG).pack(pady=(0, 15))

        for lbl, val in [("Nombre:", d["nombre"]), ("Teléfono:", d["telefono"]), ("Dirección:", d["direccion"])]:
            row = tk.Frame(frm, bg=DETAIL_BG); row.pack(fill='x', pady=2)
            tk.Label(row, text=lbl, width=12, anchor='e', bg=DETAIL_BG).pack(side='left')
            tk.Label(row, text=val, bg=DETAIL_BG).pack(side='left', padx=5)

        tk.Frame(frm, height=2, bg="gray").pack(fill='x', pady=10)
        tk.Label(frm, text="INFORMACIÓN DE LA CITA", font=("Arial", 12, "bold"), bg=DETAIL_BG).pack(pady=(5, 10))

        for lbl, val in [("Fecha:", d["fecha"]), ("Hora:", d["hora"]),
                         ("Doctor:", f"{d['doctor']} ({d['especialidad']})"),
                         ("Motivo:", d["motivo"])]:
            row = tk.Frame(frm, bg=DETAIL_BG); row.pack(fill='x', pady=2)
            tk.Label(row, text=lbl, width=12, anchor='e', bg=DETAIL_BG).pack(side='left')
            tk.Label(row, text=val, bg=DETAIL_BG).pack(side='left', padx=5)

        btns = tk.Frame(frm, bg=DETAIL_BG); btns.pack(pady=20)
        tk.Button(btns, text="Editar", width=10, bg=EDIT_BTN_BG, fg="white",
                  command=lambda: messagebox.showinfo("Editar", "Función editar")).pack(side='left', padx=5)
        tk.Button(btns, text="Cerrar", width=10, command=top.destroy).pack(side='left', padx=5)

if __name__ == "__main__":
    ProximasCitasVentana(id_usuario=1)
