import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from conexionDB import conexionDB

conexion = conexionDB()

df = pd.read_sql_query("select * from citas", conexion)

citas_al_dia = df["fecha_cita"].value_counts().sort_index()

plt.figure(figsize=(6, 6))
plt.bar(citas_al_dia.index, citas_al_dia.values, color='skyblue')
plt.title("Citas por Día")
plt.xlabel("Fecha")
plt.ylabel("Número de Citas")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
