from dataclasses import dataclass
from formlang.contextfree import Terminal, Nonterminal


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
class SelectStatement:
    graph_name: str
    path_from: str
    path_to: str
    path_expr: str
