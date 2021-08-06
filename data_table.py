import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv("suicide_rates.csv")

app = dash.Dash(__name__)
#style={'visibility': 'hidden'}

dpdown = []
for i in df['sex'].unique() :
   str(dpdown.append({'label':i,'value':(i)}))

app.layout = html.Div([
             html.P([
             html.Label("Choose a feature"),
             html.Div(dcc.Dropdown(id='dropdown', options=dpdown),
                                style = {'width': '100px',
                                    'fontSize' : '10px',
                                    'padding-left' : '100px',
                                    'display': 'inline-block'})]),


    #style={'visibility': 'hidden'},
            html.Div(id='table-container',  className='tableDiv'),
            dcc.Graph(id = 'plot',style={'height' : '25%', 'width' : '25%'})

   ])
    #dcc.Dropdown(id='dropdown', style={'height': '30px', 'width': '100px'}, options=dpdown),
    #dcc.Graph(id='graph'),
                #html.Div(html.H3('country graph'),id='table-container1',className='tableDiv1')



@app.callback(
    dash.dependencies.Output('table-container','children'),
    [dash.dependencies.Input('dropdown', 'value')])

def display_table(dpdown):
    df_temp = df[df['sex']==dpdown]
    return html.Div([
        dt.DataTable(
            id='main-table',
            columns=[{'name': i, 'id': i} for i in df_temp.columns],
             data=df_temp[0:5].to_dict('rows'),
             style_table={
                'maxHeight': '20%',
                #'overflowY': 'scroll',
                'width': '30%',
                'minWidth': '10%',
            },
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={'backgroundColor': 'rgb(50, 50, 50)','color': 'white','height': 'auto','width': 'auto'},#minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'},
            #style_cell={'minWidth': '120px', 'width': '150px', 'maxWidth': '180px'},
              style_data={'whiteSpace': 'auto','height': 'auto','width': 'auto'}

    )

    ])


if __name__ == '__main__':
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(
        port=8050,
        host='0.0.0.0'
    )