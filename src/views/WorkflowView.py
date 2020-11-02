import xml
from flask import request, json, Response, Blueprint, render_template
from ..models.WorkflowModel import WorkflowModel, WorkflowSchema
from ..models.NodeModel import NodeModel, NodeSchema
from flask import redirect

workflow_api = Blueprint('workflow_api', __name__)
workflow_schema = WorkflowSchema()
node_schema = NodeSchema()


@workflow_api.route('/', methods = ['GET'])
def get_all():
    flows = WorkflowModel.get_all_flows()
    # print('flows are',flows[0].nodes)
    # ser_flow = workflow_schema.dump(flows,many=True)

    parent = {}
    for item in flows:
        if item.flow_id == '0':
            parent[item.id] = item
            parent[item.id].children = []

    for child in flows:
        key = int(child.flow_id)
        if key in parent:
            print('parent found', parent[key])
            parent[key].children.append(child)
        # parent[key] = parentFlow

    for par in parent:
        print(parent[par], "::", parent[par].children)

    print('parent is ', parent)
    print('true')
    # ser_flow = workflow_schema.dump(parent, many=True)
    return render_template('flowt.html', data = parent)
# return custom_response(ser_flow, 200)


@workflow_api.route('/viewFlow/<int:id>')
def view(id):
    return render_template('flowt.html', mode = 'view', id = id)


@workflow_api.route('/editFlow/<int:id>')
def edit(id):
    wflow = WorkflowModel.get_flowbyId(id)
    flow_id = wflow.flow_id
    return render_template('base.html', mode = 'edit', id = id, flow_id = flow_id)


@workflow_api.route('/<int:id>', methods = ['GET'])
def getFlowByID(id):
    flow = WorkflowModel.get_flowbyId(id)
    print('flow is ', flow)
    if not flow:
        return custom_response({'error': 'Workflow not found'}, 404)

    ser_flow = workflow_schema.dump(flow)
    return custom_response(ser_flow, 200)


@workflow_api.route('/', methods = ['POST'])
def create():
    req_data = request.get_json()
    print(req_data)
    print('*****************')
    nodes = req_data.get("nodes")
    flow_id = req_data.get('flow_id')
    if (flow_id != '0'):
        wList = list(WorkflowModel.get_flowForVersion(flow_id))
        listLen = len(wList)
        # len will be 0 for the first version
        if (listLen == 0):
            wList = list(WorkflowModel.get_flowForId(flow_id))
            listLen = len(wList)
        if (listLen > 0):
            print("flow from order_by is ", wList[0].id)
            print("flow from order_by is ", wList[listLen - 1].id)
            version = int(wList[listLen - 1].version) + 1
            req_data['version'] = str(version)

    parent = ''

    for node in nodes[:]:
        child = node
        nodes.remove(node)
        item = {}
        item["node_id"] = child.get("node_id")
        item["type"] = child.get("type")
        item["status"] = child.get("status")
        item["data"] = child
        item["parent"] = parent
        node = NodeModel(item)
        nodes.append(node)
        nodeId = child.get("node_id")
        if ('circle' in nodeId) or ('diamond' in nodeId) or ('rect' in nodeId) or ('rrect' in nodeId):
            parent = nodeId
            print('parent is ', parent)

    print(req_data)

    workflowModel = WorkflowModel(req_data)
    workflowModel.save()
    print('in create method data is saved')
    return custom_response({'id': workflowModel.id}, 200)


@workflow_api.route('/addForm/<flowId>/<nodeId>')
def addForm(flowId, nodeId):
    return redirect('http://localhost:5001/api/v1/form/addForm/' + flowId + '/' + nodeId, code = 301)


def custom_response(res, status_code):
    """
  Custom Response Function
  """
    return Response(
        mimetype = "application/json",
        response = json.dumps(res),
        status = status_code
    )

#
# import json
#
# from lxml import etree
#
# # load input
# dom = etree.parse('data.xml')
# # load XSLT
# transform = etree.XSLT(etree.fromstring(xml))
#
# # apply XSLT on loaded dom
# json_text = str(transform(dom))
#
# # json_text contains the data converted to JSON format.
# # you can use it with the JSON API. Example:
# data = json.loads(json_text)
# print(data)