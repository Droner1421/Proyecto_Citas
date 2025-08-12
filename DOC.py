import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from conexionDB import conexionDB
from Nueva_cita import CitaNueva
from PIL import Image, ImageTk
from Dashboard import CitasDashboard

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

class vistadoc:
    def __init__(self, id_doctor):
        #ventana principal del doctor ajuste de resolucion y color de fondo
        # ID del doctor actualmente conectado
        self.id_doctor = id_doctor
        self.fecha_test = None  # fecha para probar, o None para hoy
        self.root = tk.Tk()
        self.root.title("Próximas Citas")
        self.root.geometry("900x720")
        self.root.configure(bg='black')
        #para referirse a las celdas y detalles de las citas
        self.celdas = {}
        # detalles de las citas
        self.detalles = {}
        # Crear la interfaz
        self._crear_interfaz()
        self._cargar_citas()
        self._iniciar_refresco_automatico()
        self.root.mainloop()
     #refresca la tabla 
    def _iniciar_refresco_automatico(self):
        self._cargar_citas()
        self.root.after(5000, self._iniciar_refresco_automatico)

    def abrir_dashboard(self):
        dashboard = CitasDashboard()
        dashboard.mostrar()

    #crea la interfaz llamando a los metodos de crear header, topbar, tabla de citas y footer
    def _crear_interfaz(self):
        self._crear_header()
        self._crear_topbar()
        self.crear_tabla_citas()
        self._crear_footer()
    #crea el header con el logo y el nombre de la clinica
    def _crear_header(self):
        header = tk.Frame(self.root, bg=HEADER_BG, height=60, bd=2, relief='groove')
        header.pack(fill='x', side='top')

        # Logo
        logo_image = Image.open("logo.jpg")  
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(header, image=logo, bg=HEADER_BG)
        logo_label.image = logo 
        logo_label.pack(side='left', padx=10)
        tk.Label(header, text="Casa de salud La Huanica", bg=HEADER_BG, fg='black',font=("Arial", 14, "bold")).pack(side='left', padx=20)
    #crea la topbar con el boton de ver grafica, el nombre del doctor y el boton de cerrar sesion
    def _crear_topbar(self):
        topbar = tk.Frame(self.root, bg=FOOTER_BG, height=90, bd=1, relief='groove')
        topbar.pack(fill='x')
        # Botón de visualización grafica    
        graficar_btn = tk.Button(topbar, text="Ver Gráfica", command=self.abrir_dashboard, bg=BUTTON_OP_BG, fg=BUTTON_OP_FG)
        graficar_btn.pack(side='left', padx=20, pady=5)


      

        # Mostrar nombre del doctor
        conexion = conexionDB()
        cursor = conexion.cursor()
        # Consulta para obtener el nombre del doctor
        cursor.execute("SELECT nombre FROM personal WHERE id = %s", (self.id_doctor,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado:
            nombre_medico = resultado[0]
            tk.Label(topbar, text=f"Bienvenido Doctor: {nombre_medico}", bg=FOOTER_BG, font=("Arial", 10, "bold")).pack(side="left", padx=20)

        btn_cerrar = tk.Button(topbar, text="Cerrar Sesión", bg="#FF6347", fg='white',
                              command=self._cerrar_sesion)
        btn_cerrar.pack(side='right', padx=20, pady=5)
   #boton para abrir la ventana de nueva cita
    def _abrir_nueva_cita(self):
        def refrescar_y_update():
            self._cargar_citas()
            self.root.update_idletasks()
        CitaNueva(master=self.root, on_save=refrescar_y_update)
    #cerrar sesion y volver a la ventana de inicio
    def _cerrar_sesion(self):
        self.root.destroy()
        import Inicio
        Inicio.vistaapp()
    #crea la tabla de citas con los dias de la semana y las horas
    def crear_tabla_citas(self):
        #marco principal de la tabla
        main_frame = tk.Frame(self.root, bg=TABLE_BG)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        #semana_text obtiene el texto de la semana actual
        semana_text = self._texto_semana()
        #etiqueta 
        self.lbl_fecha = tk.Label(main_frame, text="Citas para la semana: " + semana_text,
                                 font=("Arial", 10, "bold"), bg=TABLE_BG)
        self.lbl_fecha.pack(pady=(10, 0), anchor='ne', padx=10)
         #etiqueta de proximas citas
        tk.Label(main_frame, text="¡PRÓXIMAS CITAS!", font=("Arial", 18, "bold"),
                 fg="#1DA1F2", bg=TABLE_BG).pack(pady=(0, 10))
       #frame de la tabla
        table_frame = tk.Frame(main_frame, bg=TABLE_BG, bd=2, relief='groove')
        table_frame.pack(padx=10, pady=10, fill='both', expand=True)
        #dias de la semana y horas de atencion
        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.filas = 8
        self.horas = [(datetime.strptime("08:00", "%H:%M") + timedelta(minutes=30 * (i - 1))).strftime("%H:%M")
                      for i in range(1, self.filas + 1)]
        # Crear encabezados de la tabla
        tk.Label(table_frame, text="", bg=TABLE_BG).grid(row=0, column=0, padx=5, pady=5)
        for i, dia in enumerate(self.dias, start=1):
            tk.Label(table_frame, text=dia, bg=TABLE_BG, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i, padx=8, pady=5)
        #crea las celdas de la tabla y las enlaza con el metodo de click 
        for r in range(1, self.filas + 1):
            #define la etiqueta de las horas en la primera columna
            tk.Label(table_frame, text=self.horas[r - 1], bg=TIME_BG, fg=TIME_FG,
                     font=("Arial", 10, "bold"))\
                .grid(row=r, column=0, padx=5, pady=5, sticky='nsew')
            #crea las celdas de la tabla por medio de un ciclo for 
            for c in range(1, len(self.dias) + 1):
                celda = tk.Label(table_frame, text="", bg=CELL_BG, width=12, height=2,
                                 bd=1, relief='flat', cursor="hand2")
                celda.grid(row=r, column=c, padx=4, pady=4, sticky='nsew')
                celda.bind("<Button-1>", lambda e, rr=r, cc=c: self._on_cell_click(rr, cc))
                self.celdas[(r, c)] = celda
        # Configurar expansión de filas y columnas
        for c in range(len(self.dias) + 1):
            #dar peso a las columnas para que se expandan
            table_frame.grid_columnconfigure(c, weight=1)
        for r in range(self.filas + 1):
            table_frame.grid_rowconfigure(r, weight=1)
    #crea el footer de la ventana
    def _crear_footer(self):
        footer = tk.Frame(self.root, bg=FOOTER_BG, height=40, bd=1, relief='groove')
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="Pie de página", bg=FOOTER_BG,
                 font=("Arial", 14, "bold")).pack(pady=5)
    #obtiene el texto de la semana actual
    def _texto_semana(self):
        fecha = self.fecha_test or datetime.now().date()
        lunes = fecha - timedelta(days=fecha.weekday())
        sabado = lunes + timedelta(days=5)
        return f"{lunes.strftime('%d/%m/%Y')} - {sabado.strftime('%d/%m/%Y')}"
    #limpia la tabla de citas
    def _limpiar_tabla(self):
        for cel in self.celdas.values():
            cel.config(text="")
        self.detalles.clear()
    #carga las citas de la base de datos y las muestra en la tabla
    def _cargar_citas(self):
        self._limpiar_tabla()
        db = conexionDB()
        cursor = db.cursor()
        fecha = self.fecha_test or datetime.now().date()
        lunes = fecha - timedelta(days=fecha.weekday())
        sabado = lunes + timedelta(days=5)

        # Solo mostrar citas del doctor actual
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
        """, (lunes, sabado, self.id_doctor))
         #recorre las citas y las muestra en la tabla 
        for nombre, telefono, direccion, hora, fecha_cita, doctor, especialidad, motivo in cursor.fetchall():
            fecha_obj = fecha_cita if not isinstance(fecha_cita, str) else datetime.strptime(fecha_cita, "%Y-%m-%d").date()
            dia_semana = fecha_obj.weekday()
            if dia_semana > 5:
                continue
            col = dia_semana + 1
            # Convertir hora a formato "HH:MM"
            if isinstance(hora, str):
                hora_str = hora[:5]
            elif isinstance(hora, timedelta):
                segundos = int(hora.total_seconds())
                h = segundos // 3600
                m = (segundos % 3600) // 60
                hora_str = f"{h:02d}:{m:02d}"
            else:
                hora_str = hora.strftime("%H:%M")
            # Calcular fila basada en la hora
            inicio_hora = datetime.strptime("08:00", "%H:%M")
            hora_cita = datetime.strptime(hora_str, "%H:%M")
            diferencia_minutos = (hora_cita - inicio_hora).total_seconds() / 60
            fila = int(diferencia_minutos // 30) + 1

            celda = self.celdas.get((fila, col))
            if celda:
                # Mostrar solo el nombre del paciente en la celda
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
    #metodo que se ejecuta al hacer click en una celda de la tabla
    def _on_cell_click(self, r, c):
        data = self.detalles.get((r, c))
        if data:
            self._mostrar_detalles(data)
    #metodo para eliminar una cita
    def eliminar_cita(self, id_cita, top):
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar esta cita?"):
            db = conexionDB()
            cursor = db.cursor()
            cursor.execute("DELETE FROM cita WHERE id_cita = %s", (id_cita,))
            db.commit()
            cursor.close()
            db.close()
            messagebox.showinfo("Éxito", "Cita eliminada correctamente.")
            top.destroy()


        #metodo para mostrar los detalles de la cita en una ventana emergente
    def _mostrar_detalles(self, d):
        import os
        top = tk.Toplevel(self.root)
        top.title("Detalles de la Cita")
        w, h = 400, 650
        x = self.root.winfo_rootx() + (self.root.winfo_width() - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        top.resizable(False, False)
        top.grab_set()
        top.configure(bg=DETAIL_BG)
        # Frame principal
        frm = tk.Frame(top, bg=DETAIL_BG, padx=20, pady=20)
        frm.pack(fill='both', expand=True)
            # Título
        tk.Label(frm, text="DETALLES DEL PACIENTE", font=("Arial", 14, "bold"), bg=DETAIL_BG).pack(pady=(0, 15))
        # Conexión con base de datos para obtener detalles del paciente y cita
        db = conexionDB()
        cursor = db.cursor()
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
        # Mostrar detalles del paciente y cita en la ventana emergente
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

        tk.Frame(frm, height=2, bg="gray").pack(fill='x', pady=10)
        tk.Label(frm, text="INFORMACIÓN DE LA CITA", font=("Arial", 12, "bold"), bg=DETAIL_BG).pack(pady=(5, 10))
        #si se encuentra la cita, mostrar sus detalles
        if cita:
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

        def finalizar_cita():
            # Eliminar cita de la base de datos
            if cita:
                db = conexionDB()
                cursor = db.cursor()
                cursor.execute("DELETE FROM cita WHERE id_cita = %s", (cita[0],))
                db.commit()
                cursor.close()
                db.close()
                messagebox.showinfo("Éxito", "Cita finalizada y eliminada correctamente.")
                # Guardar paciente en TXT dentro de la carpeta citas_finalizadas
                fecha_txt = datetime.strptime(d["fecha"], "%d/%m/%Y").strftime("%Y-%m-%d")
                # Crear carpeta si no existe
                folder = "citas_finalizadas"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                filename = os.path.join(folder, f"atendidos_{fecha_txt}.txt")
                # Guardar detalles en el archivo
                info = [
                    f"ID Paciente: {paciente[0]}",
                    f"Nombre(s): {paciente[1]}",
                    f"Apellido paterno: {paciente[2]}",
                    f"Apellido materno: {paciente[3]}",
                    f"Dirección: {paciente[4]}",
                    f"Teléfono: {paciente[5]}",
                    f"NSS: {paciente[6]}",
                    f"Temperatura: {paciente[7]}",
                    f"Peso: {paciente[8]}",
                    f"Edad: {paciente[9]}",
                    f"Talla: {paciente[10]}",
                    f"ID Cita: {cita[0]}",
                    f"Fecha: {d['fecha']}",
                    f"Hora: {d['hora']}",
                    f"Motivo: {cita[1]}",
                    f"Doctor: {cita[2]} ({cita[3]})",
                    "-"*40
                ]
                # Append to the file
                with open(filename, "a", encoding="utf-8") as f:
                    f.write("\n".join(info) + "\n")
                top.destroy()
                self._cargar_citas()
        # Botones para finalizar o cerrar
        tk.Button(btns, text="Finalizar Cita", width=14, bg=EDIT_BTN_BG, fg="white", command=finalizar_cita).pack(side='left', padx=5)
        tk.Button(btns, text="Cerrar", width=10, bg=CLOSE_BTN_BG, fg="white", command=top.destroy).pack(side='left', padx=5)
    
        
        
    
    
if __name__ == "__main__":
    vistadoc(id_doctor=2)
