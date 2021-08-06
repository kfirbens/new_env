import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import datetime

#Taken from https://opendata.cityofnewyork.us/
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash%20Components/Dropdown/Urban_Park_Ranger_Animal_Condition.csv")
df['year'] = pd.DatetimeIndex(df['Date and time of Ranger response']).year
df.head()

# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
app = dash.Dash(__name__)

cat_lst = ['Final Ranger Action', 'Age']
new_lst = [{'label': key, 'value': key} for key in cat_lst]
print(new_lst)

dates = [2018,2019,2020]
new_dates = [{'label': key, 'value': key} for key in dates]
print(new_dates)
# ---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([

        html.Label(['NYYY Calls for Animal Rescue']),
        dcc.Dropdown(id='my_dropdown',
                     options=new_lst,
                     value='Animal Class',
                     multi=False,
                     clearable=False,
                     style={"width": "50%"}
                     ),

        html.Label(['choose_date']),
        dcc.Dropdown(id='date_choosing',
                     options=new_dates,
                     value=2017,
                     multi=False,
                     clearable=False,
                     style={"width": "50%"}
                     ),

        # className='two columns')

    ]),
])

#---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value'),
     Input(component_id='date_choosing', component_property='value')]
)

def update_graph(my_dropdown, date_choosing):
    dff = df[(df['year']==date_choosing)]

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