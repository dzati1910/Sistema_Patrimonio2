from django.utils import html
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Criando o app Dash dentro do Django
app = DjangoDash('SimpleExample')

# Criando um conjunto de dados fictício
df = pd.DataFrame({
    "Categoria": ["A", "B", "C", "D", "E"] * 2,
    "Valor": [10, 20, 30, 40, 50, 15, 25, 35, 45, 55],
    "Grupo": ["Grupo 1"] * 5 + ["Grupo 2"] * 5
})

# Layout do Dash
app.layout = html.Div([
    html.H1("Dashboard Interativo", style={"textAlign": "center"}),

    # Dropdown para seleção de grupo
    dcc.Dropdown(
        id='dropdown-grupo',
        options=[{'label': g, 'value': g} for g in df['Grupo'].unique()],
        value='Grupo 1',
        clearable=False,
        style={"width": "50%", "margin": "auto"}
    ),

    # Slider para multiplicar os valores
    dcc.Slider(
        id='slider-multiplicador',
        min=1,
        max=5,
        step=0.5,
        value=1,
        marks={i: str(i) for i in range(1, 6)}
    ),

    # Gráfico dinâmico
    dcc.Graph(id='grafico-barra')
])


# Callback para atualizar o gráfico
@app.callback(
    Output('grafico-barra', 'figure'),
    Input('dropdown-grupo', 'value'),
    Input('slider-multiplicador', 'value')
)
def atualizar_grafico(grupo_selecionado, multiplicador):
    df_filtrado = df[df['Grupo'] == grupo_selecionado].copy()
    df_filtrado['Valor'] *= multiplicador

    fig = px.bar(df_filtrado, x="Categoria", y="Valor", title=f"Grupo: {grupo_selecionado}",
                 color="Categoria", text="Valor")

    fig.update_traces(textposition="outside")
    return fig

app2 = DjangoDash('GraficoLinha')

df2 = pd.DataFrame({
    "Ano": [2018, 2019, 2020, 2021, 2022],
    "Vendas": [100, 150, 200, 250, 300]
})

app2.layout = html.Div([
    html.H3("Evolução das Vendas"),
    dcc.Graph(
        id='grafico-linha',
        figure=px.line(df2, x="Ano", y="Vendas", title="Vendas ao longo dos anos")
    )
])
