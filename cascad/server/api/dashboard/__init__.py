"""Experiment Show with Dash app
"""
import dash
from cascad.experiment.MBM import analyze as analyze_mbm
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from cascad.models.datamodel import GeneResultModel
import plotly.express as px

# from aletheia.analyze_model.load_exp import create_detail_fig, get_index_page
from cascad.experiment.MBM.load_exp import create_detail_fig, get_index_page


def init_dashboard(server): 
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/exp1/",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP
        ],
    )

    # analyze = analyze_mbm.Analyze("exp3")
    # analyze.load_data(round=2)
    # GL_RL_DF = analyze.create_multiline_RL_GL()
    # GL_RL_fig = px.line(GL_RL_DF, x='iter', y='value', color='color', title='RL and MEL Changed Over Iter')
    
    # agent_df = analyze.create_multiline()
    # agent_fig = px.line(agent_df, x='iter', y='value', color='color', title='Agent Proportion Over Iter')
    
    # TOPN_DF = analyze.get_code_iter(99)

    def generate_table(dataframe, max_rows=10):
        return dbc.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ], style={'marginLeft': 'auto', 'marginRight': 'auto', 'textAlign': 'center'})
    
 

    dash_app.layout = html.Div(
        children=[
            dcc.Location(id='url', refresh=False),
    
            dbc.Row(dbc.Col(html.H1(children='Analysis of MBM Experiment',
                                    style={'textAlign': 'center'}))),

            html.Div(id='page-content', children=[html.H1(children='Data is loading......',
                                    style={'textAlign': 'center'})]),
            # html.Div(
            #     [
            #         html.Progress(id="progress_bar"),
            #     ]
            # ),
    
        #     html.Hr(),
        #     dbc.Row(
        #         [
        #             dbc.Col(
        #                 dcc.Graph(
        #                     id='example=graph',
        #                     figure=GL_RL_fig),
        #             ),
    
        #             dbc.Col(
        #                 dcc.Graph(
        #                     id='burned graph',
        #                     figure=agent_fig 
        #                 )
        #             )
    
        #              ], align='center'),
    
        #     html.Hr(),
        #     dbc.Row(html.Div(children='''
        #        Code of Top 10 Largest Lost Scenarios.
        # ''', style={'textAlign': 'center'})),
        #     dbc.Row(
        #         dbc.Col(
        #         generate_table(TOPN_DF))
        #         , align='center'
        #     ),
    
        #     html.Hr(),
    
            # dbc.Row(dbc.Col(html.Div(id='page-content', children=[])))
        ]
    )
    
    @dash_app.callback(dash.dependencies.Output('page-content', 'children'),
                  [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        # if pathname in []:
        # if re.match(pathname, 'gen_\d')
        # return create_detail_fig()
        # if pathname[1:]:
            # return create_detail_fig(pathname[1:])
        # return get_index_page()
        # return create_detail_fig('')
        _id = pathname.split('/')[-1]
        print(_id)
        analyze = analyze_mbm.Analyze(_id)
        analyze.load_data(round=2)
        GL_RL_DF = analyze.create_multiline_RL_GL()
        GL_RL_fig = px.line(GL_RL_DF, x='iter', y='value', color='color', title='RL and MEL Changed Over Iter')
        
        agent_df = analyze.create_multiline()
        agent_fig = px.line(agent_df, x='iter', y='value', color='color', title='Agent Proportion Over Iter')
        
        TOPN_DF = analyze.get_code_iter(99)

        return [

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
               Code of Top 10 Largest Lost Scenarios.
        ''', style={'textAlign': 'center'})),
            dbc.Row(
                dbc.Col(
                generate_table(TOPN_DF))
                , align='center'
            ),
    
            html.Hr(),
        ]
 
        # return html.Div(html.H1(children='Display function actived',
                                    # style={'textAlign': 'center'}))

    return dash_app.server