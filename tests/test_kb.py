import sys
import os
sys.path.append('..')
sys.path.append('.')
import unittest
from cascad.models.kb import Things, Entity, Property
from rdflib import Literal

class TestAgent(unittest.TestCase):
    def setUp(self):
        pass

    def test_entity_assign(self):
        entity = Entity('id', 'entity1')
        property = Property('id1', 'property1')
        entity[property] = 'value1'
        assert entity[property][0].toPython() == 'value1'
        del entity[property]
        assert entity[property] == []

    def test_update_entity(self):
        entity = Entity('id', 'entity1')
        property = Property('id1', 'property1')
        del entity[property]
        entity[property] = 'value1'
        assert entity[property][0].toPython() == 'value1'
        entity[property] = 'value2'
        result = [value.toPython() for value in entity[property]]
        assert 'value2' in result
        # assert entity[property][0].toPython() == 'value2' and len(entity[property]) == 2
        # del entity[property]

    def test_multiple_entity(self):
        entity = Entity('id', 'entity1')
        property = Property('id1', 'has_entity')
        entity2 = Entity('id3', 'entity2')
        entity3 = Entity('id4', 'eneity3')
        entity[property] = entity2
        entity[property] = entity3
        print(entity[property])

    def test_keys(self): 
        entity = Entity('id', 'entity1')
        property = Property('id1', 'has_entity')
        entity2 = Entity('id3', 'entity2')
        entity3 = Entity('id4', 'eneity3')
        entity[property] = entity2
        entity[property] = entity3
        print(entity.keys())

    def test_delete_key(self):
        entity = Entity('id', 'entity1')
        property = Property('id1', 'has_entity')
        entity2 = Entity('id3', 'entity2')
        entity[property] = entity2
        entity.delete(property, entity2)
        assert entity2 in entity[property]

if __name__ == '__main__':
    unittest.main()
    pass