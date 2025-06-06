import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import threading
import webview
from conexionDB import conexionDB


def cargar_datos():
    conn = conexionDB()
    df = pd.read_sql_query("SELECT fecha_cita FROM citas", conn)
    conn.close()
    return df

df = cargar_datos()
df_grouped = df['fecha_cita'].value_counts().reset_index()
df_grouped.columns = ['Fecha', 'Número de citas']
df_grouped = df_grouped.sort_values(by='Fecha')


app = dash.Dash(__name__)
app.title = "Dashboard de Citas Médicas"

app.layout = html.Div([
    html.H1("Grafica", style={'textAlign': 'center'}),
    dcc.Graph(
        id='grafico',
        figure=px.bar(
            df_grouped,
            x='Fecha',
            y='Número de citas',
            title="Cantidad de Citas por Fecha",
            labels={'Fecha': 'Fecha', 'Número de citas': 'Citas'},
            template='plotly_white',
            color='Número de citas',
            color_continuous_scale='Plasma',
        )
    )
])


def iniciar_dash():
    app.run(debug=False, use_reloader=False)


if __name__ == '__main__':
    dash_thread = threading.Thread(target=iniciar_dash)
    dash_thread.daemon = True
    dash_thread.start()

    webview.create_window("Grafica", "http://127.0.0.1:8050", width=900, height=600)
    webview.start()
