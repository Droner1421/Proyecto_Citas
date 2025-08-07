import tkinter as tk  # Importa la librería tkinter para crear interfaces gráficas
from tkinter import messagebox  # Importa el módulo messagebox para mostrar mensajes emergentes
import os  # Importa el módulo os para interactuar con el sistema de archivos
import pandas as pd  # Importa pandas para manipulación de datos en DataFrames
import matplotlib.pyplot as plt  # Importa matplotlib para graficar datos

CARPETA = "citas_finalizadas"  # Define el nombre de la carpeta donde están los archivos de citas

def leer_txt_como_df(ruta):
    # Lee un archivo de texto y lo convierte en un DataFrame de pandas
    with open(ruta, encoding='utf-8') as f:
        contenido = f.read()  # Lee todo el contenido del archivo

    bloques = contenido.strip().split('-' * 40)  # Separa el contenido en bloques usando líneas de 40 guiones
    registros = []  # Lista para almacenar los registros
    for bloque in bloques:
        datos = {}  # Diccionario para almacenar los datos de cada bloque
        for linea in bloque.strip().split('\n'):
            if ": " in linea:
                clave, valor = linea.split(": ", 1)  # Separa la línea en clave y valor
                datos[clave.strip()] = valor.strip()  # Agrega la clave y valor al diccionario
        if datos:
            registros.append(datos)  # Agrega el diccionario a la lista de registros
    return pd.DataFrame(registros)  # Devuelve un DataFrame con todos los registros

def graficar():
    # Busca todos los archivos .txt en la carpeta y grafica la cantidad de citas por fecha
    archivos = [f for f in os.listdir(CARPETA) if f.endswith(".txt")]  # Lista los archivos .txt
    if not archivos:
        messagebox.showerror("Error", "No hay archivos de citas finalizadas.")  # Muestra error si no hay archivos
        return

    dfs = []  # Lista para almacenar los DataFrames de cada archivo
    for archivo in archivos:
        ruta = os.path.join(CARPETA, archivo)  # Obtiene la ruta completa del archivo
        df = leer_txt_como_df(ruta)  # Lee el archivo como DataFrame
        if not df.empty and 'Fecha' in df.columns:
            dfs.append(df)  # Agrega el DataFrame a la lista si tiene datos y columna 'Fecha'

    if not dfs:
        messagebox.showerror("Error", "No se encontraron datos válidos en los archivos.")  # Error si no hay datos válidos
        return

    df_total = pd.concat(dfs, ignore_index=True)  # Une todos los DataFrames en uno solo
    citas_por_fecha = df_total['Fecha'].value_counts().sort_index()  # Cuenta las citas por fecha y las ordena

    plt.figure(figsize=(8, 6))  # Crea una figura de tamaño 8x6
    plt.bar(citas_por_fecha.index, citas_por_fecha.values, color='blue')  # Grafica un diagrama de barras
    plt.title("Citas finalizadas por fecha")  # Título del gráfico
    plt.xlabel("Fecha")  # Etiqueta del eje X
    plt.ylabel("Número de pacientes")  # Etiqueta del eje Y
    plt.xticks(rotation=45)  # Rota las etiquetas del eje X
    plt.tight_layout()  # Ajusta el diseño para que no se sobrepongan los elementos
    plt.show()  # Muestra el gráfico


# En Dashboard_2.py
def mostrar_dashboard():
    # Crea la ventana principal del dashboard
    ventana = tk.Tk()  # Crea una nueva ventana de tkinter
    ventana.title("Visualizador de Citas Finalizadas")  # Título de la ventana
    ventana.geometry("450x200")  # Tamaño de la ventana
    tk.Label(ventana, text="Visualiza todas las citas finalizadas:", font=("Arial", 12)).pack(pady=20)  # Etiqueta descriptiva
    btn_graficar = tk.Button(
        ventana,
        text="Graficar todas las citas",
        command=graficar,
        bg="green",
        fg="white",
        font=("Arial", 11)
    )  # Botón para graficar
    btn_graficar.pack(pady=30)  # Muestra el botón en la ventana
    ventana.mainloop()  # Inicia el bucle principal de la interfaz gráfica