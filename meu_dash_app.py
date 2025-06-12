import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO
from app import app

# ========= App ============== #
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app.scripts.config.serve_locally = True
server = app.server

# ========== Styles ============ #

template_theme1 = "flatly"
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR
tab_card = {'height': '100%'}

# ===== Reading n cleaning File ====== #
df_main = pd.read_csv("data_gas.csv")
df_main['DATA INICIAL'] = pd.to_datetime(df_main["DATA INICIAL"])
df_main['DATA FINAL'] = pd.to_datetime(df_main["DATA FINAL"])   

df_main['DATA MEDIA'] = ((df_main['DATA FINAL'] - df_main['DATA INICIAL'])/2) + df_main['DATA INICIAL']
df_main = df_main.sort_values(by='DATA MEDIA', ascending=True)
df_main.rename(columns= {'DATA MEDIA': 'DATA'}, inplace=True)
df_main.rename(columns= {'PRECO MÉDIO REVENDA': 'VALOR REVENDA (R$/L)'}, inplace=True)

df_main['ANO'] = df_main['DATA'].apply(lambda x: str(x.year))
df_main = df_main[df_main.PRODUTO == 'GASOLINA COMUM']

#excluindo tabelas que nao vou usar 

df_main.drop(['UNIDADE DE MEDIDA', 'COEF DE VARIAÇÃO REVENDA', 'COEF DE VARIAÇÃO DISTRIBUIÇÃO', 
    'NÚMERO DE POSTOS PESQUISADOS', 'DATA INICIAL', 'DATA FINAL', 'PREÇO MÁXIMO DISTRIBUIÇÃO', 'PREÇO MÍNIMO DISTRIBUIÇÃO', 
    'DESVIO PADRÃO DISTRIBUIÇÃO', 'MARGEM MÉDIA REVENDA', 'PREÇO MÍNIMO REVENDA', 'PREÇO MÁXIMO REVENDA', 'DESVIO PADRÃO REVENDA', 
    'PRODUTO', 'PREÇO MÉDIO DISTRIBUIÇÃO'], inplace=True, axis=1)

df_main = df_main.reset_index()

df_store = df_main.to_dict()
# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    #armazenar o dataset
    dcc.Store(id='dataset', data=df_store),
    dcc.Store(id='dataset_fixed', data=df_store),



    #layout
    #row1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Gás Prices Analysis')
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-filter', style={'font-size': '300%'})
                        ], sm=4, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend('Henrique Analista')
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Visite meu Git', href="https://github.com/henrique9900/gasoline-analysis", target="_blank")
                        )
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Maximos e Minimos'),
                            dcc.Graph(id='static-maxmin', config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ], style=tab_card)
        ], sm=8, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6('Ano de Analise'),
                            dcc.Dropdown(
                                id="select ano",
                                value=df_main.at[df_main.index[1], 'ANO'],
                                clearable = False,
                                className='dbc',
                                options=[
                                    {"label": x, "value": x} for x in df_main.ANO.unique()
                            ]),
                        ], sm=6),
                        dbc.Col([
                            html.H6('Região de Analise'),
                            dcc.Dropdown(
                                id="select_regiao",
                                value=df_main.at[df_main.index[1], 'REGIÃO'],
                                clearable = False,
                                className='dbc',
                                options=[
                                    {"label": x, "value": x} for x in df_main.REGIÃO.unique()
                             ]),
                        ], sm=6)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='regiaobar_gaph', config={"displayModeBar": False, "showTips": False})
                        ], sm=12, md=6),
                        dbc.Col([
                            dcc.Graph(id='estadobar_graph', config={'displayModeBar': False, "showTips": False})
                        ])
                    ], style={'column-gap': '0 px'})
                ])
            ], style=tab_card)
        ], sm=12, lg=7)
    ]),

    

    #row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Preço x Estado'),
                    html.H6('Comparação temporal entre estados'),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id='select_estados0',
                                value=[df_main.at[df_main.index[3], 'ESTADO'], df_main.at[df_main.index[13], 'ESTADO'], df_main.at[df_main.index[6], 'ESTADO']],
                                clearable=False,
                                className='dbc',
                                multi=True,
                                options=[
                                    {"label": x, "value": x} for x in df_main.ESTADO.unique()
                                ]),
                        ], sm=10),
                    ]),
                    dbc.Row(
                        dbc.Col([
                            dcc.Graph(id='animation_graph', config={"displayModeBar": False})
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Comparação direta'),
                    html.H6('Qua preço é maior em um dado periodo de tempo'),
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id='select_estado1',
                                value=df_main.at[df_main.index[3], 'ESTADO'],
                                clearable=False,
                                className='dbc',
                                options=[
                                    {"label": x, "value": x} for x in df_main.ESTADO.unique()
                                ]),
                        ], sm=10, md=5),
                        dbc.Col([
                            dcc.Dropdown(
                                id='select_estado2',
                                value=df_main.at[df_main.index[1], 'ESTADO'],
                                clearable=False,
                                className='dbc', 
                                options=[
                                    {"label": x, "value": x} for x in df_main.ESTADO.unique()
                                ]),
                        ], sm=10, md=6),
                    ], style={'margin-top': '20px'}, justify='center'),
                    dcc.Graph(id='direct_comparison_graph', config={"displayModeBar": False, "showTips": False}),
                    html.P(id='desc_comparison', style={'color': 'gray', 'font-size': '80%'})
                ])
            ], style=tab_card)
        ], sm=12, md=6, lg=4),
    ])
    
           








], fluid=True, style={'height': '100%'})


# ======== Callbacks ========== #


# Run server
if __name__ == '__main__':
    app.run(debug=True)

