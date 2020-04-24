from formlang.contextfree import *

GRAMMARS = [
    # https://en.wikipedia.org/wiki/Context-free_grammar#Examples

    # Words from {a, b} concatenated with their reverse
    ("""\
S eps
S a S a
S b S b
""", """\
NEW2 eps
NEW2 NEW3 NEW5
NEW2 NEW4 NEW6
S NEW3 NEW5
NEW5 S NEW3
S NEW4 NEW6
NEW6 S NEW4
NEW3 a
NEW4 b
NEW5 a
NEW6 b
"""),

    # Same thing, but with empty word disallowed

    ("""\
S a a
S b b
S a S a
S b S b
""", """\
NEW2 NEW3 NEW3
NEW2 NEW4 NEW4
NEW2 NEW3 NEW5
NEW2 NEW4 NEW6
S NEW3 NEW3
S NEW4 NEW4
S NEW3 NEW5
NEW5 S NEW3
S NEW4 NEW6
NEW6 S NEW4
NEW3 a
NEW4 b
"""),

    # Well-formed parentheses

    ("""\
S S S
S a S b
S a b
""", """\
NEW2 S S
NEW2 NEW3 NEW5
NEW2 NEW3 NEW4
S S S
S NEW3 NEW5
NEW5 S NEW4
S NEW3 NEW4
NEW3 a
NEW4 b
"""),

    # Unequal number of a's and b's

    ("""\
S T
S U
T V a T
T V a V
T T a V
U V b U
U V b V
U U b V
V a V b V
V b V a V
V eps
""", """
NEW2 V NEW5
NEW2 NEW3 T
NEW2 V NEW6
NEW2 NEW3 V
NEW2 T NEW7
NEW2 V NEW8
NEW2 NEW4 U
NEW2 V NEW9
NEW2 NEW4 V
NEW2 U NEW10
NEW2 a
NEW2 b
T V NEW5
NEW5 NEW3 T
T V NEW6
NEW6 NEW3 V
T T NEW7
NEW7 NEW3 V
U V NEW8
NEW8 NEW4 U
U V NEW9
NEW9 NEW4 V
U U NEW10
NEW10 NEW4 V
V NEW3 NEW11
NEW11 V NEW12
NEW12 NEW4 V
V NEW4 NEW13
NEW13 V NEW14
NEW14 NEW3 V
NEW3 a
NEW4 b
T NEW3 T
T NEW3 V
U NEW4 U
U NEW4 V
NEW11 NEW4 V
NEW13 NEW3 V
T a
NEW13 a
NEW7 a
NEW6 a
NEW14 a
U b
NEW12 b
NEW11 b
NEW10 b
NEW9 b
""")
]


def test_normalize():
    for orig, norm in GRAMMARS:
        g = Grammar.deserialize(orig)
        target = Grammar.deserialize(norm)
        assert(not g.is_normalized())
        Nonterminal.instances = 1
        g.normalize()
        assert(g.is_normalized())
        assert(g == target)

def test_eliminate_start():
    g = Grammar.deserialize("""\
S A B
S eps
A a
B b
A B S B
""")
    Nonterminal.instances = 0
    g.eliminate_start()
    assert(g == Grammar.deserialize("""\
NEW1 S
S A B
S eps
A a
B b
A B S B
"""))


def test_eliminate_nonsolitary_terminals():
    g = Grammar.deserialize("""\
S a B A b a B A c
A c S c
A eps
B A d
""")
    Nonterminal.instances = 0
    g.eliminate_nonsolitary_terminals()
    assert(g == Grammar.deserialize("""\
S NEW1 B A NEW2 NEW1 B A NEW3
A NEW3 S NEW3
A eps
B A NEW4
NEW1 a
NEW2 b
NEW3 c
NEW4 d
"""))


def test_eliminate_long_productions():
    g = Grammar.deserialize("""\
S A B C D
A eps
A A A
A a
B w o w
C A
D u S v
""")
    Nonterminal.instances = 0
    g.eliminate_long_productions()
    assert(g == Grammar.deserialize("""\
S A NEW1
NEW1 B NEW2
NEW2 C D
A eps
A A A
A a
B w NEW3
NEW3 o w
C A
D u NEW4
NEW4 S v
"""))

def test_eliminate_epsilon():
    g = Grammar.deserialize("""\
S a T b T
T x
T eps
""")
    Nonterminal.instances = 0
    g.eliminate_epsilon()
    assert(g == Grammar.deserialize("""\
S a b
S a b T
S a T b
S a T b T
T x
"""))

def test_eliminate_epsilon2():
    g = Grammar.deserialize("""\
S a T b T
T S c S d S
S eps
T eps
""")
    Nonterminal.instances = 0
    g.eliminate_epsilon()
    assert(g == Grammar.deserialize("""\
S eps
S a b
S a T b
S a b T
S a T b T
T c d
T S c d
T c S d
T S c S d
T c d S
T S c d S
T c S d S
T S c S d S
"""))

def test_eliminate_unit_rules():
    g = Grammar.deserialize("""\
S A A
A B
A C
B x
C y
""")
    Nonterminal.instances = 0
    g.eliminate_unit_rules()
    g.eliminate_repetitions()
    assert(g == Grammar.deserialize("""\
S A A
A x
A y
B x
C y
"""))


def test_eliminate_unit_rules2():
    g = Grammar.deserialize("""\
S T
S U
T V a T
T V a V
T T a V
U V b U
U V b V
U U b V
V a V b V
V b V a V
V eps
""")
    Nonterminal.instances = 0
    g.eliminate_unit_rules()
    g.eliminate_repetitions()
    assert(g == Grammar.deserialize("""\
S V a T
S V a V
S T a V
S V b U
S V b V
S U b V
T V a T
T V a V
T T a V
U V b U
U V b V
U U b V
V a V b V
V b V a V
V eps
"""))
