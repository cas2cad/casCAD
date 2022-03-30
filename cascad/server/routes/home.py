from flask import Blueprint, render_template, url_for, request
from cascad.models.datamodel import AgentTypeModel, ComputeExperimentModel, ComputeExperimentTypeModel

home_bp = Blueprint('home_bp', __name__)


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

            return render_template(
                'config_3.html',
                experiment_type = experiment_type,
                experiment_params = experiment_params,
                agent_types = agent_types,
                selected_agents = selected_agents,
                selected_agent_types = selected_agent_types,
                params_result = params_result
            )

    else:
        if step == 0:
            experiment_types = ComputeExperimentTypeModel.objects.all()
            return render_template('config_0.html', experiment_types=experiment_types)
        elif step == 1:

            pass