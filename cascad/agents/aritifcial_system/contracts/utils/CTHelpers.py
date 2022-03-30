import hashlib
import math

P = 21888242871839275222246405745257275088696311157297823662689037894645226208583
B = 3

class CTHelpers:

    @staticmethod
    def getConditionId(cls, oracle, qustionId, outcomeSlotCount):
        m = hashlib.md5()
        m.update(oracle)
        m.update(qustionId)
        m.update(outcomeSlotCount)
        return m.hexdigest()

    @staticmethod
    def getPositionId(cls, collateralToken, collectionId):
        m = hashlib.md5()
        m.update(collateralToken)
        m.update(collectionId)
        return m.hexdigest()

    @staticmethod
    def encodePacked(cls, *args):
        m = hashlib.md5()
        for n in args:
            m.update(n)
        return m.hexdigest()

    @staticmethod       
    def getCollectionId(cls, parentCollectionId, conditionId, indexSet):
        x1 = cls.encodePacked(conditionId, indexSet)
        odd = x1 >> 255 != 0
        
        x1 = (x1 + 1) % P
        yy = (((x1 * x1 % P) * x1 % P ) + B ) % P
        y1 = math.sqrt(yy)

        while y1 * y1 % P  != yy:
            if (odd and y1 % 2 == 0) or ((not odd) and y1 % 2 == 1):
                y1 = P - y1

