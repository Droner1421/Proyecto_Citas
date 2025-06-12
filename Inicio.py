import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import cv2
from ffpyplayer.player import MediaPlayer
from conexionDB import conexionDB
from ENF import ProximasCitasVentana

HEADER_BG = '#8FD3F4'
BUTTON_REG_BG = '#AAF0D1'
BUTTON_LOGIN_BG = '#5DADE2'
BUTTON_FG = '#000000'
CONTAINER_BG = '#FFFFFF'
FAQ_BG = '#FFFFFF'
FOOTER_BG = '#D3D3D3'
POPUP_BORDER = '#AAF0D1'
POPUP_BG = '#FFFFFF'


class Autentificacion:
    def __init__(self):

        self.conexion = conexionDB()

    def Login(self, Usuario, Contrasena, ventana):
        cursor = self.conexion.cursor()
        cursor.execute("Select * from usuarios where Usuarios = %s and contrasena = %s", (Usuario, Contrasena))
        if cursor.fetchone():
            messagebox.showinfo("Login exitoso", "Gracias por iniciar sesión")
            ventana.destroy()
            ProximasCitasVentana()

        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


    def Registro(self, nombre, Usuario, Contrasena, confirmcontrasena, TipoUsuario, Telefono, ventana):

        if not Usuario or not Contrasena or not nombre or not confirmcontrasena or not TipoUsuario or not Telefono:
            messagebox.showerror("Error", "Por favor, rellena todos los campos")
            return
        if Contrasena != confirmcontrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        cursor = self.conexion.cursor()
        cursor.execute ("Select * from usuarios where Usuarios = %s and contrasena = %s", (Usuario, Contrasena))
        if cursor.fetchone():
            messagebox.showerror("Error", "El usuario ya existe")
            return
        else:
            cursor.execute ("Insert into usuarios (Usuarios, Contrasena, Nombre, TipoUsuario, Telefono) values (%s, %s, %s, %s, %s)", (Usuario, Contrasena, nombre, TipoUsuario, Telefono))
            self.conexion.commit()
            messagebox.showinfo("Registro exitoso", "Gracias por registrarte")
            ventana.destroy()
        








 


class Video:
    def __init__(self, video_label, mute_button, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.media_player = MediaPlayer(video_path)
        self.video_label = video_label
        self.mute_button = mute_button
        self.audio_muted = False
        self.mute_button.config(command=self.mutear_audio)
        self.actualizar_frame()

    def actualizar_frame(self):
        ret, frame = self.cap.read()
        audio_frame, val = self.media_player.get_frame()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame).resize((400, 250), Image.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.video_label.after(30, self.actualizar_frame)
        else:
            self.cap.release()
            self.media_player.close_player()

    def mutear_audio(self):
        if not self.audio_muted:
            self.media_player.set_volume(0)
            self.audio_muted = True
            self.mute_button.config(text="Desmutear audio")
        else:
            self.media_player.set_volume(1)
            self.audio_muted = False
            self.mute_button.config(text="Mutear audio")



class vistaapp:

    def __init__(self):
        self.aut = Autentificacion()
        self.vista_inicio()
        self.video_frames = []
        self.audio_muted = False
        
        
        pass


    def vista_inicio(self):
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Salud")
        self.ventana.geometry('800x600')
        self.ventana.configure(bg='white')
        header_font = font.Font(family="Helvetica", size=16, weight="bold")
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        subtitle_font = font.Font(family="Helvetica", size=14, weight="bold")
        faq_font = font.Font(family="Helvetica", size=12)

        header = tk.Frame(self.ventana, bg=HEADER_BG, height=50)
        header.pack(fill='x')
        logo = tk.Canvas(header, width=40, height=40, bg='white', highlightthickness=1)
        logo.create_oval(5, 5, 35, 35)
        logo.pack(side='left', padx=10, pady=5)
        tk.Label(header, text="Nombre institucion", bg=HEADER_BG, fg='black', font=header_font).pack(side='left', padx=20)
        login_top = tk.Label(header, text="Inicio de sesión", bg=HEADER_BG, fg='black', font=faq_font, cursor="hand2")
        login_top.pack(side='right', padx=20)
        login_top.bind("<Button-1>", lambda e: self.abrir_login())  # solo llamada a otra vista o controlador

        # Cuerpo principal
        main_frame = tk.Frame(self.ventana, bg='white')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Panel izquierdo
        left_frame = tk.Frame(main_frame, bg=CONTAINER_BG, bd=1, relief='solid')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        tk.Label(left_frame, text="BIENVENIDO AL", font=title_font, bg=CONTAINER_BG).pack(pady=(20, 0))
        tk.Label(left_frame, text="SISTEMA", font=font.Font(family="Helvetica", size=32, weight="bold"), fg=HEADER_BG, bg=CONTAINER_BG).pack(pady=(0, 10))
        tk.Label(left_frame, text="LEYENDA SOBRE SALUD", font=subtitle_font, bg=CONTAINER_BG).pack(pady=(0, 20))

        tk.Button(left_frame, text="Registrarse", bg=BUTTON_REG_BG, fg=BUTTON_FG, command=self.Registro_vista).pack(side='left', padx=(50, 10), pady=20)
        tk.Button(left_frame, text="Iniciar sesión", bg=BUTTON_LOGIN_BG, fg=BUTTON_FG, command=self.login_vista).pack(side='left', padx=10, pady=20)

        # Panel derecho
        right_frame = tk.Frame(main_frame, bg=CONTAINER_BG, bd=1, relief='solid')
        right_frame.pack(side='left', fill='both', expand=True, padx=(5, 0))
        tk.Label(right_frame, text="Video de introducción", font=subtitle_font, bg=CONTAINER_BG).pack(pady=(20, 10))

        self.video_label = tk.Label(right_frame, bg='black')
        self.video_label.pack(pady=10)

        self.mute_button = tk.Button(
            right_frame,
            text="Mutear audio",
            bg="#FFD700",
            fg="black"
        )
        self.mute_button.pack(pady=5)

        # video
        self.video = Video(
            self.video_label,
            self.mute_button,
            r"C:\Users\Gabriel\Documents\python\proyecto\Consulta en el médico para niños - Tipos de médicos - Estudios sociales _ Kids Academy.mp4"
        )

        
        



  
        faq_frame = tk.Frame(self.ventana, bg=FAQ_BG)
        faq_frame.pack(fill='x', padx=10)
        tk.Label(faq_frame, text="Preguntas Frecuentes", font=subtitle_font, bg=FAQ_BG).grid(row=0, column=0, sticky='w', pady=(10, 5))
        faqs = ["¿Cómo me registro?", "¿Cómo reprogramo mi cita?", "¿Qué documentos necesito?"]
        for i, text in enumerate(faqs, start=1):
            tk.Label(faq_frame, text=f"\u25CA {text}", font=faq_font, bg=FAQ_BG).grid(row=(i // 2) + 1, column=(i - 1) % 2, sticky='w', padx=20, pady=2)


        footer = tk.Frame(self.ventana, bg=FOOTER_BG, height=30)
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="Pie de pagina", bg=FOOTER_BG, fg='black', font=subtitle_font).pack(pady=5)

     
        self.ventana.mainloop()



    def login_vista(self):
        self.login = tk.Toplevel()
        self.login.title = "Login"
        self.login.geometry('400x400')
        self.login.configure(bg=POPUP_BORDER)

        title_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        label_font = font.Font(family="Helvetica", size=12)
        inner = tk.Frame(self.login, bg=POPUP_BG, bd=2, relief='solid')
        inner.place(relx=0.5, rely=0.5, anchor='center', width=360, height=350)
        tk.Label(inner, text="Inicio de sesión", font=title_font, bg=POPUP_BG).pack(pady=(20,10))


        # Campo usuario
        self.entry_user = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", lambda e: self.entry_user.delete(0, tk.END) if self.entry_user.get() == "Usuario" else None)
        self.entry_user.pack(pady=(0,10), ipadx=50, ipady=5)

        # Campo contraseña
        self.entry_pass = tk.Entry(inner, font=label_font, bg=POPUP_BG, show="")
        self.entry_pass.insert(0, "Contraseña")
        def limpiar_pass(event):
            if self.entry_pass.get() == "Contraseña":
                self.entry_pass.delete(0, tk.END)
                self.entry_pass.config(show="*")
        self.entry_pass.bind("<FocusIn>", limpiar_pass)
        self.entry_pass.pack(pady=(0,5), ipadx=50, ipady=5)

        tk.Label(inner, text="olvidaste contraseña", font=label_font, bg=POPUP_BG, cursor="hand2").pack(anchor='e', padx=20)
        tk.Button(inner, text="Iniciar sesión", bg=BUTTON_REG_BG, fg=BUTTON_FG, font=label_font, bd=0, relief='ridge',command= lambda: self.aut.Login(self.entry_user.get(), self.entry_pass.get(), self.login)).pack(pady=20, ipadx=20, ipady=5)
        footer_text = tk.Label(inner, text="¿Aun no tienes cuenta? registrate", font=label_font, bg=POPUP_BG, cursor="hand2")
        footer_text.pack(pady=(10,0))
    


 


    def Registro_vista(self):
        self.Registro = tk.Toplevel()
        self.Registro.title = "Registro"
        self.Registro.geometry('400x450')
        self.Registro.configure(bg=POPUP_BORDER)

        title_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        label_font = font.Font(family="Helvetica", size=12)
        inner = tk.Frame(self.Registro, bg=POPUP_BG, bd=2, relief='solid')
        inner.place(relx=0.5, rely=0.5, anchor='center', width=360, height=450) 
        tk.Label(inner, text="Inicio de sesión", font=title_font, bg=POPUP_BG).pack(pady=(20,10))

        # Campo nombre completo
        self.entry_nombre = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_nombre.insert(0, "Nombre completo")
        self.entry_nombre.bind("<FocusIn>", lambda e: self.entry_nombre.delete(0, tk.END) if self.entry_nombre.get() == "Nombre completo" else None)
        self.entry_nombre.pack(pady=(0,10), ipadx=50, ipady=5)

        #Telefono
        self.entry_telefono = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_telefono.insert(0, "Telefono")
        self.entry_telefono.bind("<FocusIn>", lambda e: self.entry_telefono.delete(0, tk.END) if self.entry_telefono.get() == "Telefono" else None)
        self.entry_telefono.pack(pady=(0,10), ipadx=50, ipady=5)




        # Campo usuario
        self.entry_user = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", lambda e: self.entry_user.delete(0, tk.END) if self.entry_user.get() == "Usuario" else None)
        self.entry_user.pack(pady=(0,10), ipadx=50, ipady=5)

        # Campo contraseña
        self.entry_pass = tk.Entry(inner, font=label_font, bg=POPUP_BG, show="")
        self.entry_pass.insert(0, "Contraseña")
        def limpiar_pass(event):
            if self.entry_pass.get() == "Contraseña":
                self.entry_pass.delete(0, tk.END)
                self.entry_pass.config(show="*")
        self.entry_pass.bind("<FocusIn>", limpiar_pass)
        self.entry_pass.pack(pady=(0,5), ipadx=50, ipady=5)

        #confirmar contraseña
        self.entry_pass2 = tk.Entry(inner, font=label_font, bg=POPUP_BG, show="")
        self.entry_pass2.insert(0, "Confirmar contraseña")
        def limpiar_pass2(event):
            if self.entry_pass2.get() == "Confirmar contraseña":
                self.entry_pass2.delete(0, tk.END)
                self.entry_pass2.config(show="*")
        self.entry_pass2.bind("<FocusIn>", limpiar_pass2)
        self.entry_pass2.pack(pady=(0,5), ipadx=50, ipady=5)

        # Radio buttons para tipo de usuario
        self.tipo_usuario = tk.StringVar(value="medico")
        radio_frame = tk.Frame(inner, bg=POPUP_BG)
        tk.Label(radio_frame, text="Tipo de usuario:", font=label_font, bg=POPUP_BG).pack(side='left')
        tk.Radiobutton(radio_frame, text="Médico", variable=self.tipo_usuario, value="medico", bg=POPUP_BG, font=label_font).pack(side='left', padx=10)
        tk.Radiobutton(radio_frame, text="Recepcionista", variable=self.tipo_usuario, value="recepcionista", bg=POPUP_BG, font=label_font).pack(side='left', padx=10)
        radio_frame.pack(pady=(0,10))

        tk.Label(inner, text="olvidaste contraseña", font=label_font, bg=POPUP_BG, cursor="hand2").pack(anchor='e', padx=20)
        tk.Button(inner, text="Registrarse", bg=BUTTON_REG_BG, fg=BUTTON_FG, font=label_font, bd=0, relief='ridge',command=lambda: self.aut.Registro(self.entry_nombre.get(), self.entry_user.get(), self.entry_pass.get(), self.entry_pass2.get(), self.tipo_usuario.get(), self.entry_telefono.get(), self.Registro)).pack(pady=20, ipadx=20, ipady=5)




    




def main():
   app = vistaapp()


if __name__ == "__main__":
    main()





        