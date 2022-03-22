from cascad.settings import BASE_IRI, NEO4J_URI, NEO4J_DATABASE, NEO4J_USER, NEO4J_PWD
from collections.abc import MutableMapping
from cascad.settings import RDF_STORE
from cascad.utils.myfuncs import switch
from cascad.models.neo4jbase import  Neo4j
from datetime import datetime


rdf_store = None
for case in switch(RDF_STORE): 
    if case('neo4j'):
        rdf_store = Neo4j(NEO4J_URI, NEO4J_DATABASE, NEO4J_USER, NEO4J_PWD, BASE_IRI)
        break

    if case():
        rdf_store = Neo4j()
        break


class Things(dict):
    """the Base class for the knowlege model.

    Args:
        dict ([type]): [description]
    """
    ontoName = 'Thing'
    iri_base = BASE_IRI + ontoName

    def __init__(self, unique_id, name):
        self.is_a = [self.iri_base]
        self.iri = self.iri_base + '#' + str(unique_id)
        self.unique_id = unique_id
        self.name = name
        self.store = dict()
        self.allowDot()

    def __getitem__ (self, key):
        print('executed')
        return self.store.get(key)

    def __setitem__ (self, key, value):
        self.store[key] = value

    def allowDot(self, value=True):
        if value:
            self.__setattr__ = self.__setitem__
            self.__getattr__ = self.__getitem__
        else:
            del self.__setattr__
            del self.__getattr__
        
    def __eq__ (self, other):
        if isinstance(other, self.__class__) and self.iri == other.iri:
            return True
        else:
            return False


class Entity(Things):
    ontoName = 'Entity'
    iri_base = BASE_IRI + ontoName

    def __setitem__(self, key, value):
        """Set a value of a property

        Args:
            key (Property): Link name
            value (Value): The property value
        """
        if isinstance(key, Property):
            key = key.iri

        if value is None: 
            raise ValueError("The value could not be None")
            
        if type(value)  == dict:
            raise ValueError("Dict value type is not supported")

        if type(value) in [int, str, float, datetime]:
            rdf_store.add_literal(self.iri, key, value)
        elif type(value) == list:
            for item in value:
                rdf_store.add_literal(self.iri, key, item)
        elif isinstance(value, Entity):
            # rdf_store.add_link(self.iri, key, value.iri)
            rdf_store.add_triple(self.iri, key, value.iri)
        else: 
            raise ValueError("Unknown value type")
        # super(Entity, self).__setitem__(key, value)

    def __getitem__(self, key):
        """Get the values of a property

        Args:
            key (Property): Link name
            value (Value): The property value
        """
        if isinstance(key, Property):
            key = key.iri

        return rdf_store.get_object(self.iri, key)
    
    def __delitem__(self, key):
        """Delete a property

        Args:
            key ([type]): [description]
        """
        if isinstance(key, Property):
            key = key.iri

        return rdf_store.remove_triple(self.iri, key)

    def delete(self, key, value):
        if isinstance(key, Property):
            key = key.iri

        if value is None: 
            raise ValueError("The value could not be None")
            
        if type(value)  == dict:
            raise ValueError("Dict value type is not supported")

        if type(value) in [int, str, float, datetime]:
            rdf_store.remove_triple(self.iri, key, value)
        elif isinstance(value, Entity):
            # rdf_store.add_link(self.iri, key, value.iri)
            rdf_store.remove_triple(self.iri, key, value.iri)
        else: 
            raise ValueError("Unknown value type")

    def keys(self):
        result = rdf_store.get_predicate_object(self.iri)
        return list(set([item[0] for item in result]))

class Property(Things):
    ontoName = 'Property'
    iri_base = BASE_IRI + ontoName
            