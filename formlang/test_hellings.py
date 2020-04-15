import io

from formlang.contextfree import *
from formlang.graph import *
from formlang.samplegrammars import *


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

GRAPH4 = read_graph_from_file(io.StringIO("""\
0 a 0
0 b 1
1 b 2
2 a 2
"""))

GRAPH5 = read_graph_from_file(io.StringIO(""))

GRAMMAR1 = Grammar.deserialize(even_palindromes)

GRAMMAR2 = Grammar.deserialize(odd_palindromes_nonempty)

GRAMMAR3a = Grammar.deserialize(well_formed_parentheses)

GRAMMAR3b = Grammar.deserialize(well_formed_parentheses_ambiguous)

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
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
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
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
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
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
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


def test_hellings_graph4_grammar1():
    graph = GRAPH4
    grammar = GRAMMAR1
    answer = [
        (0, 0),
        (0, 2),
        (1, 1),
        (2, 2),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph4_grammar2():
    graph = GRAPH4
    grammar = GRAMMAR2
    answer = [
        (0, 0),
        (0, 1),
        (1, 2),
        (2, 2),
    ]
    assert grammar.path_query(graph) == answer


def test_hellings_graph4_grammar3():
    graph = GRAPH4
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
        answer = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 1),
            (2, 2),
        ]
        assert grammar.path_query(graph) == answer


def test_hellings_graph5_grammar1():
    graph = GRAPH5
    grammar = GRAMMAR1
    answer = []
    assert grammar.path_query(graph) == answer


def test_hellings_graph5_grammar2():
    graph = GRAPH5
    grammar = GRAMMAR2
    answer = []
    assert grammar.path_query(graph) == answer


def test_hellings_graph5_grammar3():
    graph = GRAPH5
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
        answer = []
        assert grammar.path_query(graph) == answer
