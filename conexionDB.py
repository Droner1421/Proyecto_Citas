import mysql.connector
import tkinter as tk
from tkinter import messagebox
#conexion a la base de datos mysql
def conexionDB():
    conexio = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='syra',
    )
    return conexio


