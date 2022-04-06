from flask import Blueprint, render_template, url_for, request
from cascad.models.datamodel import AgentTypeModel, ComputeExperimentModel, ComputeExperimentTypeModel, AgentModel
from pyecharts import options as opts
from pyecharts.charts import Bar, Scatter
from jinja2 import Markup
from cascad.experiment.token_sender import ERC20TokenWorld

home_bp = Blueprint('home_bp', __name__)

def bar_base() -> Scatter:
    c = (
        Scatter()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="代币分布图"))
    )
    return c

def token_discribute(max_step, world_id) ->  Scatter:
    agent_models = AgentModel.objects(step=max_step, world_id=world_id)
    result = [
            (str(agent_model.unique_id)[-4:], agent_model.state['token']) for agent_model in agent_models
    ]
    c = (
        Scatter()
        .add_xaxis([x[0] for x in result])
        .add_yaxis("代币数量", [x[1] for x in result])
        .set_global_opts(title_opts=opts.TitleOpts(title="代币分布图"))
    )
    return c

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@home_bp.route("/compute_experiment", methods=['GET', 'POST'])
def compute():
    experiments = ComputeExperimentModel.objects.all()

    return render_template('compute_experiment.html', experiments=experiments)

@home_bp.route("/agents", methods=['GET', 'POST'])
def agent():
    if request.method == 'POST':
        agent_type = request.form['agent_type']

    else:
        agents = AgentTypeModel.objects.all()
        return render_template('agent.html', agents=agents)


@home_bp.route("/config_experiment", methods=["GET", "POST"])
@home_bp.route("/config_experiment/<step>", methods=["GET", "POST"])
def config_experiment(step=0):
    step = int(step)
    if request.method == 'POST':
        experiment_type = request.form['experiment_type']
        if step == 1:
            agent_types = AgentTypeModel.objects.all()
            return render_template(
                'config_1.html',
                experiment_type = experiment_type,
                agent_types = agent_types
            )
        elif step == 2:
            selected_agents = request.form.getlist('agent_types')
            experiment_type = request.form['experiment_type']
            experiment_params = ComputeExperimentTypeModel.objects.get(experiment_type=experiment_type).experiment_params
            agent_types = AgentTypeModel.objects.all()
            selected_agent_types = zip(agent_types, selected_agents)

            return render_template(
                'config_2.html',
                experiment_type = experiment_type,
                experiment_params = experiment_params,
                agent_types = agent_types,
                selected_agents = selected_agents,
                selected_agent_types = selected_agent_types
            )

        elif step == 3:
            selected_agents = request.form.getlist('agent_types')
            experiment_type = request.form['experiment_type']
            experiment_params = ComputeExperimentTypeModel.objects.get(experiment_type=experiment_type).experiment_params
            agent_types = AgentTypeModel.objects.all()
            selected_agent_types = zip(agent_types, selected_agents)
            params_result = {
                param: request.form[param] for param in experiment_params
            }
            if experiment_type == '_erc20_token':

                erc20_token_world = ERC20TokenWorld(
                    float(params_result['AgentRadio']),
                    int(params_result['AgentNumber']),
                    int(params_result['IterNumbers']),
                )
                world_id = erc20_token_world.unique_id
                max_step = int(params_result['IterNumbers']) - 1
                erc20_token_world.run()
            else:
                pass
            return render_template(
                'config_3.html',
                experiment_type = experiment_type,
                experiment_params = experiment_params,
                agent_types = agent_types,
                selected_agents = selected_agents,
                selected_agent_types = selected_agent_types,
                params_result = params_result,
                world_id = world_id,
                max_step = max_step
            )

    else:
        if step == 0:
            experiment_types = ComputeExperimentTypeModel.objects.all()
            return render_template('config_0.html', experiment_types=experiment_types)

@home_bp.route("/tokens/<max_step>/<world_id>", methods=["GET", "POST"])
def token_data(max_step, world_id):
    c = token_discribute(max_step, world_id)
    return c.dump_options_with_quotes()

@home_bp.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()

@home_bp.route("/bar")
def get_bar_index():
    return render_template("bart.html")
