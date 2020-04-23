from formlang.contextfree import *

GRAMMARS = [
    # https://en.wikipedia.org/wiki/Context-free_grammar#Examples

    # Words from {a, b} concatenated with their reverse
    ("""\
S eps
S a S a
S b S b
""", """\
@@2 eps
@@2 @@3 @@5
@@2 @@4 @@6
S @@3 @@5
@@5 S @@3
S @@4 @@6
@@6 S @@4
@@3 a
@@4 b
@@5 a
@@6 b
"""),

    # Same thing, but with empty word disallowed

    ("""\
S a a
S b b
S a S a
S b S b
""", """\
@@2 @@3 @@3
@@2 @@4 @@4
@@2 @@3 @@5
@@2 @@4 @@6
S @@3 @@3
S @@4 @@4
S @@3 @@5
@@5 S @@3
S @@4 @@6
@@6 S @@4
@@3 a
@@4 b
"""),

    # Well-formed parentheses

    ("""\
S S S
S a S b
S a b
""", """\
@@2 S S
@@2 @@3 @@5
@@2 @@3 @@4
S S S
S @@3 @@5
@@5 S @@4
S @@3 @@4
@@3 a
@@4 b
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
@@2 V @@5
@@2 @@3 T
@@2 V @@6
@@2 @@3 V
@@2 T @@7
@@2 V @@8
@@2 @@4 U
@@2 V @@9
@@2 @@4 V
@@2 U @@10
@@2 a
@@2 b
T V @@5
@@5 @@3 T
T V @@6
@@6 @@3 V
T T @@7
@@7 @@3 V
U V @@8
@@8 @@4 U
U V @@9
@@9 @@4 V
U U @@10
@@10 @@4 V
V @@3 @@11
@@11 V @@12
@@12 @@4 V
V @@4 @@13
@@13 V @@14
@@14 @@3 V
@@3 a
@@4 b
T @@3 T
T @@3 V
U @@4 U
U @@4 V
@@11 @@4 V
@@13 @@3 V
T a
@@13 a
@@7 a
@@6 a
@@14 a
U b
@@12 b
@@11 b
@@10 b
@@9 b
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
@@1 S
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
S @@1 B A @@2 @@1 B A @@3
A @@3 S @@3
A eps
B A @@4
@@1 a
@@2 b
@@3 c
@@4 d
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
S A @@1
@@1 B @@2
@@2 C D
A eps
A A A
A a
B w @@3
@@3 o w
C A
D u @@4
@@4 S v
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
