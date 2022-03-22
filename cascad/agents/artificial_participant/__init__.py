from  cascad.agents import  Agent

class Participant(Agent):
    """Base calss for particpant agent.

    Args:
        unique_id (int): The unique identifier for the agent
        world (World): the world this agent belongs to
    """

    def observe(self): 
        """sensor of an agent
        """
        pass

    def think(self):
        """or planner, here agent make decision with the observed knowledge
        """
        pass

    def takeActions(self):
        """Effect the environment
        """
        pass

    def step(self):
        self.observe()
        self.think()
        self.takeActions()
        pass