import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dash_table
import pandas_datareader.data as web
import datetime
import dash_table as dt

df = pd.read_csv("IBM_HR_DATA_NEW.csv")
df.head()

numeric_col = ['Age','DistanceFromHome','MonthlyIncome']
categorical_col = ['Gender','MaritalStatus','Education','Department']

options=[{'label':x, 'value':x} for x in df.sort_values('DistanceFromHome')['DistanceFromHome'].unique()]


dff = df
boxplot = px.box(
    data_frame=dff,
    y=dff['Age'],
    # hover_data=['country'],
    # text="country",
    height=550
)
boxplot.update_traces(quartilemethod="exclusive")
boxplot.show()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}] ## adjust graph to phones
                )

app.layout = dbc.Container([

    #for headline
    dbc.Row(
        dbc.Col(html.H1("Exploraty data analysis",
                        className='text-center text-primary mb-4'), #https://hackerthemes.com/bootstrap-cheatsheet/
                width=12)
    ),

    dbc.Row([
        #----------------------------scatter plot 2 numeric -------------------------------------------------
        dbc.Col([
            html.P("Select 2 numeric variable:",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='numeric_1', multi=False, value=numeric_col[0],
                         options=[{'label': x, 'value': x} for x in numeric_col],
                         ),
            dcc.Dropdown(id='numeric_2', multi=False, value=numeric_col[0],
                         options=[{'label': x, 'value': x} for x in numeric_col],
                         ),
            html.P("Select variable for hue:",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='categorical_55', multi=False, value=categorical_col[0],
                         options=[{'label': x, 'value': x} for x in categorical_col],
                         ),
            dcc.Graph(id='sctter_between_numeric', figure={})  # declare empty figure, one row has 12 column
        ],  # width={'size':5, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=5, xl=5  ## adjust layout to screen size
        ),
        #-----------------------------------Pie chart------------------------------------------------------
        dbc.Col([
            html.P("Select 2 variable:",
                   style={"textDecoration": "underline"}),
            # dcc.Dropdown(id='variable_1', multi=False, value=2016,
            #              options=[{'label':x, 'value':x} for x in df.sort_values('DistanceFromHome')['DistanceFromHome'].unique()],
            #              ),
            dcc.Dropdown(id='variable_2', multi=False, value=categorical_col[0],
                         options=[{'label': x, 'value': x} for x in categorical_col],
                         ),
            dcc.Graph(id='pie_chart', figure={})  # declare empty figure, one row has 12 column
        ],
            xs=12, sm=12, md=12, lg=5, xl=5  ## adjust layout to screen size
        ),
        ], no_gutters=False, justify='start'),

    dbc.Row([
        # ------------------------------Box plot one feature----------------------------------------
        dbc.Col([
            html.P("Box-plot for one feature",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='numeric_3', multi=False, value=numeric_col[0],
                         options=[{'label': x, 'value': x} for x in numeric_col],
                         ),
            dcc.Graph(id='box_plot', figure={})  # declare empty figure, one row has 12 column
        ],
            xs=12, sm=12, md=12, lg=5, xl=5  ## adjust layout to screen size
        ),
        #------------------------Box plot categorical vs numeric feature---------------#
        dbc.Col([
            html.P("Box-plot for 2 feature:",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='categorical_10', multi=False, value=categorical_col[0],
                         options=[{'label': x, 'value': x} for x in categorical_col],
                         ),
            dcc.Dropdown(id='Numerical_10', multi=False, value=numeric_col[0],
                         options=[{'label': x, 'value': x} for x in numeric_col],
                         ),
            dcc.Graph(id='box_plot_2_cat_vs_num', figure={})  # declare empty figure, one row has 12 column
        ],
            xs=12, sm=12, md=12, lg=5, xl=5  ## adjust layout to screen size
        ),
        # --------------------------------------------------------------------------------------------
    ], no_gutters=False, justify='start'),

    dbc.Row([
        # --------------------------------------------------------------------------------------------
        dbc.Col([
            html.P("suicide rates dashboard_1",
                   style={"textDecoration": "underline"}),
            dcc.Dropdown(id='categorical_3', multi=False, value=categorical_col[0],
                         options=[{'label': x, 'value': x} for x in categorical_col],
                         ),
            dcc.Dropdown(id='categorical_4', multi=False, value=categorical_col[1],
                         options=[{'label': x, 'value': x} for x in categorical_col],
                         ),
            html.Div(id='table-container', className='tableDiv')
        ],
            xs=12, sm=12, md=12, lg=5, xl=5  ## adjust layout to screen size
        )
        # --------------------------------------------------------------------------------------------
    ], no_gutters=False, justify='start')


], fluid=True) #fluid for strach graph without space



#------------------------Scatter plot 2 numeric---------------
@app.callback(
    Output('sctter_between_numeric', 'figure'), ## graph_id
    [Input('numeric_1', 'value'),
     Input('numeric_2', 'value')]
)

def update_graph(numeric_1, numeric_2):
    # print(years_chosen)

    dff=df

    scatterplot = px.scatter(
        data_frame=dff,
        x=dff[numeric_1],
        y=dff[numeric_2],
        color=dff['Gender'],
        height=550,
        template="simple_white"
    )

    scatterplot.update_traces(textposition='top center')

    return (scatterplot)

#------------------------Pie chart---------------
@app.callback(
    Output('pie_chart','figure'), ## graph_id
    [#Input('variable_1','value'),
     Input('variable_2','value')]
)

def update_graph(variable_2):
    # print(years_chosen)

    #dff=df[df['DistanceFromHome'] == variable_1]
    dff=df
    piechart=px.pie(
            data_frame=dff,
            names=variable_2,
            hole=.3,
            )

    return (piechart)

#------------------------Box plot one feature---------------
@app.callback(
    Output('box_plot','figure'), ## graph_id
    [Input('numeric_3','value')]
)

def update_graph(numeric_3):
    # print(years_chosen)

    dff= df
    box_1_feature_graph = px.box(
        data_frame=dff,
        y=numeric_3,
        #hover_data=['country'],
        #text="country",
        height=550,
        template="simple_white"
    )

    # box_graph.update_traces(textposition='top center', quartilemethod="exclusive")
    box_1_feature_graph.update_traces(quartilemethod="exclusive")

    return (box_1_feature_graph)


#------------------------Box plot categorical vs numeric feature---------------
@app.callback(
    Output('box_plot_2_cat_vs_num','figure'), ## graph_id
    [Input('categorical_10','value'),
     Input('Numerical_10','value')]
)

def update_graph(categorical_10,Numerical_10):
    # print(years_chosen)

    dff= df
    box_2_feature_graph = px.box(
        data_frame=dff,
        x=categorical_10,
        y=Numerical_10,
        height=550,
        template="simple_white"
    )

    # box_graph.update_traces(textposition='top center', quartilemethod="exclusive")
    box_2_feature_graph.update_traces(quartilemethod="exclusive")

    return (box_2_feature_graph)

@app.callback(
    Output('table-container','children'), ## graph_id
    [Input('categorical_3','value'),
     Input('categorical_4','value')]
)

def update_graph(categorical_3, categorical_4):

    dff=df[[categorical_3, categorical_4]].value_counts().round(2).reset_index()
    dff.columns = [categorical_3, categorical_4, 'count']
    dff = dff.sort_values(by=[categorical_3,categorical_4],
                                 ascending=[True, True])
    return html.Div([
        dt.DataTable(

            id='main-table',
            columns=[{'name': i, 'id': i} for i in dff.columns],
             data=dff[0:50].to_dict('rows'),
             style_table={
                'maxHeight': '20%',
                #'overflowY': 'scroll',
                'width': '60%',
                'minWidth': '30%',
            },
            style_header={'backgroundColor': 'rgb(230, 230, 230)'},
            style_cell={'backgroundColor': 'rgb(250, 250, 250)','color': 'black','height': 'auto','width': 'auto'},#minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'},
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