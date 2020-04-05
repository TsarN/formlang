import io

from formlang.contextfree import *

def test_from_file():
    # I think there's no reason to test reading/writing actual files
    assert(Grammar.from_file(io.StringIO("""\
S eps
S a T b T
T c S c
""")) == Grammar(Nonterminal("S"), [
    Production(Nonterminal("S"), []),
    Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
    Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
]))


def test_write_file():
    # I think there's no reason to test reading/writing actual files
    file_obj = io.StringIO()
    Grammar(Nonterminal("S"), [
        Production(Nonterminal("S"), []),
        Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
        Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
    ]).write_file(file_obj)
    file_obj.seek(0)
    assert(file_obj.read() == """\
S eps
S a T b T
T c S c""")

    file_obj = io.StringIO()
    Grammar(Nonterminal("T"), [
        Production(Nonterminal("S"), []),
        Production(Nonterminal("S"), [Terminal("a"), Nonterminal("T"), Terminal("b"), Nonterminal("T")]),
        Production(Nonterminal("T"), [Terminal("c"), Nonterminal("S"), Terminal("c")]),
    ]).write_file(file_obj)
    file_obj.seek(0)
    assert(file_obj.read() == """\
T c S c
S eps
S a T b T""")
