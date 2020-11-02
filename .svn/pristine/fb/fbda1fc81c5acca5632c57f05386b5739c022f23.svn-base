from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSON

from . import db
import datetime
import sqlalchemy_jsonfield
from marshmallow import fields, Schema

class NodeModel(db.Model):

    __tablename__ = 'flow_node'
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('flow_workflow.id'), nullable=False)
    #workflow = db.ForeignKey(Workflow, null=True, on_delete=db.CASCADE)
    node_id = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False,default='Active')
    data = db.Column(JSON)
    parent = db.Column(db.String(64),default='')
    # data = db.Column(sqlalchemy_jsonfield.JSONField(enforce_string=False,enforce_unicode=False))
    #data = db.Column(MutableDict.as_mutable(HSTORE))
    #db.Column(JSON)  # JSONField(null=False,default=dict)

    def __init__(self, item):
        """
        Class constructor
        """
        self.node_id = item.get('node_id')
        self.type = item.get('type')
        self.status = item.get('status')
        self.data = item.get('data')
        self.workflow_id = item.get('workflow')
        self.parent = item.get('parent')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        #self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_blogposts():
        return NodeModel.query.all()

    @staticmethod
    def get_one_blogpost(id):
        return NodeModel.query.get(id)

    def __str__(self):
        return self.node_id


class NodeSchema(Schema):
  """
  Node Schema
  """

  class Meta:
      fields = ("id", "node_id", "type", "status","data","workflow_id","parent")

  id = fields.Int(dump_only=True)
  node_id = fields.Str(required=True)
  type = fields.Str(required=True)
  status = fields.Str(required=True)
  data = fields.Raw(required=False)
  workflow_id = fields.Int(dump_only=True)
  parent = fields.Str(dump_only=True)
