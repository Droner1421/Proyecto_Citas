import tkinter as tk
from tkinter import ttk, font
from conexionDB import conexionDB
from tkinter import messagebox

def ventanaENF():
   
    HEADER_BG = '#8FD3F4'
    BUTTON_OP_BG = '#AAF0D1'
    BUTTON_OP_FG = '#000000'
    TABLE_BG = '#FFFFFF'
    TABLE_BORDER = '#DDDDDD'
    TIME_BG = '#E8F8EF'
    TIME_FG = '#2E8B57'
    CELL_BG = '#D3D3D3'
    FOOTER_BG = '#F5F5F5'

    root = tk.Tk()
    root.title("Próximas Citas")
    root.geometry("800x700")
    root.configure(bg='black')

  
    header = tk.Frame(root, bg=HEADER_BG, height=60, bd=2, relief='groove')
    header.pack(fill='x', side='top')

    logo = tk.Canvas(header, width=40, height=40, bg='white', highlightthickness=1)
    logo.create_oval(5, 5, 35, 35)
    logo.create_text(20, 20, text="L", font=("Arial", 14, "bold"))
    logo.pack(side='left', padx=10, pady=10)

    tk.Label(header, text="Logotipo", bg=HEADER_BG, fg='black', font=("Arial", 14, "bold")).pack(side='left')
    tk.Label(header, text="Nombre institucion", bg=HEADER_BG, fg='black', font=("Arial", 16, "bold")).pack(side='right', padx=20)

   
    topbar = tk.Frame(root, bg='#F5F5F5', height=40, bd=1, relief='groove')
    topbar.pack(fill='x')

    op_btn = tk.Menubutton(topbar, text="Operaciones", bg=BUTTON_OP_BG, fg=BUTTON_OP_FG, font=("Arial", 10, "bold"), relief='raised')
    op_menu = tk.Menu(op_btn, tearoff=0)
    op_menu.add_command(label="Nueva Cita", command=lambda: messagebox.showinfo("Nueva Cita", "Funcionalidad no implementada"))
    op_menu.add_command(label="Buscar Cita", command=lambda: messagebox.showinfo("Buscar Cita", "Funcionalidad no implementada"))
    op_menu.add_command(label="Opción 2", command=lambda: messagebox.showinfo("Opción 2", "Funcionalidad no implementada"))
    op_btn.config(menu=op_menu)
    op_btn.pack(side='left', padx=15, pady=5)


    tk.Button(topbar, text="Cerrar Sesión", bg='#FF6347', fg='white', font=("Arial", 10, "bold"), command=root.destroy).pack(side='right', padx=10, pady=5)

  
    main_frame = tk.Frame(root, bg=TABLE_BG)
    main_frame.pack(fill='both', expand=True, padx=20, pady=10)

    
    phone_icon = tk.Label(main_frame, text="📞", font=("Arial", 18), bg=TABLE_BG)
    phone_icon.pack(anchor='nw', pady=(10,0), padx=10)

  
    tk.Label(main_frame, text="¡PROXIMAS CITAS !", font=("Arial", 18, "bold"), fg="#1DA1F2", bg=TABLE_BG).pack(pady=(0,10))

   
    table_frame = tk.Frame(main_frame, bg=TABLE_BG, bd=2, relief='groove')
    table_frame.pack(padx=10, pady=10)

    days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]
    hours = ["00:00"] * 8

  
    tk.Label(table_frame, text="", bg=TABLE_BG).grid(row=0, column=0, padx=5, pady=5)
    for i, day in enumerate(days):
        tk.Label(table_frame, text=day, bg=TABLE_BG, font=("Arial", 10, "bold")).grid(row=0, column=i+1, padx=8, pady=5)

  
    for r in range(1, 9):
        tk.Label(table_frame, text="00:00", bg=TIME_BG, fg=TIME_FG, font=("Arial", 10, "bold")).grid(row=r, column=0, padx=5, pady=5, sticky='nsew')
        for c in range(1, 7):
            tk.Label(table_frame, bg=CELL_BG, width=12, height=2, bd=1, relief='flat').grid(row=r, column=c, padx=4, pady=4, sticky='nsew')


    footer = tk.Frame(root, bg=FOOTER_BG, height=40, bd=1, relief='groove')
    footer.pack(fill='x', side='bottom')
    tk.Label(footer, text="Pie de pagina", bg=FOOTER_BG, fg='black', font=("Arial", 14, "bold")).pack(pady=5)