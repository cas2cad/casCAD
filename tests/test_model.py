import sys
import os
sys.path.append('..')
sys.path.append('.')
import unittest
from cascad.models.datamodel import AgentModel

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

    
if __name__ == '__main__':
    unittest.main()