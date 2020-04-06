import io

from formlang.contextfree import *
from formlang.graph import *


GRAPH1 = read_graph_from_file(io.StringIO("""\
0 a 1
1 a 2
2 a 0
2 b 3
3 b 2
"""))

GRAPH2 = read_graph_from_file(io.StringIO("""\
0 a 1
1 a 0
1 b 2
2 b 1
"""))

GRAPH3 = read_graph_from_file(io.StringIO("""\
0 a 1
1 a 2
2 a 0
2 b 3
3 b 4
4 b 2
"""))

GRAMMAR1 = Grammar.deserialize("""\
S eps
S a S a
S b S b
""")

GRAMMAR2 = Grammar.deserialize("""\
S a
S b
S a S a
S b S b
""")

GRAMMAR3 = Grammar.deserialize("""\
S eps
S a S b S
""")

def test_hellings_graph1_grammar1():
    graph = GRAPH1
    grammar = GRAMMAR1
    answer = [
        ( 0, 0 ),
        ( 0, 1 ),
        ( 0, 2 ),
        ( 1, 0 ),
        ( 1, 1 ),
        ( 1, 2 ),
        ( 2, 0 ),
        ( 2, 1 ),
        ( 2, 2 ),
        ( 3, 3 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph1_grammar2():
    graph = GRAPH1
    grammar = GRAMMAR2
    answer = [
        ( 0, 0 ),
        ( 0, 1 ),
        ( 0, 2 ),
        ( 1, 0 ),
        ( 1, 1 ),
        ( 1, 2 ),
        ( 2, 0 ),
        ( 2, 1 ),
        ( 2, 2 ),
        ( 2, 3 ),
        ( 3, 2 ),
        ( 3, 3 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph1_grammar3():
    graph = GRAPH1
    grammar = GRAMMAR3
    answer = [
        ( 0, 0 ),
        ( 0, 2 ),
        ( 0, 3 ),
        ( 1, 1 ),
        ( 1, 2 ),
        ( 1, 3 ),
        ( 2, 2 ),
        ( 2, 3 ),
        ( 3, 3 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph2_grammar1():
    graph = GRAPH2
    grammar = GRAMMAR1
    answer = [
        ( 0, 0 ),
        ( 1, 1 ),
        ( 2, 2 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph2_grammar2():
    graph = GRAPH2
    grammar = GRAMMAR2
    answer = [
        ( 0, 1 ),
        ( 1, 0 ),
        ( 1, 2 ),
        ( 2, 1 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph2_grammar3():
    graph = GRAPH2
    grammar = GRAMMAR3
    answer = [
        ( 0, 0 ),
        ( 0, 2 ),
        ( 1, 1 ),
        ( 2, 2 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph3_grammar1():
    graph = GRAPH3
    grammar = GRAMMAR1
    answer = [
        ( 0, 0 ),
        ( 0, 1 ),
        ( 0, 2 ),
        ( 1, 0 ),
        ( 1, 1 ),
        ( 1, 2 ),
        ( 2, 0 ),
        ( 2, 1 ),
        ( 2, 2 ),
        ( 2, 3 ),
        ( 2, 4 ),
        ( 3, 2 ),
        ( 3, 3 ),
        ( 3, 4 ),
        ( 4, 2 ),
        ( 4, 3 ),
        ( 4, 4 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph3_grammar2():
    graph = GRAPH3
    grammar = GRAMMAR2
    answer = [
        ( 0, 0 ),
        ( 0, 1 ),
        ( 0, 2 ),
        ( 1, 0 ),
        ( 1, 1 ),
        ( 1, 2 ),
        ( 2, 0 ),
        ( 2, 1 ),
        ( 2, 2 ),
        ( 2, 3 ),
        ( 2, 4 ),
        ( 3, 2 ),
        ( 3, 3 ),
        ( 3, 4 ),
        ( 4, 2 ),
        ( 4, 3 ),
        ( 4, 4 ),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph3_grammar3():
    graph = GRAPH3
    grammar = GRAMMAR3
    answer = [
        ( 0, 0 ),
        ( 0, 4 ),
        ( 1, 1 ),
        ( 1, 3 ),
        ( 2, 2 ),
        ( 3, 3 ),
        ( 4, 4 ),
    ]
    assert grammar.path_query(graph) == answer
