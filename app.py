import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from src.plots import pie_plot_1, pie_plot_2, tests, test_selector, stats, stats_plot
from flask import Flask
import plotly.graph_objects as go


NAVBAR_NAMES = ['Menu' ,'Testy', 'Statystyki', 'O nas']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)

app.config['suppress_callback_exceptions'] = True
app.config.suppress_callback_exceptions = True

img_url = 'https://images.unsplash.com/photo-1520333789090-1afc82db536a?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1351&q=80'

def page_0():
    text =  html.Div(
            [
                html.H4("WSZYSTKIE TESTY W JEDNYM MIEJSCU!"),
                html.P(
                    "Testy predyspozycji zawodowych i psychologicznych z dokładnym opisem, zobacz tez co wybrały podobne do Ciebie osoby",
                ),
            ],
        )
    column1 = [dbc.Row(text), dbc.Row(html.Img(src=img_url, style={'width': '100%'}))]
    column1 = dbc.Col(column1, width={"size": 7})
    column2 = dbc.Col([dbc.Row(dbc.Col([dcc.Graph(figure=pie_plot_1(), style={})]),), 
                       dbc.Row(dbc.Col(dcc.Graph(figure=pie_plot_2(), style={}))),
                       ], 
                       width={"size": 5}
                       )

    template = dbc.Row([column1, column2], id='main', align="center")
    return template

# navbar_buttons = [dbc.Col(html.Button(name, id=f'btn-nclicks-{i}', n_clicks=0), width=True) for i, name in enumerate(NAVBAR_NAMES)]
navbar_buttons = [html.Button(name, id=f'btn-nclicks-{i}', n_clicks=0, style={'width': '25%'}) for i, name in enumerate(NAVBAR_NAMES)]

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1('Z nami po przyszłość!', style={"text-align": "left"}), width={"size": 4, "offset": 4})),
    dbc.Row(navbar_buttons),
    page_0(),
])

@app.callback(Output('main', 'children'),
              Input('btn-nclicks-0', 'n_clicks'),
              Input('btn-nclicks-1', 'n_clicks'),
              Input('btn-nclicks-2', 'n_clicks'),
              Input('btn-nclicks-3', 'n_clicks'),)
def displayClick(btn0, btn1, btn2, btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-0' in changed_id:
        msg = page_0()
    elif 'btn-nclicks-1' in changed_id:
        msg = tests()
    elif 'btn-nclicks-2' in changed_id:
        msg = stats()
    elif 'btn-nclicks-3' in changed_id:
        msg = 'Button 3 was most recently clicked'
    else:
        msg = page_0()
    return msg


@app.callback(Output('tests', 'children'),
              [Input(component_id='dost', component_property='value'), Input(component_id='time', component_property='value')],)
def displayClick(value, max_time):
    print(value)
    if value == 'all':
        msg = tests(dost='all', max_time=max_time)
    elif value == 'bp':
        msg = tests(dost='bp', max_time=max_time)
    else:
        msg = tests(dost='p', max_time=max_time)
    return msg


@app.callback(Output('stats_plot', 'children'),
              Input('stats_button', 'n_clicks'),)
def displayClick(btn):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'stats_button' in changed_id:
        msg = dcc.Graph(figure=stats_plot(), style={})
    else:
        msg = ''
    return msg


if __name__ == '__main__':
    app.run_server()
