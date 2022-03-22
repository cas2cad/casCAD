from typing_extensions import Required
import datetime
import copy
from mongoengine import connect, Document, StringField, DictField, ListField, DateTimeField, IntField
from cascad.settings import MONGO_DB, MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PWD

# connect(MONGO_DB, username=MONGO_USER, password=MONGO_PWD, host=MONGO_HOST, port=MONGO_PORT)
connect(MONGO_DB, port=MONGO_PORT)

class AgentModel(Document):
    unique_id = StringField(required=True, primary_key=True)
    step = IntField()
    creation_date = DateTimeField(default=datetime.datetime.now())
    modified_date = DateTimeField(default=datetime.datetime.now())
    state = DictField()
    state_history = ListField(DictField(), default=[])

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        tmp_state = copy.deepcopy(self.state)
        ## add the step infor
        tmp_state['step'] = self.step
        self.state_history.append(tmp_state)
        
        self.modified_date = datetime.datetime.now()
        return super(AgentModel, self).save(*args, **kwargs)
