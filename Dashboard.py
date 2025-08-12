import tkinter as tk 
from tkinter import messagebox  
import pandas as pd 
import matplotlib.pyplot as plt  
import os

class CitasDashboard:
    CARPETA = "citas_finalizadas"  # Carpeta donde están los archivos de citas

    def __init__(self):
        self.ventana = tk.Tk()  
        self.ventana.withdraw()  
        self.ventana.after(100, self.graficar)  

    def leer_txt_como_df(self, ruta):
        with open(ruta, encoding='utf-8') as f:  # Abre el archivo de texto
            contenido = f.read()  # Lee todo el contenido
        bloques = contenido.strip().split('-' * 40)  # Separa los bloques de registros
        registros = []
        for bloque in bloques:
            datos = {}
            for linea in bloque.strip().split('\n'):  # Procesa cada línea del bloque
                if ": " in linea:
                    clave, valor = linea.split(": ", 1)  # Separa clave y valor
                    datos[clave.strip()] = valor.strip()
            if datos:
                registros.append(datos)  # Agrega el registro si tiene datos
        return pd.DataFrame(registros)  # Devuelve un DataFrame con los registros

    def graficar(self):
        archivos = [f for f in os.listdir(self.CARPETA) if f.endswith(".txt")]  # Lista los archivos .txt en la carpeta
        if not archivos:
            messagebox.showerror("Error", "No hay archivos de citas finalizadas.")  # Muestra error si no hay archivos
            self.ventana.destroy()
            return

        dfs = []
        for archivo in archivos:
            ruta = os.path.join(self.CARPETA, archivo)  # Ruta completa del archivo
            df = self.leer_txt_como_df(ruta)  # Lee el archivo como DataFrame
            if not df.empty and 'Fecha' in df.columns:
                dfs.append(df)  # Agrega el DataFrame si tiene datos y columna Fecha

        if not dfs:
            messagebox.showerror("Error", "No se encontraron datos válidos en los archivos.")  # Error si no hay datos válidos
            self.ventana.destroy()
            return

        df_total = pd.concat(dfs, ignore_index=True)  # Une todos los DataFrames en uno solo
        citas_por_fecha = df_total['Fecha'].value_counts().sort_index()  # Cuenta citas por fecha

        plt.figure(figsize=(8, 6))  # Tamaño de la figura
        plt.bar(citas_por_fecha.index, citas_por_fecha.values, color='blue')  # Crea la gráfica de barras
        plt.title("Citas finalizadas por fecha")  
        plt.xlabel("Fecha") 
        plt.ylabel("Número de pacientes")  # Etiqueta del eje Y
        plt.xticks(rotation=45)  # Rota las etiquetas del eje X
        plt.tight_layout() 
        plt.show()  # Muestra la gráfica
        self.ventana.destroy() 

    def mostrar(self):
        self.ventana.mainloop()  