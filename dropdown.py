import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#Taken from https://opendata.cityofnewyork.us/
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash%20Components/Dropdown/Urban_Park_Ranger_Animal_Condition.csv")
df.head()
# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
app = dash.Dash(__name__)

cat_lst = ['Final Ranger Action', 'Age']
new_lst = [{'label': key, 'value': key} for key in cat_lst]

#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.Label(['NYC Calls for Animal Rescue']),
        dcc.Dropdown(
            id='my_dropdown',
            options=new_lst,
            value='Animal Class',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

#---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def update_graph(my_dropdown):
    dff = df

    piechart=px.pie(
            data_frame=dff,
            names=my_dropdown,
            hole=.3,
            )

    return (piechart)


if __name__ == '__main__':
    # For Development only, otherwise use gunicorn or uwsgi to launch, e.g.
    # gunicorn -b 0.0.0.0:8050 index:app.server
    app.run_server(
        port=8050,
        host='0.0.0.0'
    )