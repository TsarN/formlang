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


def test_query_exists_symbol(capsys):
    f('select exists(_) from "g1" where path(_, _, a);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_symbol_empty(capsys):
    f('select exists(_) from "g5" where path(_, _, a);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_symbol_not_exists(capsys):
    f('select exists(_) from "g1" where path(_, _, x);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_expr1(capsys):
    f('select exists(_) from "g1" where path(_, _, a a b b*);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_expr1_filtered1(capsys):
    f('select exists(_) from "g1" where path(x.id=0, _, a a b b*);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_expr1_filtered2(capsys):
    f('select exists(_) from "g1" where path(x.id=1, _, a a b b*);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_expr2(capsys):
    f('select exists(_) from "g1" where path(_, _, a b a);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_ext1(capsys):
    f('A = a a; B = b b*; select exists(_) from "g1" where path(_, _, A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext1_filtered1(capsys):
    f('A = a a; B = b b*; select exists(_) from "g1" where path(_, x.id=2, A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext1_filtered2(capsys):
    f('A = a a; B = b b*; select exists(_) from "g1" where path(_, x.id=0, A B);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_ext2(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g1" where path(_, _, A B a);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_ext3(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g1" where path(_, _, A B b a);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext4(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g1" where path(_, _, A B b A a b);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext5(capsys):
    f('A = a a; B = b (b b)*; select exists(_) from "g2" where path(_, _, A B b A a b);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_ext6(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select exists(_) from "g2" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext7(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select exists(_) from "g3" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext8(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select exists(_) from "g4" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_ext9(capsys):
    f('A = B a a B; B = b b; select exists(_) from "g4" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_exists_ext10(capsys):
    f('A = B a a B; B = b b; select exists(_) from "g2" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext11(capsys):
    f('A = B a a B; B = b b; S = A B; select exists(_) from "g2" where path(_, _, S);')
    assert capsys.readouterr().out == "TRUE\n"

def test_query_exists_ext12(capsys):
    f('A = B a a B; B = b b; S = A B; select exists(_) from "g1" where path(_, _, S);')
    assert capsys.readouterr().out == "FALSE\n"

def test_query_count_symbol(capsys):
    f('select count(_) from "g1" where path(_, _, a);')
    assert capsys.readouterr().out == "3\n"

def test_query_count_symbol_empty(capsys):
    f('select count(_) from "g5" where path(_, _, a);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_symbol_not_count(capsys):
    f('select count(_) from "g1" where path(_, _, x);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_expr1(capsys):
    f('select count(_) from "g1" where path(_, _, a a b b*);')
    assert capsys.readouterr().out == "2\n"

def test_query_count_expr2(capsys):
    f('select count(_) from "g1" where path(_, _, a b a);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_ext1(capsys):
    f('A = a a; B = b b*; select count(_) from "g1" where path(_, _, A B);')
    assert capsys.readouterr().out == "2\n"

def test_query_count_ext2(capsys):
    f('A = a a; B = b (b b)*; select count(_) from "g1" where path(_, _, A B a);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_ext3(capsys):
    f('A = a a; B = b (b b)*; select count(_) from "g1" where path(_, _, A B b a);')
    assert capsys.readouterr().out == "1\n"

def test_query_count_ext4(capsys):
    f('A = a a; B = b (b b)*; select count(_) from "g1" where path(_, _, A B b A a b);')
    assert capsys.readouterr().out == "1\n"

def test_query_count_ext5(capsys):
    f('A = a a; B = b (b b)*; select count(_) from "g2" where path(_, _, A B b A a b);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_ext6(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select count(_) from "g2" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "1\n"

def test_query_count_ext7(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select count(_) from "g3" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "9\n"

def test_query_count_ext7_filtered(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select count(_) from "g3" where path(x.id=1, _, A B A B A B);')
    assert capsys.readouterr().out == "3\n"

def test_query_count_ext8(capsys):
    f('A = a a (a a)*; B = b b (b b)*; select count(_) from "g4" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_ext9(capsys):
    f('A = B a a B; B = b b; select count(_) from "g4" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "0\n"

def test_query_count_ext10(capsys):
    f('A = B a a B; B = b b; select count(_) from "g2" where path(_, _, A B A B A B);')
    assert capsys.readouterr().out == "1\n"

def test_query_count_ext11(capsys):
    f('A = B a a B; B = b b; S = A B; select count(_) from "g2" where path(_, _, S);')
    assert capsys.readouterr().out == "1\n"

def test_query_count_ext12(capsys):
    f('A = B a a B; B = b b; S = A B; select count(_) from "g1" where path(_, _, S);')
    assert capsys.readouterr().out == "0\n"

# There's really not much point in exhaustive testing, since
# test_cfpq already tests the path query algorithm.
# Here we only test the frontend.

def test_query_select1(capsys):
    f('S = () | a S a | b S b; select a, b from "g1" where path(a, b, S);')
    assert capsys.readouterr().out == """\
0 0
0 1
0 2
1 0
1 1
1 2
2 0
2 1
2 2
3 3
"""

def test_query_select2(capsys):
    f('S = () | a S a | b S b; select b, a from "g1" where path(a, b, S);')
    assert capsys.readouterr().out == """\
0 0
0 1
0 2
1 0
1 1
1 2
2 0
2 1
2 2
3 3
"""

def test_query_select3(capsys):
    f('S = () | a S b S; select a, b from "g1" where path(a, b, S);')
    assert capsys.readouterr().out == """\
0 0
0 2
0 3
1 1
1 2
1 3
2 2
2 3
3 3
"""

def test_query_select4(capsys):
    f('S = () | a S b S; select b, a from "g1" where path(a, b, S);')
    assert capsys.readouterr().out == """\
0 0
1 1
2 0
2 1
2 2
3 0
3 1
3 2
3 3
"""

def test_query_select5(capsys):
    f('S = () | a S b S; select b from "g1" where path(a, b, S);')
    assert capsys.readouterr().out == """\
0
1
2
2
2
3
3
3
3
"""

def test_query_select6(capsys):
    f('S = () | a S b S; select a, b from "g1" where path(a.id=0, b, S);')
    assert capsys.readouterr().out == """\
0 0
0 2
0 3
"""

def test_query_select7(capsys):
    f('S = () | a S b S; select a from "g1" where path(a.id=0, b, S);')
    assert capsys.readouterr().out == """\
0
0
0
"""

def test_query_select8(capsys):
    f('S = () | a S b S; select b from "g1" where path(a.id=0, b, S);')
    assert capsys.readouterr().out == """\
0
2
3
"""

def test_query_select9(capsys):
    f('S = () | a S b S; select a, b from "g1" where path(a.id=0, b.id=0, S);')
    assert capsys.readouterr().out == """\
0 0
"""

def test_query_select10(capsys):
    f('S = () | a S b S; select a, b from "g1" where path(a.id=0, b.id=1, S);')
    assert capsys.readouterr().out == ""