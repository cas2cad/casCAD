"""
The agent class for cascad framework.

Core  Objects: Agent
"""

from cascad.models.datamodel import  AgentModel

class Agent:
    """Base class for all Agent object.

    Attributes:
        unique_id: an unique identifier of agent
        world: the world this agent belongs to
    
    """

    def __init__(self, unique_id: int, world) -> None:
        self.unique_id = unique_id
        self.world = world 
        self.state = {} # the agent
        self.state_history = []
        self.agentModel = AgentModel(unique_id=unique_id, state=self.state)
        pass

    def step(self) -> None:
        pass

    def save(self) -> None:
        # id, timestamp, step, state
        self.agentModel.step = self.system.step
        self.agentModel.state = self.state
        self.agentModel.save()

    @property
    def model(self):
        return self.agentModel