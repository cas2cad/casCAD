import sys
import os
sys.path.append('..')
sys.path.append('.')
import unittest
# from cascad.models.kb import Things, Entity, Property
from cascad.models.neo4jbase import Neo4j

class TestNeo4j(unittest.TestCase):
    def setUp(self):
        self.neo4j = Neo4j(
            "neo4j://localhost:7687",
            "neo4j",
            "neo4j",
            "rem8271206",
            "http://cascad/test"
        )

    def test_add_trip(self): 
        self.neo4j.add_triple(
            "test1", "isA", "testType"
        )
        print(self.neo4j.get_object("test1", "isA"))
        self.neo4j.remove_triple(
            "test1", "isA"
        )
    
    def test_add_property(self):
        pass

if __name__ == '__main__':
    unittest.main()
    pass