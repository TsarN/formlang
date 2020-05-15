from antlr4 import InputStream
from formlang.db import Executor, DictDatabase, FileDatabase
from formlang.query import parse_query
from formlang.samples import sample_graphs

import pytest


def f(s, real_fs=False):
    stream = InputStream(s)
    parsed = parse_query(stream)

    if real_fs:
        db = FileDatabase()
    else:
        db = DictDatabase(sample_graphs)

    executor = Executor(db)
    executor.execute_many(parsed)
    return executor


def test_connect():
    assert f('connect "./path/to/db";').db.path == "./path/to/db"


def test_list_graphs(capsys):
    f("list graphs;")
    assert capsys.readouterr().out == """\
g1
g2
g3
g4
g5
"""

def test_real_fs(capsys, tmp_path):
    names = ["foo", "bar", "baz"]
    for i in names:
        (tmp_path / i).write_text("1 a 2\n")

    assert f(f"""
connect "{tmp_path}";
list graphs;
""", True).db.path == str(tmp_path)

    assert capsys.readouterr().out == """\
bar
baz
foo
"""


def test_query_symbol(capsys):
    f('select exists(_) from "g1" where path(_, _, a);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_symbol_empty(capsys):
    f('select exists(_) from "g5" where path(_, _, a);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_symbol_not_exists(capsys):
    f('select exists(_) from "g1" where path(_, _, x);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_expr1(capsys):
    f('select exists(_) from "g1" where path(_, _, a a b+);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_expr2(capsys):
    f('select exists(_) from "g1" where path(_, _, a b a);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_ext1(capsys):
    f('A = a a; B = b+; select exists(_) from "g1" where path(_, _, A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext2(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g1" where path(_, _, A B a);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_ext3(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g1" where path(_, _, A B b a);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext4(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g1" where path(_, _, A B b A a b);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext5(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g2" where path(_, _, A B b A a b);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_ext6(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select exists(_) from "g2" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext7(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select exists(_) from "g3" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext8(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select exists(_) from "g4" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_ext9(capsys):
    f('A = B a a B; B = b b; select exists(_) from "g4" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_ext10(capsys):
    f('A = B a a B; B = b b; select exists(_) from "g2" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext11(capsys):
    f('A = B a a B; B = b b; S = A B; select exists(_) from "g2" where path(_, _, S);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_ext12(capsys):
    f('A = B a a B; B = b b; S = A B; select exists(_) from "g1" where path(_, _, S);')
    assert capsys.readouterr().out == "FALSE\n"