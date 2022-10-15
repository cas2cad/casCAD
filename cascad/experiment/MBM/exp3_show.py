import sys
sys.path.append('.')

from aletheia.agents.desires import Trader
from sqlite3.dbapi2 import Row
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Br import Br
from dash_html_components.Hr import Hr
import dash_bootstrap_components as dbc

from aletheia.analyze_model.load_exp import create_detail_fig, get_index_page


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),

        dbc.Row(dbc.Col(html.H1(children='Experiment 3',
                                style={'textAlign': 'center'}))),

        dbc.Row(dbc.Col(html.Div(children='''
            Analyze and visualize the result of Aletheia.
    ''', style={'textAlign': 'center'}))),

        html.Hr(),
        dbc.Row(dbc.Col(html.Div(id='page-content', children=[])))
    ]
)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    # if pathname in []:
    # if re.match(pathname, 'gen_\d')
    # return create_detail_fig()
    if pathname[1:]:
        return create_detail_fig(pathname[1:])
    return get_index_page()
    # return create_detail_fig('')


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8056)