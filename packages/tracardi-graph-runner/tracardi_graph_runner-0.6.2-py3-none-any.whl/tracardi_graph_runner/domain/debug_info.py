from typing import List, Dict
from pydantic import BaseModel

from tracardi_graph_runner.domain.debug_call_info import DebugCallInfo, Profiler
from tracardi_graph_runner.domain.entity import Entity
from tracardi_graph_runner.domain.error_debug_info import ErrorDebugInfo


class FlowDebugInfo(Entity):
    error: List[ErrorDebugInfo] = []


class DebugNodeInfo(BaseModel):
    id: str
    name: str = None
    sequenceNumber: int = None
    executionNumber: int = None
    calls: List[DebugCallInfo] = []
    profiler: Profiler


class DebugEdgeInfo(BaseModel):
    active: List[bool] = []


class DebugInfo(BaseModel):
    timestamp: float
    flow: FlowDebugInfo
    event: Entity
    nodes: Dict[str, DebugNodeInfo] = {}
    edges: Dict[str, DebugEdgeInfo] = {}

    def add_debug_edge_info(self, input_edge_id, active):
        if input_edge_id is not None:
            if input_edge_id not in self.edges:
                self.edges[input_edge_id] = DebugEdgeInfo(
                    active=[active]
                )
            else:
                self.edges[input_edge_id].active.append(active)
