from . import Node
'''
loginNode = Node("/login")
orderNode = Node("/order")
decisionNode = Node("/decision")
a = Node("/a")
b = Node("/b")
c = Node("/c")
x = Node("/x")
y = Node("/y")
z = Node("/z")


flow1 = [loginNode,orderNode,decisionNode]
flow2 = [a,b,c]
flow3 = [x,y,z]

flow = {"flow1":flow1,"flow2":flow2,"flow3":flow3}
start = "flow1"

def executeFlow(flow):
    for n in flow:
        result = n.execute()
        if(n is isinstance(decision)):
            flowName = result.getflowName()
            executeFlow(flow[flowName])

executeFlow(flow[start])

'''
