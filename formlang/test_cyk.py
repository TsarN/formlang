from formlang.contextfree import *

def test_even_palindromes():
    g = Grammar.deserialize("""\
S eps
S a S a
S b S b
""")

    assert(g.recognize(""))
    assert(g.recognize("aa"))
    assert(g.recognize("abba"))
    assert(g.recognize("abbbba"))
    assert(g.recognize("aaaaaa"))
    assert(g.recognize("baaaaaab"))
    assert(g.recognize("babbbaabbbab"))
    assert(not g.recognize("babbbabbbab"))
    assert(not g.recognize("aaaaa"))
    assert(not g.recognize("ababa"))
    assert(not g.recognize("a"))
    assert(not g.recognize("cc"))
    assert(not g.recognize("ab"))
    assert(not g.recognize("abb"))
    assert(not g.recognize("abbc"))
    assert(not g.recognize("baba"))
    assert(not g.recognize("ababababab"))


def test_even_palindromes_nonempty():
    g = Grammar.deserialize("""\
S a a
S b b
S a S a
S b S b
""")

    assert(g.recognize("aa"))
    assert(g.recognize("abba"))
    assert(g.recognize("abbbba"))
    assert(g.recognize("aaaaaa"))
    assert(g.recognize("baaaaaab"))
    assert(g.recognize("babbbaabbbab"))
    assert(not g.recognize(""))
    assert(not g.recognize("babbbabbbab"))
    assert(not g.recognize("aaaaa"))
    assert(not g.recognize("ababa"))
    assert(not g.recognize("a"))
    assert(not g.recognize("cc"))
    assert(not g.recognize("ab"))
    assert(not g.recognize("abb"))
    assert(not g.recognize("abbc"))
    assert(not g.recognize("baba"))
    assert(not g.recognize("ababababab"))


def test_well_formed_parentheses():
    g = Grammar.deserialize("""\
S S S
S a S b
S a b
""")

    assert(g.recognize("ab"))
    assert(g.recognize("abab"))
    assert(g.recognize("aabb"))
    assert(g.recognize("aabbab"))
    assert(g.recognize("abaabb"))
    assert(g.recognize("ababab"))
    assert(g.recognize("aaabbb"))
    assert(g.recognize("abaaabbb"))
    assert(g.recognize("abaaababbb"))
    assert(not g.recognize(""))
    assert(not g.recognize("a"))
    assert(not g.recognize("b"))
    assert(not g.recognize("aa"))
    assert(not g.recognize("abb"))
    assert(not g.recognize("aba"))
    assert(not g.recognize("abba"))
    assert(not g.recognize("ababbbababab"))


def test_unequal_number():
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

    assert(g.recognize("a"))
    assert(g.recognize("aa"))
    assert(g.recognize("aab"))
    assert(g.recognize("bab"))
    assert(g.recognize("bbaab"))
    assert(g.recognize("ababbaa"))
    assert(g.recognize("bababbbabba"))
    assert(not g.recognize(""))
    assert(not g.recognize("ab"))
    assert(not g.recognize("abba"))
    assert(not g.recognize("baba"))
    assert(not g.recognize("aabbab"))
    assert(not g.recognize("aaaabbbb"))
    assert(not g.recognize("baababba"))
