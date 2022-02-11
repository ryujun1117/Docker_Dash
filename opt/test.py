# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

app.layout = html.Div(children = [
    html.H1(children = "Iris_data DashBoard"),
   
    html.Div([
         html.Div('''
        x軸の選択↓
        '''),
        dcc.Dropdown(
            df.columns.to_list(),
            "sepal_length",
            id = "xaxis-column"
        ),
        dcc.RadioItems(
            ["Linear", "Log"],
            "Linear",
            id = "xaxis-type",
            inline = True
        ),
        dcc.Graph(
            id='indicator-graphic'
            # figure=fig,
            # style = {"width" : '48%', 'display':'inline-block'}
            ),
    ], style = {"width" : '48%', 'display':'inline-block'}),

    html.Div([
         html.Div('''
        y軸を選択↓
        '''),
        dcc.Dropdown(
            df.columns.to_list(),
            "sepal_width",
            id = "yaxis-column"
        ),
        dcc.RadioItems(
            ["Linear", "Log"],
            "Linear",
            id = "yaxis-type",
            inline = True
        ),
        dcc.Graph(
            id='histogram'
        )
    ], style = {"width" : '48%', 'float': 'right', 'display':'inline-block'}),

  
    # dcc.Graph(
    #     id='life-exp-vs-gdp2',
    #     figure=fig,
    #     style = {"width" : '48%', 'float':'right', 'display':'inline-block'}
    # )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    Output('histogram', 'figure'),
    Input("xaxis-column", 'value'),
    Input("yaxis-column", 'value'),
    Input("xaxis-type", 'value'),
    Input("yaxis-type", 'value'))

def update_graph(xaxis_column_name, yaxis_column_name,
                xaxis_type, yaxis_type):
    fig = px.scatter(df, x=df[xaxis_column_name], y=df[yaxis_column_name],
                  color="species", hover_name="species")
    fig.update_xaxes(title=xaxis_column_name,
                type = "linear" if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name,
                type = 'linear' if yaxis_type == 'Linear' else 'log')
    
    fig_hist = make_subplots(rows=2, cols=1)
    fig_hist.add_trace(go.Histogram(x=df[xaxis_column_name],autobinx=True, name=xaxis_column_name), 1, 1)
    fig_hist.add_trace(go.Histogram(x=df[yaxis_column_name], autobinx=True, name=yaxis_column_name), 2, 1)
    return (fig, fig_hist)

if __name__ == '__main__':
    app.run_server(debug=True)