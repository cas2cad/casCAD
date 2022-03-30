from cascad.agents.aritifcial_system.contracts.token.ERC20 import ERC20
from cascad.agents.aritifcial_system.contracts.token.ERC1155 import ERC1155
from cascad.agents.aritifcial_system.contracts.utils.CTHelpers import CTHelpers
from cascad.models.datamodel import ConditionPreparationModel, ConditionResolutionModel
import uuid


class ConditionalTokens(ERC1155):
    payoutNumerators = {}
    payoutDenominator = {}

    def prepareCondition(self, oracle, questionId, outcomeSlotCount, questionTitle, questionType, caller=None):
        assert outcomeSlotCount <= 256, "too many outcome slots"
        assert outcomeSlotCount > 1, "there should be more than one outcome slot"
        conditionId = CTHelpers.getConditionId(oracle, questionId, outcomeSlotCount)
        assert conditionId not in self.payoutNumerators.keys(), "condition already prepared"
        self.payoutNumerators[conditionId] = []
        ConditionPreparationModel(
            unique_id=uuid.uuid4().hex,
            conditionId = conditionId,
            oracle = oracle,
            questionId = questionId,
            outcomeSlotCount = outcomeSlotCount,
            questionTitle=questionTitle,
            questionType = questionType
            ).save()

    def reportPayouts(self, questionId, payouts, caller=None):
        outcomeSlotCount = len(payouts)
        assert outcomeSlotCount > 1, "there should be more than one outcomeslot"
        conditionId = CTHelpers.getConditionId(caller, questionId, outcomeSlotCount)

        assert len(self.payoutNumerators[conditionId]) == outcomeSlotCount, "condition not prepared or found"

        assert self.payoutDenominator[conditionId] == 0, "payout denominator already set"

        den: int = 0

        for i in range(0, outcomeSlotCount):
            num = payouts[i]
            den = den + num

            assert self.payoutNumerators[conditionId][i] == 0, "payout numerator already set"
            self.payoutNumerators[conditionId][i] = num

        assert den > 0, "payout is all zeroes"
        ConditionResolutionModel(
            conditionId = conditionId,
            oracle = caller,
            questionId = questionId,
            outcomeSlotCount = outcomeSlotCount,
            pyaoutNumerator = self.payoutNumerators[conditionId]
        ).save()

    def splitPosition(self, collateralToken, parentCollectionId, conditionId, partition, amount, caller=None):
        assert len(partition) > 1, "got empty or singleton partition"

        outcomeSlotCount = len(self.payoutNumerators[conditionId])

        assert outcomeSlotCount > 0, "condition not prepared yet"

        fullIndexSet = (1 << outcomeSlotCount) - 1
        freeIndexSet = fullIndexSet

        positionIds = []
        amounts = []
        for i in range(0, len(partition)):
            indexSet = partition[i]
            assert indexSet >0 and indexSet < fullIndexSet, "got invalid index set"

            assert (indexSet & freeIndexSet) == indexSet, "partition not disjoint"

            freeIndexSet ^= indexSet