from antlr4 import InputStream
from formlang.query import verify_query


def f(s):
    return verify_query(InputStream(s))


def test_query_connect():
    assert f("connect \"database\";")
    assert not f("connect \"database\"")
    assert not f("connect;")

def test_query_list_graphs():
    assert f("list graphs;")
    assert not f("list graphs")
    assert not f("list;")

def test_query_grammar():
    assert f("S = a;")
    assert not f("S =;")
    assert f("S = a | ( b S c S ) * ;")
    assert not f("S = ( b S c S * ;")

def test_query_select():
    assert f("select a from \"graph\" where path ( _, _, S);")
    assert f("select a , a from \"graph\" where path ( _, _, S);")
    assert f("select a , a from \"graph\" where path ( _, a.id = 1234, S);")
    assert f("select a from \"graph\" where path( _, _, S*);")
    assert f("select a from \"graph\" where path( _, _, S | a*);")
    assert not f("select a \"graph\" where path( _, _, S | a*);")
    assert not f("select from \"graph\" where path( _, _, S);")
    assert not f("select a from \"graph\" where path _, _, S;")
    assert not f("select a from \"graph\" ;")
