import io

import pytest

from formlang.contextfree import *
from formlang.graph import *
from formlang.samples import *

GRAMMAR1 = Grammar.deserialize(even_palindromes)

GRAMMAR2 = Grammar.deserialize(odd_palindromes_nonempty)

GRAMMAR3a = Grammar.deserialize(well_formed_parentheses)

GRAMMAR3b = Grammar.deserialize(well_formed_parentheses_ambiguous)


def get_graph(name):
    return read_graph_from_file(io.StringIO(sample_graphs[name]))

@pytest.fixture(params=Grammar.path_query.algorithms)
def algorithm(request):
    yield request.param

def test_cfpq_graph1_grammar1(algorithm):
    graph = get_graph("g1")
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
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph1_grammar2(algorithm):
    graph = get_graph("g1")
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
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph1_grammar3(algorithm):
    graph = get_graph("g1")
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
        assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph2_grammar1(algorithm):
    graph = get_graph("g2")
    grammar = GRAMMAR1
    answer = [
        ( 0, 0 ),
        ( 1, 1 ),
        ( 2, 2 ),
    ]
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph2_grammar2(algorithm):
    graph = get_graph("g2")
    grammar = GRAMMAR2
    answer = [
        ( 0, 1 ),
        ( 1, 0 ),
        ( 1, 2 ),
        ( 2, 1 ),
    ]
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph2_grammar3(algorithm):
    graph = get_graph("g2")
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
        answer = [
            ( 0, 0 ),
            ( 0, 2 ),
            ( 1, 1 ),
            ( 2, 2 ),
        ]
        assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph3_grammar1(algorithm):
    graph = get_graph("g3")
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
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph3_grammar2(algorithm):
    graph = get_graph("g3")
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
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph3_grammar3(algorithm):
    graph = get_graph("g3")
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
        assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph4_grammar1(algorithm):
    graph = get_graph("g4")
    grammar = GRAMMAR1
    answer = [
        (0, 0),
        (0, 2),
        (1, 1),
        (2, 2),
    ]
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph4_grammar2(algorithm):
    graph = get_graph("g4")
    grammar = GRAMMAR2
    answer = [
        (0, 0),
        (0, 1),
        (1, 2),
        (2, 2),
    ]
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph4_grammar3(algorithm):
    graph = get_graph("g4")
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
        answer = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 1),
            (2, 2),
        ]
        assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph5_grammar1(algorithm):
    graph = get_graph("g5")
    grammar = GRAMMAR1
    answer = []
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph5_grammar2(algorithm):
    graph = get_graph("g5")
    grammar = GRAMMAR2
    answer = []
    assert grammar.clone().path_query(graph, algorithm) == answer


def test_cfpq_graph5_grammar3(algorithm):
    graph = get_graph("g5")
    for grammar in [GRAMMAR3a, GRAMMAR3b]:
        answer = []
        assert grammar.clone().path_query(graph, algorithm) == answer
