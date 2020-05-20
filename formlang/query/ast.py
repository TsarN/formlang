from dataclasses import dataclass
from enum import Enum
from formlang.contextfree import Terminal, Nonterminal
from typing import List, Optional


@dataclass
class ConnectStatement:
    path: str

@dataclass
class ListGraphsStatement:
    pass

@dataclass
class RuleStatement:
    lhs: Nonterminal
    rhs: str # TODO: safely parse regex

@dataclass
class VertexExpr:
    name: Optional[str]
    vid: Optional[int]


class Operator(Enum):
    NONE = 1
    EXISTS = 2
    COUNT = 3


@dataclass
class SelectStatement:
    graph_name: str
    operator: Operator
    columns: List[str]
    path_from: VertexExpr
    path_to: VertexExpr
    path_expr: str
