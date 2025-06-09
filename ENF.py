import tkinter as tk
from tkinter import messagebox, ttk
from conexionDB import conexionDB
from Regis_Pas import RegistroCitaVentana
from Dashboard_2 import grafica  

class ProximasCitasVentana:
    def __init__(self):
        self.crear_interfaz()

    def crear_interfaz(self):
        self.ventana = tk.Tk()
        self.ventana.title("Próximas Citas")
        self.ventana.geometry("1100x600")
        self.ventana.configure(bg='white')

        header = tk.Frame(self.ventana, bg='#8FD3F4', height=60, bd=2, relief='groove')
        header.pack(fill='x', side='top')

        logo = tk.Canvas(header, width=40, height=40, bg='white', highlightthickness=1)
        logo.create_oval(5, 5, 35, 35)
        logo.create_text(20, 20, text="L", font=("Arial", 14, "bold"))
        logo.pack(side='left', padx=10, pady=10)

        tk.Label(header, text="Logotipo", bg='#8FD3F4', fg='black', font=("Arial", 14, "bold")).pack(side='left')
        tk.Label(header, text="Nombre institución", bg='#8FD3F4', fg='black', font=("Arial", 16, "bold")).pack(side='right', padx=20)

        topbar = tk.Frame(self.ventana, bg='#F5F5F5', height=40, bd=1, relief='groove')
        topbar.pack(fill='x')

        op_btn = tk.Menubutton(topbar, text="Operaciones", bg='#AAF0D1', fg='#000000', font=("Arial", 10, "bold"), relief='raised')
        op_menu = tk.Menu(op_btn, tearoff=0)
        op_menu.add_command(label="Nueva Cita", command=lambda: RegistroCitaVentana(self.ventana, on_close=self.cargar_citas))
        op_menu.add_command(label="Buscar Cita", command=lambda: messagebox.showinfo("Buscar Cita", "Funcionalidad no implementada"))
        op_menu.add_command(label="Dashboard", command=lambda: grafica())
      
        op_btn.config(menu=op_menu)
        op_btn.pack(side='left', padx=15, pady=5)

        tk.Button(topbar, text="Cerrar Sesión", bg='#FF6347', fg='white', font=("Arial", 10, "bold"), command=self.ventana.destroy).pack(side='right', padx=10, pady=5)

        main_frame = tk.Frame(self.ventana, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        tk.Label(main_frame, text="¡PRÓXIMAS CITAS!", font=("Arial", 18, "bold"), fg="#1DA1F2", bg='white').pack(pady=(0, 10))

        columns = (
            "Nombre", "Apellido", "Teléfono", "NSS", "Peso", "Altura", "Temperatura", "Fecha", "Hora"
        )
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill='both', expand=True)

        self.tree.bind("<Double-1>", self.ver_detalle_cita)

        self.cargar_citas()

        footer = tk.Frame(self.ventana, bg='#F5F5F5', height=40, bd=1, relief='groove')
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="Pie de página", bg='#F5F5F5', fg='black', font=("Arial", 14, "bold")).pack(pady=5)

        self.ventana.mainloop()

    def cargar_citas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = conexionDB()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT Nombre_paciente, Apellido_paciente, telefono_paciente, NSS_paciente,
                       Peso_paciente, Altura_paciente, temperatura_paciente,
                       fecha_cita, hora_cita
                FROM citas
                ORDER BY fecha_cita, hora_cita
            """)
            for row in cursor.fetchall():
                nombre, apellido, telefono, nss, peso, altura, temperatura, fecha, hora = row
                fecha_str = fecha.strftime("%d/%m/%Y")
                if hasattr(hora, 'strftime'):
                    hora_str = hora.strftime("%H:%M")
                elif hasattr(hora, 'seconds'):
                    total_seconds = int(hora.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    hora_str = f"{hours:02d}:{minutes:02d}"
                else:
                    hora_str = str(hora)
                values = (nombre, apellido, telefono, nss, f"{peso} kg", f"{altura} m", f"{temperatura} °C", fecha_str, hora_str)
                self.tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error al cargar citas", str(e))
        finally:
            cursor.close()
            conn.close()

    def ver_detalle_cita(self, event):
        item = self.tree.focus()
        if not item:
            return
        values = self.tree.item(item, "values")
        mensaje = (
            f"Nombre: {values[0]} {values[1]}\n"
            f"Teléfono: {values[2]}\n"
            f"NSS: {values[3]}\n"
            f"Peso: {values[4]}\n"
            f"Altura: {values[5]}\n"
            f"Temperatura: {values[6]}\n"
            f"Fecha: {values[7]}\n"
            f"Hora: {values[8]}"
        )
        messagebox.showinfo("Detalle de la cita", mensaje)
if __name__ == "__main__":
    ProximasCitasVentana()