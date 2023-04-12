from email.policy import default
import datetime
import copy
from mongoengine import connect, Document, StringField, DictField, ListField, DateTimeField, IntField, FloatField, \
    BooleanField
from cascad.settings import MONGO_DB, MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PWD

# connect(MONGO_DB, username=MONGO_USER, password=MONGO_PWD, host=MONGO_HOST, port=MONGO_PORT)
connect(MONGO_DB, port=MONGO_PORT)


class BaseModel(Document):
    unique_id = StringField(required=True, primary_key=True)
    creation_date = DateTimeField(default=datetime.datetime.now())
    modified_date = DateTimeField(default=datetime.datetime.now())
    meta = {'abstract': True}


class AgentTypeModel(Document):
    unique_id = StringField(required=True, primary_key=True)
    agent_name = StringField()
    agent_params = ListField(StringField(), default=[])
    agent_describe = StringField()
    corresponding_experiment = StringField()


class ComponentTypeModel(Document):
    unique_id = StringField(required=True, primary_key=True)
    component_name = StringField()
    component_params = ListField(StringField(), default=[])
    component_describe = StringField()
    corresponding_experiment = StringField()


class ComputeExperimentTypeModel(Document):
    unique_id = StringField(required=True, primary_key=True)
    experiment_type = StringField()
    experiment_name = StringField()
    experiment_describe = StringField()
    experiment_params = ListField(StringField(), default=[])


class ComputeExperimentModel(BaseModel):
    unique_id = StringField(required=True, unique=True)
    experiment_name = StringField()
    status = StringField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()
        return super(ComputeExperimentModel, self).save(*args, **kwargs)


class AgentModel(Document):
    unique_id = StringField(required=True, primary_key=True)
    world_id = StringField()
    agent_id = StringField()
    step = IntField()
    creation_date = DateTimeField(default=datetime.datetime.now())
    modified_date = DateTimeField(default=datetime.datetime.now())
    state = DictField()

    # state_history = ListField(DictField(), default=[])

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        tmp_state = copy.deepcopy(self.state)
        ## add the step infor
        tmp_state['step'] = self.step
        # self.state_history.append(tmp_state)

        self.modified_date = datetime.datetime.now()
        return super(AgentModel, self).save(*args, **kwargs)


class AMMCreated(Document):
    pass


class TransferModel(BaseModel):
    unique_id = StringField(required=True, primary_key=True)
    action_name = StringField(default="Transfer")
    sender = StringField()
    recipient = StringField()
    amount = FloatField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()
        return super(TransferModel, self).save(*args, **kwargs)


class ApprovelModel(BaseModel):
    unique_id = StringField(required=True, primary_key=True)
    owner = StringField()
    spender = StringField()
    amount = FloatField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()
        return super(ApprovelModel, self).save(*args, **kwargs)


class ConditionPreparationModel(BaseModel):
    unique_id = StringField(required=True, primary_key=True)
    conditionId = StringField()
    oracle = StringField()
    questionId = StringField()
    outcomeSlotCount = IntField()
    questionTitle = StringField()
    questionType = StringField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()
        return super(ConditionPreparationModel, self).save(*args, **kwargs)


class ConditionResolutionModel(BaseModel):
    unique_id = StringField(required=True, primary_key=True)
    conditionId = StringField()
    oracle = StringField()
    questionId = StringField()
    outcomeSlotCount = IntField()
    payoutNumerators = ListField()

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()
        return super(ConditionPreparationModel, self).save(*args, **kwargs)


class WorldModel(BaseModel):
    pass


class TransferSingleModel(BaseModel):
    operator = StringField()
    _from = StringField()
    to = StringField()
    id = StringField()
    value = IntField()


class TransferBatchModel(BaseModel):
    operator = StringField()
    _from = StringField()
    to = StringField()
    ids = ListField()
    values = ListField()


class ApprovalForAllModel(BaseModel):
    owner = StringField()
    operator = StringField()
    approved = BooleanField()


class URIModel(BaseModel):
    value = StringField()
    id = IntField()


class PositionSplitModel(BaseModel):
    stakeholder = StringField()

    pass


class ExperimentResultModel(Document):
    # unique_id = StringField(required=True, primary_key=True)
    experiment_id = StringField()
    day = IntField()
    result = ListField()
    code = ListField()


class GeneResultModel(Document):
    # unique_id = StringField(required=True, primary_key=True)
    geneId = StringField()
    experiment_id = StringField()
    result = ListField()
    code = ListField()
    loss = ListField()
    iter = IntField()


class GeneResultModelRound2(Document):
    # unique_id = StringField(required=True, primary_key=True)
    geneId = StringField()
    result = ListField()
    code = ListField()
    loss = ListField()
    iter = IntField()


class GeneResultModelRound0(Document):
    # unique_id = StringField(required=True, primary_key=True)
    geneId = StringField()
    experiment_id = StringField()
    result = ListField()
    code = ListField()
    loss = ListField()
    iter = IntField()
