import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import cv2
from ffpyplayer.player import MediaPlayer
from conexionDB import conexionDB
from ENF import ProximasCitasVentana
from DOC import vistadoc
import re

HEADER_BG = '#8FD3F4'
BUTTON_REG_BG = '#AAF0D1'
BUTTON_LOGIN_BG = '#5DADE2'
BUTTON_FG = '#000000'
CONTAINER_BG = '#FFFFFF'
FAQ_BG = '#FFFFFF'
FOOTER_BG = '#D3D3D3'
POPUP_BORDER = '#AAF0D1'
POPUP_BG = '#FFFFFF'

# Conexion a la base de datos
class Autentificacion:
    def __init__(self):
        self.conexion = conexionDB()

    #Login y saber si es doctor o recepcionista
    def Login(self, Usuario, Contrasena, ventana_login, ventana_principal, destroy_video):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT id, tipo_usuario FROM personal WHERE usuario = %s AND contrasena = %s", (Usuario, Contrasena))
        result = cursor.fetchone()
        if result:
            id_usuario, tipo_usuario = result
            #comprobar si el usuario es medico o recepcionista
            if tipo_usuario == "medico":
                messagebox.showinfo("Login exitoso", "Gracias por iniciar sesión como médico")
                destroy_video()
                ventana_login.destroy()
                ventana_principal.destroy()
                # Mandar id del usuario a la vista de médico
                vistadoc(id_usuario)
            else:
                messagebox.showinfo("Login exitoso", "Gracias por iniciar sesión como recepcionista")
                destroy_video()
                ventana_login.destroy()
                ventana_principal.destroy()
                ProximasCitasVentana(id_usuario)
        else:
            #mensaje de error si el usuario o contraseña son incorrectos
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Método para registrar un nuevo usuario en la base de datos
    def Registro(self, nombre, Usuario, Contrasena, confirmcontrasena, TipoUsuario, Telefono, apellido_materno, apellido_paterno, ventana):
        # Verifica que todos los campos estén llenos
        if not Usuario or not Contrasena or not nombre or not confirmcontrasena or not TipoUsuario or not Telefono or not apellido_paterno or not apellido_materno:
            messagebox.showerror("Error", "Por favor, rellena todos los campos")
            return
        # Verifica que las contraseñas coincidan
        if Contrasena != confirmcontrasena:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        cursor = self.conexion.cursor()
        # Verifica si el usuario ya existe en la base de datos
        cursor.execute("Select * from personal where usuario = %s", (Usuario,))
        if cursor.fetchone():
            messagebox.showerror("Error", "El usuario ya existe")
            return
        else:
            # Inserta el nuevo usuario en la base de datos
            cursor.execute(
                "Insert into personal (usuario, contrasena, nombre, apellido_paterno, apellido_materno, tipo_usuario, telefono) values (%s, %s, %s, %s, %s, %s, %s)",
                (Usuario, Contrasena, nombre, apellido_paterno, apellido_materno, TipoUsuario, Telefono)
            )
            self.conexion.commit()
            messagebox.showinfo("Registro exitoso", "Gracias por registrarte")
            ventana.destroy()









 

# Video y audio de la aplicación
class Video:
    def __init__(self, video_label, mute_button, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.media_player = MediaPlayer(video_path)
        self.video_label = video_label
        self.mute_button = mute_button
        self.audio_muted = False
        self.mute_button.config(command=self.mutear_audio)
        self.actualizar_frame()
     #actuliza los frames del video
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
            self.detener()
  

    
    def mutear_audio(self):
        if not self.audio_muted:
            # Si el audio no está muteado, lo silencia
            self.media_player.set_volume(0)
            self.audio_muted = True
            self.mute_button.config(text="Desmutear audio")
        else:
            # Si el audio está muteado, lo activa
            self.media_player.set_volume(1)
            self.audio_muted = False
            self.mute_button.config(text="Mutear audio")

    def detener(self):
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        if hasattr(self, 'media_player') and self.media_player:
            self.media_player.close_player()
        if hasattr(self, 'video_label') and self.video_label:
            if hasattr(self, 'after_id'):
                self.video_label.after_cancel(self.after_id)


# class vistaapp
class vistaapp:

    def __init__(self):
        self.aut = Autentificacion()
        self.vista_inicio()
        self.video_frames = []
        self.audio_muted = False
        
        
        pass

    def destruir_video(self):
        #verificar si self tiene un atributo llamado video
        if hasattr(self, 'video'):
            # si existe llama al método detener
            self.video.detener()


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
        # Logo
        logo_image = Image.open("logo.jpg")  
        logo_image = logo_image.resize((50, 50), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(header, image=logo, bg=HEADER_BG)
        logo_label.image = logo 
        logo_label.pack(side='left', padx=10)
        tk.Label(header, text="Casa de salud La Huanica", bg=HEADER_BG, fg='black', font=header_font).pack(side='left', padx=20)
        login_top = tk.Label(header, text="Inicio de sesión", bg=HEADER_BG, fg='black', font=faq_font, cursor="hand2")
        login_top.pack(side='right', padx=20)
        login_top.bind("<Button-1>", lambda e: self.login_vista())  

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

        # crear un botón para iniciar sesión en el panel izquierdo se le asigna un nombre y la funcion de abrir la ventana de login
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
            r"Consulta en el médico para niños - Tipos de médicos - Estudios sociales _ Kids Academy.mp4"
        )

        
        



  
        faq_frame = tk.Frame(self.ventana, bg=FAQ_BG)
        faq_frame.pack(fill='x', padx=10)
        tk.Label(faq_frame, text="Preguntas Frecuentes", font=subtitle_font, bg=FAQ_BG).grid(row=0, column=0, sticky='w', pady=(10, 5))
        faqs = ["¿Cómo me registro?", "¿Cómo reprogramo mi cita?", "¿Qué documentos necesito?"]
        for i, text in enumerate(faqs, start=1):
            tk.Label(faq_frame, text=f"\u25CA {text}", font=faq_font, bg=FAQ_BG).grid(row=(i // 2) + 1, column=(i - 1) % 2, sticky='w', padx=20, pady=2)


        footer = tk.Frame(self.ventana, bg=FOOTER_BG, height=30)
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="", bg=FOOTER_BG, fg='black', font=subtitle_font).pack(pady=5)

     
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
        # Crea un campo de entrada
        self.entry_user = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        # Inserta el texto Usuario como texto por defecto
        self.entry_user.insert(0, "Usuario")
        # Elimina el texto al hacer clic en el campo
        self.entry_user.bind("<FocusIn>", lambda e: self.entry_user.delete(0, tk.END) if self.entry_user.get() == "Usuario" else None)
        # definir tamaño del campo
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

        forgot_label = tk.Label(inner, text="olvidaste contraseña", font=label_font, bg=POPUP_BG, cursor="hand2")
        forgot_label.pack(anchor='e', padx=20)
        forgot_label.bind("<Button-1>", lambda e: messagebox.showinfo("Recuperar contraseña", "Por favor, contacta al desarrollador para recuperar tu contraseña."))
        tk.Button(inner, text="Iniciar sesión", bg=BUTTON_REG_BG, fg=BUTTON_FG, font=label_font, bd=0, relief='ridge', command=lambda: self.aut.Login(self.entry_user.get(), self.entry_pass.get(), self.login, self.ventana, self.destruir_video)).pack(pady=20, ipadx=20, ipady=5)
        footer_text = tk.Label(inner, text="¿Aun no tienes cuenta? registrate", font=label_font, bg=POPUP_BG, cursor="hand2")
        footer_text.pack(pady=(10,0))
        #abrir registro y cerrar login
        footer_text.bind("<Button-1>", lambda e: (self.Registro_vista(), self.login.destroy()))
        




       


 


    def Registro_vista(self):
        self.Registro = tk.Toplevel()
        self.Registro.title = "Registro"
        self.Registro.geometry('400x550')
        self.Registro.configure(bg=POPUP_BORDER)

        title_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        label_font = font.Font(family="Helvetica", size=12)
        inner = tk.Frame(self.Registro, bg=POPUP_BG, bd=2, relief='solid')
        inner.place(relx=0.5, rely=0.5, anchor='center', width=360, height=500) 
        tk.Label(inner, text="Registro", font=title_font, bg=POPUP_BG).pack(pady=(20,10))

        # Campo nombre 
        # Crea un campo de entrada
        self.entry_nombre = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        # Inserta el texto
        self.entry_nombre.insert(0, "Nombre(s)")
        # Elimina el texto al hacer clic en el campo
        self.entry_nombre.bind("<FocusIn>", lambda e: self.entry_nombre.delete(0, tk.END) if self.entry_nombre.get() == "Nombre(s)" else None)
        # define el padding y el tamaño del campo
        self.entry_nombre.pack(pady=(0,10), ipadx=50, ipady=5)
              
                # Campo apellido_paterno
        self.entry_apeellido_paterno = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_apeellido_paterno.insert(0, "Apellido paterno")
        self.entry_apeellido_paterno.bind("<FocusIn>", lambda e: self.entry_apeellido_paterno.delete(0, tk.END) if self.entry_apeellido_paterno.get() == "Apellido paterno" else None)
        self.entry_apeellido_paterno.pack(pady=(0,10), ipadx=50, ipady=5)


         # Campo apellido_materno
        self.entry_apeellido_materno = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_apeellido_materno.insert(0, "Apellido materno")
        self.entry_apeellido_materno.bind("<FocusIn>", lambda e: self.entry_apeellido_materno.delete(0, tk.END) if self.entry_apeellido_materno.get() == "Apellido materno" else None)
        self.entry_apeellido_materno.pack(pady=(0,10), ipadx=50, ipady=5)

        #Telefono
        self.entry_telefono = tk.Entry(inner, font=label_font, bg=POPUP_BG)
        self.entry_telefono.insert(0, "Telefono")
        # limipiar el campo de telefono a solo numeros con un limite de 10 numeros al sobrepasar el valor este elimina el numero que se ingreso
        def limpiar_telefono(event):
            if self.entry_telefono.get() == "Telefono":
                self.entry_telefono.delete(0, tk.END)
            elif not self.entry_telefono.get().isdigit() or len(self.entry_telefono.get()) > 10:
                self.entry_telefono.delete(len(self.entry_telefono.get())-1, tk.END)
        self.entry_telefono.bind("<FocusIn>", limpiar_telefono)
        self.entry_telefono.bind("<KeyRelease>", limpiar_telefono)
        
        # Elimina el texto al hacer clic en el campo
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

        forgot_label = tk.Label(inner, text="olvidaste contraseña", font=label_font, bg=POPUP_BG, cursor="hand2")
        forgot_label.pack(anchor='e', padx=20)
        forgot_label.bind("<Button-1>", lambda e: messagebox.showinfo("Recuperar contraseña", "Por favor, contacta al desarrollador para recuperar tu contraseña."))

        def validar_datos():
            nombre = self.entry_nombre.get().strip()
            usuario = self.entry_user.get().strip()
            contrasena = self.entry_pass.get().strip()
            confirm_contrasena = self.entry_pass2.get().strip()
            telefono = self.entry_telefono.get().strip()
            apellido_paterno = self.entry_apeellido_paterno.get().strip()
            apellido_materno = self.entry_apeellido_materno.get().strip()
            

            campos = [nombre, usuario, contrasena, confirm_contrasena, telefono, apellido_paterno, apellido_materno]
            valores_por_defecto = ["Nombre(s)", "Usuario", "Contraseña", "Confirmar contraseña", "Telefono", "Apellido paterno", "Apellido materno"]
            if any (c == "" or c in valores_por_defecto for c in campos):
                messagebox.showerror("Error", "Por favor, rellena todos los campos")
                return False
            
            patron_nombre = r"^[a-zA-Z\s]+$"
            if not re.match(patron_nombre, nombre):
                messagebox.showerror("Error", "El nombre solo debe contener letras y espacios")
                return
            if not re.match(patron_nombre, apellido_paterno):
                messagebox.showerror("Error", "El apellido paterno solo debe contener letras y espacios")
                return
            if not re.match(patron_nombre, apellido_materno):
                messagebox.showerror("Error", "El apellido materno solo debe contener letras y espacios")
                return
            if not telefono.isdigit() or len(telefono) != 10:
                messagebox.showerror("Error", "El teléfono debe ser un número de 10 dígitos")
                return
            if len(contrasena) < 8:
                messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres")
                return
            if  not re.search(r"[A-Z]", contrasena) or not re.search(r"[a-z]", contrasena) or not re.search(r"[0-9]", contrasena):
                messagebox.showerror("Error", "La contraseña debe contener al menos una letra mayúscula, una minúscula y un número")
                return
            if not re.search(r"[@$!%*?&]", contrasena):
                messagebox.showerror("Error", "La contraseña debe contener al menos un carácter especial (@, $, !, %, *, ?, &)")
                return
            if not  re.search(r"\d", contrasena):
                messagebox.showerror("Error", "La contraseña debe contener al menos un número")
                return
            
            if contrasena != confirm_contrasena:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            # en nombre apellido paterno y materno debe tener almenos 2 3 caracteres
            if len(nombre) < 3 or len(apellido_paterno) < 3 or len(apellido_materno) < 3:
                messagebox.showerror("Error", "Ingresa un nombre o apellidos válidos")
                return
            # el usuario deve tener almenos 5 caracteres
            if len(usuario) < 5:
                messagebox.showerror("Error", "El usuario debe tener al menos 5 caracteres")
                return
            
            self.aut.Registro(
                nombre,
                usuario,
                contrasena,
                confirm_contrasena,
                self.tipo_usuario.get(),
                telefono,
                apellido_materno,
                apellido_paterno,
                self.Registro
            )
            


        tk.Button(inner, text="Registrarse", bg=BUTTON_REG_BG, fg=BUTTON_FG, font=label_font, bd=0, relief='ridge', command=validar_datos).pack(pady=20, ipadx=20, ipady=5)




    




def main():
   app = vistaapp()

if __name__ == "__main__":
   main()






        