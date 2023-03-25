"""
CASCAD Neo4j Base
=================
Objects for handling the interact with a neo4j database, based on rdflib package.
In particular, this module contains interact method include:
get nodes, get properties, add nodes, add properties
"""

import rdflib
from rdflib import Graph, Literal, RDF, URIRef, store
from rdflib.namespace import FOAF, XSD
from cascad.utils.myfuncs import Singleton
from threading import  Lock

class Neo4j(metaclass=Singleton): 
    lock = Lock()

    def __init__(self, uri, database, user, pwd, base=None):
        theconfig = {
            'uri': uri,
            'database': database,
            'auth': {
                'user': user,
                'pwd': pwd
            }
        }

        # self.g = Graph(store='Neo4')
        self.g = Graph(store='neo4j-cypher')
        # g = Graph(store='neo4j-cypher')

        self.g.open(theconfig, create=False)
        self.base = base

    def process_iri(self, iri):
        """Add prefix to the uri if needed.

        Args:
            uri ([string]): iri
        """

        if not iri.startswith(self.base):
            if self.base.endswith('/'):
                iri = self.base + iri
            else: 
                iri = self.base + '/' + iri
        return iri
       
    def remove_triple(self, node1_iri, property_iri, node2_iri=None):
        """Remove a triple from the rdf graph

        Args:
            node1_iri ([str]): the iri(Internationalized Resource Identifie) of the subject node
            property_iri ([str]): the iri(Internationalized Resource Identifie) of the property
            node2_iri ([str]): the iri(Internationalized Resource Identifie) of the object node
        """
        node1 = URIRef(self.process_iri(node1_iri))
        property = URIRef(self.process_iri(property_iri))
        if node2_iri is not None:
            node2 = URIRef(self.process_iri(node2_iri))
            self.g.remove((node1, property, node2))
        else: 
            self.g.remove((node1, property, None))

    def add_triple(self, node1_iri, property_iri, node2_iri):
        """Add a triple to the rdf graph, the object should be a node

        Args:
            node1_iri ([str]): the iri(Internationalized Resource Identifie) of the subject node
            property_iri ([str]): the iri(Internationalized Resource Identifie) of the property
            node2_iri ([str]): the iri(Internationalized Resource Identifie) of the object node
        """

        node1 = URIRef(self.process_iri(node1_iri))
        property = URIRef(self.process_iri(property_iri))
        node2 = URIRef(self.process_iri(node2_iri))
        self.g.add((node1, property, node2))

    def add_literal(self, node1_iri, property_iri, literal): 
        """Add a triple to the rdf graph, the object should be a literal

        Args:
            node1_iri ([str]): the iri(Internationalized Resource Identifie) of the subject node
            property_iri ([str]): the iri(Internationalized Resource Identifie) of the property
            literal ([str]): the target value of a triple
        """

        node1 = URIRef(self.process_iri(node1_iri))
        property = URIRef(self.process_iri(property_iri))
        literal = Literal(literal)
        self.g.add((node1, property, literal))

    def get_object(self, node1_iri, property_iri):
        """Get the object nodes/literals with object and property

        Args:
            node1_iri ([type]): [description]
            property_iri ([type]): [description]

        Returns:
            [list]: [a list of target objects, with the form of resource iri]
        """
        node1 = URIRef(self.process_iri(node1_iri))
        property = URIRef(self.process_iri(property_iri))
        result = self.g.objects(node1, property)
        return list(result)

    def get_predicate_object(self, node1_iri):
        """Get the predicates and subjects 

        Args:
            node1_iri ([Entity]): iri of the object

        Returns:
            [list]: [a list of the target predict and subjects]
        """
        node1 = URIRef(self.process_iri(node1_iri))
        result = self.g.predicate_objects(node1)
        return list(result)

# # create a neo4j backed Graph
# g = rdflib.Graph(store='Neo4j')

# # set the configuration to connect to your Neo4j DB 
# theconfig = {'uri': "neo4j://localhost:7687", 'database': 'neo4j', 'auth': {'user': "neo4j", 'pwd': "rem8271206"}}

# g.open(theconfig, create = False)

# donna = URIRef("http://example.org/donna")

# # Add triples using store's add() method.
# g.add((donna, RDF.type, FOAF.Person))
# g.add((donna, FOAF.nick, Literal("donna", lang="en")))
# g.add((donna, FOAF.name, Literal("Donna Fales")))
# g.add((donna, FOAF.mbox, URIRef("mailto:donna@example.org")))

# # g.load("https://raw.githubusercontent.com/jbarrasa/datasets/master/rdf/music.nt", format="nt")

# # For each foaf:Person in the store, print out their mbox property's value.

# print("--- printing band's names ---")
# for band in g.subjects(rdflib.RDF.type, rdflib.URIRef("http://neo4j.com/voc/music#Band")):
#     for bandName in g.objects(band, rdflib.URIRef("http://neo4j.com/voc/music#name")):
#         print(bandName)
