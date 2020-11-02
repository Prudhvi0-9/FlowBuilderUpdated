from marshmallow import fields, Schema
import datetime
from . import db
from .NodeModel import NodeSchema
from sqlalchemy import desc

class WorkflowModel(db.Model):

    __tablename__ = 'flow_workflow'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(128), nullable=False)
    version =  db.Column(db.String(128), nullable=False,default='0')
    flow_id = db.Column(db.String(128), nullable=False,default='0')
    nodes = db.relationship('NodeModel', backref='WorkflowModel', lazy=True)
    data = db.Column(db.String())
    # definitions = db.column(db.String(128))
    children = []


    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.version = data.get('version')
        self.flow_id = data.get('flow_id')
        self.nodes = data.get('nodes')
        self.children = []


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_flows():
        return WorkflowModel.query.all()

    @staticmethod
    def get_flowbyId(id):
        return WorkflowModel.query.get(id)

    @staticmethod
    def get_flowForVersion(flowId):
        return WorkflowModel.query.filter_by(flow_id=flowId).order_by(desc(WorkflowModel.version))

    @staticmethod
    def get_flowForId(flowId):
        return WorkflowModel.query.filter_by(id=flowId).order_by(desc(WorkflowModel.version))

    # def __repr(self):
    #     return '<id {}>'.format(self.id)


class WorkflowSchema(Schema):
    """
    Workflow Schema
    """

    class Meta:
        fields = ("id", "name", "version", "flow_id", "nodes")

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    Phone = fields.Str(required = True)
    version = fields.Str(required=True)
    flow_id = fields.Str(required=True)
    nodes = fields.Nested(NodeSchema,many=True)
    # definitions = db.column(db.String(128))
    children = []
