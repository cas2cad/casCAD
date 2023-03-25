from flask import Blueprint, render_template, url_for, request
from cascad.models.datamodel import AgentTypeModel, ComputeExperimentModel, ComputeExperimentTypeModel, AgentModel,GeneResultModel,ExperimentResultModel, ComponentModel
from pyecharts import options as opts
from pyecharts.charts import Bar, Scatter
from jinja2 import Markup
from cascad.experiment.token_sender import ERC20TokenWorld
from cascad.experiment.MBM.exp import  GA as MBMExperiment
from collections import defaultdict

home_bp = Blueprint('home_bp', __name__ , template_folder='templates', static_folder='static')

def token_discribute(max_step, world_id) ->  Scatter:
    # agent_models = AgentModel.objects(step=max_step, world_id=world_id)
    generesult_models = ExperimentResultModel.objects(experiment_id = world_id)
    result = [
            (agent_model.day, agent_model.result[0]) for agent_model in generesult_models 
    ]

    c = (
        Scatter()
        .add_xaxis([x[0] for x in result])
        .add_yaxis("Loss", [x[1] for x in result])
        .set_global_opts(title_opts=opts.TitleOpts(title="Avg Loss Over Time"))
    )
    return c

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@home_bp.route("/compute_experiment", methods=['GET', 'POST'])
@home_bp.route("/compute_experiment/<page>", methods=['GET', 'POST'])
def compute(page=0):
    page = int(page)
    if page == 0:
        experiments = ComputeExperimentModel.objects.limit(5)
    else:
        experiments = ComputeExperimentModel.objects.skip(page * 5).limit(5)
    return render_template('compute_experiment.html', experiments=experiments, page=page)

@home_bp.route("/agents", methods=['GET', 'POST'])
@home_bp.route("/agents/<agent_name>", methods=['GET', 'POST'])
def agent(agent_name=None):
    # if request.method == 'POST':
    #     agent_type = request.form['agent_type']

    # else:
    if not agent_name:
        agents = AgentTypeModel.objects.all()
        return render_template('agent.html', agents=agents)
    else:
        agent = AgentTypeModel.objects(agent_name=agent_name).first()
        return render_template('agent_detail.html', agent=agent)


@home_bp.route("/components", methods=['GET', 'POST'])
@home_bp.route("/components/<component_name>", methods=['GET', 'POST'])
def component(agent_name=None):
    # if request.method == 'POST':
    #     agent_type = request.form['agent_type']

    # else:
    if not agent_name:
        components = ComponentModel.objects.all()
        return render_template('components.html', compoents=components)
    # else:
    #     agent = ComponentModel.objects(agent_name=agent_name).first()
    #     return render_template('agent_detail.html', agent=agent)


@home_bp.route("/examples", methods=['GET', 'POST'])
def use_cases():
    return render_template('comming_soon.html')

@home_bp.route("/config_experiment", methods=["GET", "POST"])
@home_bp.route("/config_experiment/<step>", methods=["GET", "POST"])
def config_experiment(step=0):
    step = int(step)
    if request.method == 'POST':
        experiment_type = request.form['experiment_type']
        if step == 1:
            agent_types = AgentTypeModel.objects(corresponding_experiment = experiment_type)
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
            elif experiment_type == '_mbm_experiment':
                experiment = MBMExperiment(popsize = int(params_result['popsize']), ngen=int(params_result['ngen']))
                # while experiment.running:
                    # experiment.step() 
                experiment.start()
                world_id = experiment.unique_id
                max_step = experiment.ngen
            elif experiment_type == '_pargov_experiment':
                pass
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

# @home_bp.route("/barChart")
# def get_bar_chart():
#     c = bar_base()
#     return c.dump_options_with_quotes()

@home_bp.route("/bar")
def get_bar_index():
    return render_template("bart.html")

@home_bp.route("/view_result/<experiment_id>")
def view_result(experiment_id):
    

    pass