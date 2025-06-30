import mysql.connector
import tkinter as tk
from tkinter import messagebox

def conexionDB():
    conexio = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='syra2',
    )
    return conexio


