import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from conexionDB import conexionDB
from Nueva_cita import CitaNueva
from Dashboard import CitasDashboard

# Colores personalizados para la interfaz
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
    # Ventana principal para mostrar próximas citas
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.fecha_test = None  # fecha para probar, o None para hoy
        self.root = tk.Tk()
        self.root.title("Próximas Citas")
        self.root.geometry("900x720")
        self.root.configure(bg='black')
        # sefl.celdas para referencias a las celdas de la tabla
        self.celdas = {}
        # detalles para almacenar detalles de citas por celda
        self.detalles = {}
        # Crear la interfaz
        self._crear_interfaz()
        self._cargar_citas()
        self._iniciar_refresco_automatico()  
        self.root.mainloop()
    def _iniciar_refresco_automatico(self):
        # Refresca la tabla de citas cada 60 segundos (60000 ms)
        self._cargar_citas()
        self.root.after(5000, self._iniciar_refresco_automatico)
         # Crear la interfaz de usuario
    def _crear_interfaz(self):
        self._crear_header()
        self._crear_topbar()
        self.crear_tabla_citas()
        self._crear_footer()

    def abrir_dashboard(self):
        dashboard = CitasDashboard()
        dashboard.mostrar()
        
    def _crear_header(self):
        header = tk.Frame(self.root, bg=HEADER_BG, height=60, bd=2, relief='groove')
        header.pack(fill='x', side='top')
    

        # Logo en el header
        logo_image = Image.open("logo.jpg")  
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(header, image=logo, bg=HEADER_BG)
        logo_label.image = logo 
        logo_label.pack(side='left', padx=10)
        tk.Label(header, text="Casa de salud La Huanica", bg=HEADER_BG, fg='black',font=("Arial", 14, "bold")).pack(side='left', padx=20)
    # Crear la barra superior (topbar) con botones y nombre de usuario para organizar la interfaz
    def _crear_topbar(self):
        topbar = tk.Frame(self.root, bg=FOOTER_BG, height=90, bd=1, relief='groove')
        topbar.pack(fill='x')


        # Submenus 
        # crea un boton desplegable para operaciones
        op_btn = tk.Menubutton(topbar, text="Operaciones", bg=BUTTON_OP_BG,
                               fg=BUTTON_OP_FG, font=("Arial", 10, "bold"), relief='raised')
        # Crear un menú asociado al botón anterior
        op_menu = tk.Menu(op_btn, tearoff=0)
        # Agregar una opción llamada Nueva Cita que ejecuta la función _abrir_nueva_cita
        op_menu.add_command(label="Nueva Cita", command=self._abrir_nueva_cita)
        # Agregar una opción llamada Ver Gráfica que ejecuta la función graficar
        op_menu.add_command(label="Ver Gráfica", command= self.abrir_dashboard)
       
 
        # Asociar el menú al botón y empaquetarlo en la barra superior y darle tamaño 
        op_btn.config(menu=op_menu)
        op_btn.pack(side='left', padx=20, pady=5)

        # Mostrar nombre de la recepcionista
        #conexion con base de datos
        conexion = conexionDB()
        # Ejecuta consulta para obtener el nombre del usuario según su id
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM personal WHERE id = %s", (self.id_usuario,))
        # Obtener el resultado de la consulta y guardar en variable resultado
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado:
            #si se encuentra el usuario, mostrar su nombre en la barra superior
            nombre_medico = resultado[0]
            tk.Label(topbar, text=f"Bienvenido(a) Recepcionista: {nombre_medico}", bg=FOOTER_BG, font=("Arial", 10, "bold")).pack(side="left", padx=20)
        # Botón para cerrar sesión
        btn_cerrar = tk.Button(topbar, text="Cerrar Sesión", bg="#FF6347", fg='white',
                              command=self._cerrar_sesion)
        btn_cerrar.pack(side='right', padx=20, pady=5)

    def _abrir_nueva_cita(self):
        # Abre la ventana de nueva cita y fuerza refresco de la tabla al cerrar
            # Función para refrescar la tabla y actualizar la interfaz
        def refrescar_y_update():
            self._cargar_citas()
            self.root.update_idletasks()
        CitaNueva(master=self.root, on_save=refrescar_y_update)
        #cerrar la ventana actual y abrir la ventana de inicio
    def _cerrar_sesion(self):
        self.root.destroy()
        import Inicio
        Inicio.vistaapp()


    def crear_tabla_citas(self):
        # Crea el frame principal de  la tabla de citas
        main_frame = tk.Frame(self.root, bg=TABLE_BG)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Muestra la fecha
        semana_text = self._texto_semana()
        self.lbl_fecha = tk.Label(main_frame, text="Citas para la semana: " + semana_text,
                                 font=("Arial", 10, "bold"), bg=TABLE_BG)
        self.lbl_fecha.pack(pady=(10, 0), anchor='ne', padx=10)

        # Título de la tabla
        tk.Label(main_frame, text="¡PRÓXIMAS CITAS!", font=("Arial", 18, "bold"),
                 fg="#1DA1F2", bg=TABLE_BG).pack(pady=(0, 10))

       
        table_frame = tk.Frame(main_frame, bg=TABLE_BG, bd=2, relief='groove')
        table_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Nombres de los días y horas de las filas
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.filas = 8
        self.horas = [(datetime.strptime("08:00", "%H:%M") + timedelta(minutes=30 * (i - 1))).strftime("%H:%M")
                      for i in range(1, self.filas + 1)]

        # Encabezados de la tabla: fila de días 
        tk.Label(table_frame, text="", bg=TABLE_BG).grid(row=0, column=0, padx=5, pady=5)
        # Crear etiquetas para los días de la semana
        for i, dia in enumerate(self.dias, start=1):
            tk.Label(table_frame, text=dia, bg=TABLE_BG, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i, padx=8, pady=5)

        # Celdas de la tabla: filas de hora y dia
        for r in range(1, self.filas + 1):
             # Etiqueta de la hora en la primera columna
            tk.Label(table_frame, text=self.horas[r - 1], bg=TIME_BG, fg=TIME_FG,
                     font=("Arial", 10, "bold"))\
                .grid(row=r, column=0, padx=5, pady=5, sticky='nsew')
            for c in range(1, len(self.dias) + 1):
                
                celda = tk.Label(table_frame, text="", bg=CELL_BG, width=12, height=2,
                                 bd=1, relief='flat', cursor="hand2")
                celda.grid(row=r, column=c, padx=4, pady=4, sticky='nsew')
                celda.bind("<Button-1>", lambda e, rr=r, cc=c: self._on_cell_click(rr, cc))
                self.celdas[(r, c)] = celda

        # Configura el tamaño de las columnas y filas
        for c in range(len(self.dias) + 1):
            #establece el peso de las columnas para que se expandan uniformemente
            table_frame.grid_columnconfigure(c, weight=1)
        for r in range(self.filas + 1):
            table_frame.grid_rowconfigure(r, weight=1)
    # Crear el pie de página
    def _crear_footer(self):
        footer = tk.Frame(self.root, bg=FOOTER_BG, height=40, bd=1, relief='groove')
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="Pie de página", bg=FOOTER_BG,
                 font=("Arial", 14, "bold")).pack(pady=5)

    def obtener_nombre_usuario(self):
        # conexion con base de datos
        conexion = conexionDB()
        cursor = conexion.cursor()
        # Ejecuta  consulta para obtener el nombre del usuario según su id
        cursor.execute("SELECT nombre FROM personal WHERE id = %s", (self.id_usuario,))
        result = cursor.fetchone()
        # Cierra la conexión a la base de datos
        cursor.close()
        conexion.close()
        # Manda el nombre si se encontró, si no, se terminara mandando "Desconocido"
        return result[0] if result else "Desconocido"
   # Actualiza la fecha y recarga las citas en la tabla
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
    # Calcula el texto de la semana actual o de la fecha de prueba
    def _texto_semana(self):
        fecha = self.fecha_test or datetime.now().date()
        lunes = fecha - timedelta(days=fecha.weekday())  # lunes de esa semana
        sabado = lunes + timedelta(days=5)
        return f"{lunes.strftime('%d/%m/%Y')} - {sabado.strftime('%d/%m/%Y')}"

    def _cargar_citas(self):
        # Limpiar la tabla antes de cargar nuevas citas
        self._limpiar_tabla()
        db = conexionDB()
        cursor = db.cursor()
        # Calcular lunes y sábado de la semana actual 
        fecha = self.fecha_test or datetime.now().date()
        lunes = fecha - timedelta(days=fecha.weekday())
        sabado = lunes + timedelta(days=5)
        # Verificar si el usuario es recepcionista
        cursor.execute("SELECT tipo_usuario FROM personal WHERE id = %s", (self.id_usuario,))
        tipo = cursor.fetchone()
        es_recepcionista = tipo and tipo[0].lower() == "recepcionista"
        # Consulta para obtener citas de la semana
         # Si es recepcionista, obtiene todas las citas
        if es_recepcionista:
            # Consulta para obtener citas de la semana por medio de join entre tablas cita, paciente y personal y filtra por fecha  
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
        # Procesar cada cita y colocar en la tabla
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
            #hora en formato datetime para calcular fila
            inicio_hora = datetime.strptime("08:00", "%H:%M")
            hora_cita = datetime.strptime(hora_str, "%H:%M")
            diferencia_minutos = (hora_cita - inicio_hora).total_seconds() / 60
            # calcular fila (1=08:00, 2=08:30, ..., 8=11:30)
            fila = int(diferencia_minutos // 30) + 1

            celda = self.celdas.get((fila, col))
            # Si la celda existe, actualizar su texto y almacenar detalles
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
    # Maneja el clic en una celda para mostrar detalles de la cita
    def _on_cell_click(self, r, c):
        data = self.detalles.get((r, c))
        if data:
            self._mostrar_detalles(data)
    # Muestra una ventana emergente con detalles de la cita seleccionada
    def _mostrar_detalles(self, d):
        #diseño de la ventana de detalles 
        top = tk.Toplevel(self.root)
        top.title("Detalles de la Cita")
        w, h = 400, 650
        x = self.root.winfo_rootx() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.resizable(False, False)
        top.grab_set()
        top.configure(bg=DETAIL_BG)
    
        frm = tk.Frame(top, bg=DETAIL_BG, padx=20, pady=20)
        frm.pack(fill='both', expand=True)

        tk.Label(frm, text="DETALLES DEL PACIENTE", font=("Arial", 14, "bold"), bg=DETAIL_BG).pack(pady=(0, 15))
        #conexion con base de datos para obtener detalles del paciente y cita
        db = conexionDB()
        cursor = db.cursor()
            # Consulta para obtener detalles del paciente y cita
            # Realiza una consulta para obtener detalles del paciente según el nombre y la fecha/hora por un JOIN entre tablas paciente y cita
        cursor.execute("""
            SELECT p.id_paciente, p.nombre, p.apellido_paterno, p.apellido_materno, p.direccion, p.telefono, p.nss,
                   p.temperatura, p.peso, p.edad, p.talla
            FROM paciente p
            JOIN cita c ON c.id_paciente = p.id_paciente
            WHERE p.nombre = %s AND c.fecha = %s AND c.hora = %s
        """, (
            d["nombre"],
            datetime.strptime(d["fecha"], "%d/%m/%Y").strftime("%Y-%m-%d"),
            d["hora"]
        ))
        paciente = cursor.fetchone()

        cursor.execute("""
            SELECT c.id_cita, c.motivo, per.nombre, per.tipo_usuario
            FROM cita c
            JOIN paciente p ON c.id_paciente = p.id_paciente
            JOIN personal per ON p.id_personal = per.id
            WHERE p.nombre = %s AND c.fecha = %s AND c.hora = %s
        """, (
            d["nombre"],
            datetime.strptime(d["fecha"], "%d/%m/%Y").strftime("%Y-%m-%d"),
            d["hora"]
        ))
        cita = cursor.fetchone()
        cursor.close()
        db.close()
        # Mostrar detalles del paciente y cita en la ventana emergente estos son los labels 
        #si se encuentra el paciente, mostrar sus detalles
        if paciente:
            labels = [
                ("ID Paciente:", paciente[0]),
                ("Nombre(s):", paciente[1]),
                ("Apellido paterno:", paciente[2]),
                ("Apellido materno:", paciente[3]),
                ("Dirección:", paciente[4]),
                ("Teléfono:", paciente[5]),
                ("NSS:", paciente[6]),
                ("Temperatura:", paciente[7]),
                ("Peso:", paciente[8]),
                ("Edad:", paciente[9]),
                ("Talla:", paciente[10])
            ]
            for lbl, val in labels:
                row = tk.Frame(frm, bg=DETAIL_BG)
                row.pack(fill='x', pady=2)
                tk.Label(row, text=lbl, width=16, anchor='e', bg=DETAIL_BG).pack(side='left')
                tk.Label(row, text=str(val), bg=DETAIL_BG).pack(side='left', padx=5)
        #separador entre secciones de detalles 
        tk.Frame(frm, height=2, bg="gray").pack(fill='x', pady=10)
        tk.Label(frm, text="INFORMACIÓN DE LA CITA", font=("Arial", 12, "bold"), bg=DETAIL_BG).pack(pady=(5, 10))
        #si se encuentra la cita, mostrar sus detalles
        if cita:
            # detalles de la cita labes donde se muestra el id, fecha, hora, motivo, doctor y especialidad
            cita_labels = [
                ("ID Cita:", cita[0]),
                ("Fecha:", d["fecha"]),
                ("Hora:", d["hora"]),
                ("Motivo:", cita[1]),
                ("Doctor:", f"{cita[2]} ({cita[3]})")
            ]
            # Mostrar cada detalle en una fila esto es un ciclo for que recorre los labels y los muestra 
            for lbl, val in cita_labels:
                row = tk.Frame(frm, bg=DETAIL_BG)
                row.pack(fill='x', pady=2)
                tk.Label(row, text=lbl, width=16, anchor='e', bg=DETAIL_BG).pack(side='left')
                tk.Label(row, text=str(val), bg=DETAIL_BG).pack(side='left', padx=5)

        btns = tk.Frame(frm, bg=DETAIL_BG)
        btns.pack(pady=20)
        #cierra la ventana de detalles y abre la ventana de editar cita mandando el id de la cita si existe
        def editar_y_cerrar():
            top.destroy()
            self.root.after(10, lambda: CitaNueva(master=self.root, id_cita=cita[0] if cita else None))
        # Botones para editar o cerrar
        tk.Button(btns, text="Editar", width=10, bg=EDIT_BTN_BG, fg="white", command=editar_y_cerrar).pack(side='left', padx=5)
        tk.Button(btns, text="Cerrar", width=10, bg=CLOSE_BTN_BG, fg="white", command=top.destroy).pack(side='left', padx=5)

if __name__ == "__main__":
    ProximasCitasVentana(id_usuario=1)
