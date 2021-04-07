import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import random
from sklearn.decomposition import PCA
import plotly.express as px
from src.polar_plot import polar_plot

TEST_PATH = 'data/tests.csv'
TEST_URL = 'https://niezbednikmanagera.pl/wp-content/uploads/2020/01/kompetencjometr-1.png'
app_color = {"graph_bg": "white", "graph_line": "#007ACE"}

OLD_SCORES = ''

GROUP = {'0': 'humanityczne', '1': 'scisle', '2': 'spoleczne', '3': 'fizyczne', '4': 'artystyczne'}
GENDER = {'0': 'kobieta', '1': 'mezczynza', '2': 'inna'}
OCCUP = {'0': ['psycholog', 'kognitywistyk', 'historyk', 'pracownik naukowy', 'scojolog', 'HR', 'PR', 'nauczyciel polskiego', 'prawnik', 'historyk sztuki', 'wydawca', 'dziennikarz śledczy'],
         '1': ['nauczyciel fizyki', 'nauczyciel matematyki', 'analityk bankowy', 'pracownik naukowy', 'laborant', 'analityk biznesowy', 'informatyk', 'programista', 'tester QA', 'geodeta'],
         '2': ['specjalista PR', 'specjalista ds reklamy', 'key accoun manager', 'behawiorysta', 'psi psycholog', 'sekretarka', 'opiekun biura', 'przedszkolanek', 'social media master'],
         '3': ['trener personalny', 'trener krav maga', 'nauczyciel wf', 'yoga guru', 'ratoiwnik basenowy', 'trener seniorów', 'trener pływania', 'ochroniarz'],
         '4': ['street painter', 'artysta uliczny', 'kierownik domu kultury', 'rzeźbiarz', 'portrecista', 
         'akrobata sceniczny', 'prjektand graficzny', 'ux designer', 'ui designer', 'grafik', 'rekonstruktor', 'konserwator sztuki']}



def get_data():
    groups_data = []
    for i in range(5):
        data = pd.DataFrame()
        mi = 1
        for j in range(5):
            data[f'{j}'] = np.random.normal((i * mi) * 1.1, j * 1.2 + 3, 400)
            print(data)
        # data['group'] = GROUP[str(i)]
        data['group'] = i
        groups_data.append(data)
    return pd.concat(groups_data)


def pie_plot_1(title='studiujący w wieku 20-30 (%)'):
    labels = ['studiujący','pozostali']
    values = [55, 45]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(showlegend=True, title=title, 
                      plot_bgcolor=app_color["graph_bg"],
                      paper_bgcolor=app_color["graph_bg"])
    return fig

def pie_plot_2(title='Zadowoleni z wyboru studiów w wieku 20-30 (%)'):
    labels = ['zadowoleni','niezadowoleni', 'brak odpowiedzi']
    values = [10, 70, 20]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(showlegend=True, title=title, 
                      plot_bgcolor=app_color["graph_bg"],
                      paper_bgcolor=app_color["graph_bg"])
    return fig


def pie_plot_3(title='Popularność wyników'):
    labels = ['zadowoleni','niezadowoleni', 'brak odpowiedzi']
    values = [10, 70, 20]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(showlegend=True, title=title, 
                      plot_bgcolor=app_color["graph_bg"],
                      paper_bgcolor=app_color["graph_bg"])
    return fig

MODES = {'p': 'platny', 'bp': 'bezplatny'}

def make_image(url, info):
    image = html.A(html.Img(src=url, style={'width': '100%', 'height': '100%'}), href=info['link'])
    desc1 = html.Div(info['test'], className='desc')
    desc2 = html.Div(info['opis'], className='desc')
    desc3 = html.Div(MODES[info['dost']], className='desc')
    desc4 = html.Div(f"czas: {info['czas']} min", className='desc')
    image = html.Div([image, desc1, desc2, desc3, desc4], className='gallery')
    return image

def test_selector(mode):
    title = html.H3('dostep')
    dost = dcc.RadioItems(
        options=[
            {'label': 'bezplatne', 'value': 'bp'},
            {'label': 'platne', 'value': 'p'},
            {'label': 'wszystkie', 'value': 'all'}
        ],
        value=mode,
        labelStyle={'display': 'inline-block'},
        id = 'dost'
    )  

    # time = 
    return html.Div([title, dost])


def time(curr_time=40):
    title = html.H3('maksymalny czas (min)')
    time_selector = dcc.Slider(
        id='time',
        min=0,
        max=50,
        step=None,
        value=curr_time,
        marks={i: f'{i}' for i in range(0, 50, 5)},
    )

    # time = 
    return html.Div([title, time_selector], style = {'width': '50%'})


def tests(dost='all', max_time=40):
    data = pd.read_csv(TEST_PATH)
    print(max_time)
    data = data[data.czas <= max_time]
    print(data.shape)
    if dost != 'all':
        data = data[data.dost==dost]
    n = data.shape[0]
    rows = []
    row_items = [dbc.Row([test_selector(dost), time(max_time)])]
    col_items = []
    for i in range(1, n+1):
        info = data.iloc[i - 1] 
        image = make_image(info['img'], info)
        col = dbc.Col(image, width={"size": 4})
        col_items.append(col)
        if i % 3 == 0:
            row = dbc.Row(col_items)
            row_items.append(row)
            col_items = []
    if n % 3 != 0 and n > 0:
        row_items.append(dbc.Row(col_items))


    # row_items.append(row)
    return html.Div(row_items, id='tests')


def test_output(test_name):
    title = html.H3(test_name)
    drop =  dcc.Dropdown(
        id='test_name',
        options=[{'label': f'bla_bla_{i}', 'value': i} for i in range(10)],
        value=f'bla_bla_{0}',
        style = {'width': '100%'}
    )

    return dbc.Col(html.Div([title, drop]))


def stats_plot():
    data = get_data()
    pca = PCA(n_components=2)
    X = data[data.columns[:-1]]

    pca = PCA(n_components=2)
    components = pca.fit_transform(X)
    print(components)
    sat = [random.randint(0, 10) for _ in range(data.shape[0])]
    data['group_str'] = [f'{GROUP[str(i)]} <br> {OCCUP[str(i)][random.randint(0, len(OCCUP[str(i)]) - 1)]} <br> satysfakcja: {sat[j]}' for j, i in enumerate(data['group'].values)]
    print(data['group_str'])

    fig = px.scatter(components, x=0, y=1, color=data['group'])

    fig = go.Figure(data=go.Scatter(x=[c[0] for c in components],
                                    y=[c[1] for c in components],
                                    opacity=0.5,
                                    mode='markers',
                                    marker_color=data['group'],
                                    text=data['group_str'])) # hover text goes here

    fig.update_layout(title='Osoby z podobnymi wynikami testów')
    fig.update_layout(showlegend=False)

    fig.add_trace(
    go.Scatter(
        x=[20],
        y=[4],
        mode="markers",
        line=go.scatter.Line(color="red"),
        marker=dict(size=12),
        showlegend=False)
)
    fig.update_layout(plot_bgcolor=app_color["graph_bg"],
                    paper_bgcolor=app_color["graph_bg"])

    return fig



def stats():
    # row_items.append(row)
    selectors = []
    for i in range(6):
        selectors.append(test_output(f'test {i}'))
    
    selectors.append(html.Button('show', id='stats_button'))
    row = dbc.Row(selectors, id='tests_scores')
    rows = html.Div([dbc.Row(html.H2('Sprawdź jakie zawody wybrały osoby z podobnymi wynikami testów!')), 
                    row, dbc.Row([dbc.Col(id='stats_plot', width={"size": 6}), 
                                  dbc.Col(dcc.Graph(figure=polar_plot(), id='polar_plot'), width={"size": 6})]), 
                                  dbc.Row(dcc.Graph(figure=popularity_data(), style={}))])
    return rows


def popularity_data(k=100):
    data = get_data()
    data = data.sample(n=k, random_state=1)
    data['num'] = 1
    data['proff'] = [GROUP[str(i)] for i in data['group'].values]
    df = data.groupby(['group']).sum()
    df['proff'] = [GROUP[str(i)] for i in df.index]
    print(df)
    fig = go.Figure(data=[
        go.Bar(name='grupa', x=df['proff'], y=df['num']),
        go.Bar(name='satysfakcja (średnia)', x=df['proff'], y=[round(random.random(), 2) * 9 for _ in range(df.shape[0])])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    return fig


