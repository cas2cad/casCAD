import sys

from cascad.experiment.MBM import analyze
sys.path.append('.')

from sqlite3.dbapi2 import Row
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from cascad.models.datamodel import GeneResultModel
import plotly.express as px

# from aletheia.analyze_model.load_exp import create_detail_fig, get_index_page
from cascad.experiment.MBM.load_exp import create_detail_fig, get_index_page


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


analyze = analyze.Analyze('exp3')
analyze.load_data(round=2)
GL_RL_DF = analyze.create_multiline_RL_GL()
GL_RL_fig = px.line(GL_RL_DF, x='iter', y='value', color='color', title='RL and MEL Changed Over Iter')
GL_RL_fig.update_layout(
    font=dict(
        size=18,  # 这里可以调整字体大小
    ),
)


agent_df = analyze.create_multiline()
agent_fig = px.line(agent_df, x='iter', y='value', color='color', title='Agent Proportion Over Iter')
agent_fig.update_layout(
    font=dict(
        size=18,  # 这里可以调整字体大小
    ),
)

TOPN_DF = analyze.get_code_iter(99)

# def generate_table(dataframe, max_rows=10):
#     return dbc.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ], style={'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center'})


def generate_table(dataframe, max_rows=40):
    return dbc.Table([
        html.Thead(
            html.Tr([html.Th(col, style={'fontSize': '20px'}) for col in dataframe.columns]),
            style={'textAlign': 'center'}
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col], style={'fontSize': '20px'}) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center'})


app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),

        dbc.Row(dbc.Col(html.H1(children='Analysis of MAM Experiment',
                                style={'textAlign': 'center'}))),

        # dbc.Row(dbc.Col(html.Div(children='''
            # Analyze and visualize the result of casCAD2.
    # ''', style={'textAlign': 'center'}))),

        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='example=graph',
                        figure=GL_RL_fig),
                ),

                dbc.Col(
                    dcc.Graph(
                        id='burned graph',
                        figure=agent_fig 
                    )
                )

                 ], align='center'),

        html.Hr(),
        dbc.Row(html.Div(children='''
           Code of Top 8 Largest Lost Scenarios.
    ''', style={'textAlign': 'center', 'fontSize': '20px'})),
        # html.Br(),
        dbc.Row(
            dbc.Col(
            generate_table(TOPN_DF))
            , align='center'
        ),

        html.Hr(),

        # dbc.Row(dbc.Col(html.Div(id='page-content', children=[])))
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