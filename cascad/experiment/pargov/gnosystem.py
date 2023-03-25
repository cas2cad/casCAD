# from aletheia.scenario_generator.timeline import TimeLine
# from cascad.experiment.pargov.timeline import  TimeLine
from cascad.aritificial_world.timeline import TimeLine
from numpy.lib.arraysetops import isin
from cascad.experiment.pargov.constant import DUET, DUET_USDT, FARM, FRAMWITHDRAW, MINT1, NO_TOKEN, REDEEM, STAKE, STAKEWITHDRAW, SWAP1, VOTE_CONDITION, VOTE_YES, YES_TOKEN, ZBTC_ZUSD, ZNAS, ZNAS_ZUSD, ZUSD_USDT, USDT, GNO, DAI, VOTE_NO
# from pargov.Omen import  Omen
from cascad.experiment.pargov.Omen import Omen

class ArtificalSystem(object):
    pass


class DuetSystem(ArtificalSystem):

    def __init__(self, states={}):
        self.states = states

    def mint(self):
        pass

# gip3 81 GNO   5000 DAI

#gip1  70 GNO        5050 DAI

class Proposal:
    def __init__(self, _id, start_time, _type):
        self._id = _id
        # self.accept_token = accept_token
        self.dura_time = 0
        self.start_time = start_time
        self.passed = False
        self.states = {
            VOTE_YES: [],
            VOTE_NO : []
        }
        self.last_time = 7
        self.activate = True
        self._type = _type

    def vote_yes(self, agent):
        agent.states[VOTE_CONDITION] = VOTE_YES
        self.states[VOTE_YES].append((agent.unique_id, agent.states[GNO]))

    def vote_no(self, agent):
        agent.states[VOTE_CONDITION] = VOTE_NO
        self.states[VOTE_NO].append((agent.unique_id, agent.states[GNO]))

    def count_result(self):
        yes_token = 0.1
        no_token = 0.1
        for votes in self.states[VOTE_YES]:
            yes_token += votes[1]

        for votes in self.states[VOTE_NO]:
            no_token += votes[1]

        if yes_token >= no_token:
            return True
        else:
            return False

    def step(self):
        self.dura_time += 1
        if self.dura_time >= self.last_time:
            self.passed = self.count_result()
            self.activate = False


class GNOSystem(ArtificalSystem):
    def __init__(self, timeline: TimeLine) -> None:
        self.timeline = timeline
        self.omen = Omen()
        # self.vote_system = VoteSystem()
        self.activate_proposals = []
        self.finished_proposals = []
        
    def initlize(self):
        pass

    def submit(self, _id, _type):
        proposal = Proposal(_id, self.timeline.tick, _type)
        self.omen.add_proposal(_id, 80, 80, GNO)
        self.omen.add_proposal(_id, 5000, 5000, DAI)
        self.activate_proposals.append(proposal)

    def buy(self, agent, proposal_id, token_type, amount, accept_token):
        self.omen.buy(agent, proposal_id, token_type, amount, accept_token)

    def sell(self, agent, proposal_id, token_type, amount, accept_token):
        self.omen.sell(agent, proposal_id, token_type, amount, accept_token)

    def vote_yes(self, agent,  proposal_id):
        # self.vote_system.vote_yes(agent)
        target: Proposal = None
        for proposal in self.activate_proposals:
            if proposal._id == proposal_id:
                target = proposal
        target.vote_yes(agent)

    def vote_no(self, agent, proposal_id):
        target: Proposal = None
        for proposal in self.activate_proposals:
            if proposal._id == proposal_id:
                target = proposal
        target.vote_no(agent)

    def get_proposal_by_id(self, proposal_id):
        for proposal in self.activate_proposals:
            if proposal._id == proposal_id:
                return proposal
        for proposal in self.finished_proposals:
            if proposal._id == proposal_id:
                return proposal

    def get_token_price(self, proposal_id, token_type, accept_token, only_number=False):
        proposal = self.get_proposal_by_id(proposal_id)
        if proposal.activate or only_number:
            return self.omen.get_price(proposal_id, token_type, accept_token)
        else:
            if (proposal.passed and token_type == YES_TOKEN) or (not proposal.passed and token_type == NO_TOKEN):
                return 1
            else:
                return 0
            

    def step(self):
        need_to_remove = []
        for proposal in self.activate_proposals:
            proposal.step()
            if not proposal.activate:
                need_to_remove.append(proposal)

        for proposal in need_to_remove:
            self.activate_proposals.remove(proposal)
            self.finished_proposals.append(proposal)
