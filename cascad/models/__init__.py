from mongoengine import connect, Document, StringField, DictField, ListField, DateTimeField
# from settings import MONGO_DB, MONGO_HOST, MONGO_PORT
from cascad.settings import MONGO_DB, MONGO_HOST, MONGO_PORT

connect(alias='cascad', db=MONGO_DB, host=MONGO_HOST, port=MONGO_PORT)

def init_db(): 
    connect(alias='cascad', db=MONGO_DB, host=MONGO_HOST, port=MONGO_PORT)