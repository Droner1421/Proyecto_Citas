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

class Login:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.win = tk.Toplevel(parent)
        self.win.title("Inicio de sesión")
        self.win.geometry('400x350')
        self.win.configure(bg=POPUP_BORDER)
        self.Login_vista()

    def Login_vista(self):
        title_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        label_font = font.Font(family="Helvetica", size=12)
        inner = tk.Frame(self.win, bg=POPUP_BG, bd=2, relief='solid')
        inner.place(relx=0.5, rely=0.5, anchor='center', width=360, height=310)
        tk.Label(inner, text="Inicio de sesión", font=title_font, bg=POPUP_BG).pack(pady=(20,10))
        self.entry_user = tk.Entry(inner, font=label_font)
        self.entry_user.insert(0, "nombre usuario")
        self.entry_user.bind("<FocusIn>", lambda e: self.entry_user.delete(0, tk.END))
        self.entry_user.pack(pady=(0,10), ipadx=50, ipady=5)
        self.entry_pass = tk.Entry(inner, font=label_font)
        self.entry_pass.insert(0, "Contraseña")
        self.entry_pass.bind("<FocusIn>", self.Limpiar_password)
        self.entry_pass.pack(pady=(0,5), ipadx=50, ipady=5)
        tk.Label(inner, text="olvidaste contraseña", font=label_font, bg=POPUP_BG, cursor="hand2").pack(anchor='e', padx=20)
        tk.Button(inner, text="Iniciar sesión", bg=BUTTON_REG_BG, fg=BUTTON_FG, font=label_font, bd=0, relief='ridge', command=self.Login_PeticionDB).pack(pady=20, ipadx=20, ipady=5)
        footer_text = tk.Label(inner, text="¿Aun no tienes cuenta? registrate", font=label_font, bg=POPUP_BG, cursor="hand2")
        footer_text.pack(pady=(10,0))
        footer_text.bind("<Button-1>", lambda e: Registro(self.parent, self.on_success))

    def Limpiar_password(self, e):
        self.entry_pass.delete(0, tk.END)
        self.entry_pass.config(show='*')

    def Login_PeticionDB(self):
        usuario = self.entry_user.get()
        contrasena = self.entry_pass.get()
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE usuario=%s AND contrasena=%s", (usuario, contrasena))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Éxito", "Inicio de sesión correcto")
            self.win.destroy()
            self.parent.destroy()
            ProximasCitasVentana()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        cursor.close()
        conn.close()

class Registro:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.win = tk.Toplevel(parent)
        self.win.title("Registro")
        self.win.geometry('400x350')
        self.win.configure(bg=POPUP_BORDER)
        self.Login_vista()

    def Login_vista(self):
        title_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        label_font = font.Font(family="Helvetica", size=12)
        inner = tk.Frame(self.win, bg=POPUP_BG, bd=2, relief='solid')
        inner.place(relx=0.5, rely=0.5, anchor='center', width=360, height=310)
        tk.Label(inner, text="Registro", font=title_font, bg=POPUP_BG).pack(pady=(20,10))
        self.entry_user = tk.Entry(inner, font=label_font)
        self.entry_user.insert(0, "nombre usuario")
        self.entry_user.bind("<FocusIn>", lambda e: self.entry_user.delete(0, tk.END))
        self.entry_user.pack(pady=(0,10), ipadx=50, ipady=5)
        self.entry_pass = tk.Entry(inner, font=label_font)
        self.entry_pass.insert(0, "Contraseña")
        self.entry_pass.bind("<FocusIn>", self.Limpiar_password)
        self.entry_pass.pack(pady=(0,10), ipadx=50, ipady=5)
        self.entry_confirm = tk.Entry(inner, font=label_font)
        self.entry_confirm.insert(0, "Confirmar contraseña")
        self.entry_confirm.bind("<FocusIn>", self.Limpiar_Confirmacion)
        self.entry_confirm.pack(pady=(0,10), ipadx=50, ipady=5)
        tk.Button(inner, text="Registrarse", bg=BUTTON_REG_BG, fg=BUTTON_FG, font=label_font, bd=0, relief='ridge', command=self.register_action).pack(pady=20, ipadx=20, ipady=5)
        login_text = tk.Label(inner, text="¿Ya tienes cuenta? Iniciar sesión", font=label_font, bg=POPUP_BG, cursor="hand2")
        login_text.pack(pady=(10,0))
        login_text.bind("<Button-1>", lambda e: Login(self.parent, self.on_success))

    def Limpiar_password(self, e):
        self.entry_pass.delete(0, tk.END)
        self.entry_pass.config(show='*')

    def Limpiar_Confirmacion(self, e):
        self.entry_confirm.delete(0, tk.END)
        self.entry_confirm.config(show='*')

    def register_action(self):
        usuario = self.entry_user.get()
        contrasena = self.entry_pass.get()
        confirmar = self.entry_confirm.get()
        if not usuario or not contrasena or not confirmar or usuario == "nombre usuario" or contrasena == "Contraseña" or confirmar == "Confirmar contraseña":
            messagebox.showerror("Error", "Completa todos los campos")
            return
        if contrasena != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        conn = conexionDB()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login WHERE usuario=%s", (usuario,))
        if cursor.fetchone():
            messagebox.showerror("Error", "El usuario ya existe")
        else:
            cursor.execute("INSERT INTO login (usuario, contrasena) VALUES (%s, %s)", (usuario, contrasena))
            conn.commit()
            messagebox.showinfo("Éxito", "Registro exitoso")
            self.win.destroy()
        cursor.close()
        conn.close()

class video:
    def __init__(self):
        self.cap = None
        self.player = None
        self.video_label = None
        self.video_iniciarning = True
        self.audio_muted = False

    def Audio(self, video_path):
        return MediaPlayer(video_path)

    def Frames(self):
        if not self.video_iniciarning:
            return
        ret, frame = self.cap.read()
        audio_frame, val = self.player.get_frame()
        if ret:
            frame = cv2.resize(frame, (400, 225))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        if val != 'eof' and self.video_iniciarning:
            self.video_label.after_id = self.video_label.after(15, self.Frames)
        else:
            if self.cap is not None:
                self.cap.release()

    def detener_video(self):
        self.video_iniciarning = False
        if self.cap is not None:
            self.cap.release()
        if self.player is not None:
            self.player.set_volume(0)
        try:
            if self.video_label is not None and self.video_label.winfo_exists():
                after_id = getattr(self.video_label, "after_id", None)
                if after_id is not None:
                    self.video_label.after_cancel(after_id)
                self.video_label.config(image='')
        except tk.TclError:
            pass

    def mutear_audio(self):
        if self.player is not None:
            if not self.audio_muted:
                self.player.set_volume(0)
                self.audio_muted = True
            else:
                self.player.set_volume(100)
                self.audio_muted = False

    def ventana_login(self):
        Login(self.ventana, ProximasCitasVentana)

    def ventana_register(self):
        Registro(self.ventana, ProximasCitasVentana)

    def iniciar(self):
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
        logo.create_oval(5,5,35,35)
        logo.pack(side='left', padx=10, pady=5)
        tk.Label(header, text="Nombre institucion", bg=HEADER_BG, fg='black', font=header_font).pack(side='left', padx=20)
        login_top = tk.Label(header, text="Inicio de sesión", bg=HEADER_BG, fg='black', font=faq_font, cursor="hand2")
        login_top.pack(side='right', padx=20)
        login_top.bind("<Button-1>", lambda e: self.ventana_login())

        main_frame = tk.Frame(self.ventana, bg='white')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        left_frame = tk.Frame(main_frame, bg=CONTAINER_BG, bd=1, relief='solid')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0,5))
        tk.Label(left_frame, text="BIENVENIDO AL", font=title_font, bg=CONTAINER_BG).pack(pady=(20,0))
        tk.Label(left_frame, text="SISTEMA", font=font.Font(family="Helvetica", size=32, weight="bold"), fg=HEADER_BG, bg=CONTAINER_BG).pack(pady=(0,10))
        tk.Label(left_frame, text="LEYENDA SOBRE SALUD", font=subtitle_font, bg=CONTAINER_BG).pack(pady=(0,20))
        btn_reg = tk.Button(left_frame, text="Registrarse", bg=BUTTON_REG_BG, fg=BUTTON_FG, command=self.ventana_register)
        btn_reg.pack(side='left', padx=(50,10), pady=20)
        btn_open = tk.Button(left_frame, text="Iniciar sesión", bg=BUTTON_LOGIN_BG, fg=BUTTON_FG, command=self.ventana_login)
        btn_open.pack(side='left', padx=10, pady=20)

        right_frame = tk.Frame(main_frame, bg=CONTAINER_BG, bd=1, relief='solid')
        right_frame.pack(side='left', fill='both', expand=True, padx=(5,0))
        tk.Label(right_frame, text="Video de introducción", font=subtitle_font, bg=CONTAINER_BG).pack(pady=(20,10))

        self.video_label = tk.Label(right_frame, bg='black')
        self.video_label.pack(pady=10)
        btn_mute = tk.Button(right_frame, text="Mutear/Desmutear", bg="#FFD700", fg="black", command=self.mutear_audio)
        btn_mute.pack(pady=5)

        video_path = r"C:\Users\Gabriel\Documents\python\proyecto\Consulta en el médico para niños - Tipos de médicos - Estudios sociales _ Kids Academy.mp4"
        self.cap = cv2.VideoCapture(video_path)
        self.player = self.Audio(video_path)
        self.video_iniciarning = True
        self.audio_muted = False
        self.Frames()

        faq_frame = tk.Frame(self.ventana, bg=FAQ_BG)
        faq_frame.pack(fill='x', padx=10)
        tk.Label(faq_frame, text="Preguntas Frecuentes", font=subtitle_font, bg=FAQ_BG).grid(row=0, column=0, sticky='w', pady=(10,5))
        faqs = ["¿Cómo me registro?", "¿Cómo reprogramo mi cita?", "¿Qué documentos necesito?"]
        for i, text in enumerate(faqs, start=1):
            tk.Label(faq_frame, text=f"\u25CA {text}", font=faq_font, bg=FAQ_BG).grid(row=(i//2)+1, column=(i-1)%2, sticky='w', padx=20, pady=2)

        footer = tk.Frame(self.ventana, bg=FOOTER_BG, height=30)
        footer.pack(fill='x', side='bottom')
        tk.Label(footer, text="Pie de pagina", bg=FOOTER_BG, fg='black', font=subtitle_font).pack(pady=5)

        self.ventana.mainloop()

def main():
    app = video()
    app.iniciar()