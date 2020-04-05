from formlang.contextfree import *

GRAMMARS = [
    # https://en.wikipedia.org/wiki/Context-free_grammar#Examples

    # Words from {a, b} concatenated with their reverse
    ("""\
S eps
S a S a
S b S b
""", """\
A2 eps
A2 A3 A5
A2 A4 A6
S A3 A5
A5 S A3
S A4 A6
A6 S A4
A3 a
A4 b
A5 a
A6 b
"""),

    # Same thing, but with empty word disallowed

    ("""\
S a a
S b b
S a S a
S b S b
""", """\
A2 A3 A3
A2 A4 A4
A2 A3 A5
A2 A4 A6
S A3 A3
S A4 A4
S A3 A5
A5 S A3
S A4 A6
A6 S A4
A3 a
A4 b
"""),

    # Well-formed parentheses

    ("""\
S S S
S a S b
S a b
""", """\
A2 S S
A2 A3 A5
A2 A3 A4
S S S
S A3 A5
A5 S A4
S A3 A4
A3 a
A4 b
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
A2 V A5
A2 A3 T
A2 V A6
A2 A3 V
A2 T A7
A2 V A8
A2 A4 U
A2 V A9
A2 A4 V
A2 U A10
A2 a
A2 b
T V A5
A5 A3 T
T V A6
A6 A3 V
T T A7
A7 A3 V
U V A8
A8 A4 U
U V A9
A9 A4 V
U U A10
A10 A4 V
V A3 A11
A11 V A12
A12 A4 V
V A4 A13
A13 V A14
A14 A3 V
A3 a
A4 b
T A3 T
T A3 V
U A4 U
U A4 V
A11 A4 V
A13 A3 V
T a
A13 a
A7 a
A6 a
A14 a
U b
A12 b
A11 b
A10 b
A9 b
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
