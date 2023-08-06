from random import randint

from uuid import uuid4

from typing import List

from pydantic import BaseModel
from tracardi_plugin_sdk.domain.register import Plugin


class Position(BaseModel):
    x: int
    y: int


class SimplifiedSpec(BaseModel):
    module: str


class EdgeBundle:
    def __init__(self, source, edge, target):
        self.source = source
        self.edge = edge
        self.target = target

    def __repr__(self):
        return "EdgeBundle(source={}, edge=({}), target={}".format(self.source.id, self.edge, self.target.id)


class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: Plugin

    def __call__(self, *args) -> 'NodePort':
        if len(args) == 0:
            raise ValueError("Port is missing.")
        if len(args) != 1:
            raise ValueError("Only one port is allowed.")
        return NodePort(node=self, port=args[0])

    def __rshift__(self, other):
        raise ValueError(
            "You can not connect with edge nodes. Only node ports can be connected. Use parentis to indicate node.")


class NodePort:
    def __init__(self, port: str, node: Node):
        self.node = node
        self.port = port

    def __rshift__(self, node_port: 'NodePort') -> EdgeBundle:

        node_port.node.position.y += randint(0, 500)
        node_port.node.position.x += randint(0, 500)

        edge = Edge(
            id=str(uuid4()),
            type="default",
            source=self.node.id,
            target=node_port.node.id,
            sourceHandle=self.port,
            targetHandle=node_port.port
        )
        return EdgeBundle(
            source=self.node,
            edge=edge,
            target=node_port.node
        )

class Edge(BaseModel):
    source: str
    sourceHandle: str
    target: str
    targetHandle: str
    id: str
    type: str


class FlowGraphData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

    def __add__(self, node: Node):
        self.nodes.append(node)
