import sys
import os
sys.path.append('..')
sys.path.append('.')
import unittest
from cascad.models.datamodel import AgentModel, TransferModel, ApprovelModel, AgentTypeModel, ComputeExperimentModel, ComputeExperimentTypeModel

from cascad.agents.aritifcial_system.chain import ChainBase
from cascad.agents.aritifcial_system.contracts.token.ERC20 import  ERC20

class TestModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_save(self): 
        agentModel = AgentModel(
            unique_id="01",
            step=1,
            state={'step': 1}
        )
        agentModel.save()

        agents = AgentModel.objects(unique_id="01")
        for agent in agents:
            print(agent.unique_id)

        transfer = TransferModel(
            unique_id="002",
            sender = "0x111",
            recipient="0x222",
            amount = 1)
        transfer.save()

        approval = ApprovelModel(
            unique_id="003",
            owner="0x111",
            spender="0x333",
            amount=1.1
        )
        approval.save()
            
    def test_erc20(self):
        c = ChainBase()
        address = c.add_contract(ERC20())
        print(address)

    def test_agentType(self):
        agent = AgentTypeModel(
            unique_id="003",
            agent_name="Zero_Intelligent_Agent",
            agent_params = ['ActionProb'],
            agent_describe = "Zero Intelligent Agent is a kind of agent, who didn't consider the environment, only make decision follow a rule.",
            corresponding_experiment = "_erc20_token_repeat"
        )
        agent.save()

        agent = AgentTypeModel(
            unique_id="004",
            agent_name="Random_Action_Agent",
            agent_params = ['ActionProb'],
            agent_describe = "Random Action Agent is a kind of agent, who randomly take action.",
            corresponding_experiment = "_erc20_token_repeat"
        )
        agent.save()

    # def test_compute_model(self):
    #     compute_experiment = ComputeExperimentModel(
    #         unique_id = "005",
    #         experiment_name = "ERC20 代币实验",
    #         status = "Excuted",
    #     )
    #     compute_experiment.save()
    #     pass

    def test_experiment_type(self):
        experiment_type = ComputeExperimentTypeModel(
            unique_id = "007",
            experiment_type = "_erc20_token",
            experiment_name = "ERC20 Token Simulation",
            experiment_describe = "This is an example experiment of CASCAD",
            experiment_params= ['AgentRadio', 'AgentNumber', 'IterNumbers']
        )
        experiment_type.save()

    def test_agent_model(self):
        # agent_model = AgentModel(
        #     unique_id = "003",
        #     agent_id = "000001",
        #     step = 1,
        #     state = {"amount": 1000}
        # )
        # agent_model.save()
        agent_models = AgentModel.objects(step=9)
        result = [
            (str(agent_model.unique_id)[-4:], agent_model.state['token']) for agent_model in agent_models
        ]
        print(result)



if __name__ == '__main__':
    unittest.main()