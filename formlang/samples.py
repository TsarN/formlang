even_palindromes = """\
S eps
S a S a
S b S b
"""

even_palindromes_nonempty = """\
S a a
S b b
S a S a
S b S b
"""

odd_palindromes_nonempty = """\
S a
S b
S a S a
S b S b
"""

well_formed_parentheses = """\
S a S b S
S eps
"""

well_formed_parentheses_ambiguous = """\
S eps
S S S
S a S b
"""

unequal_number = """\
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
"""


sample_graphs = {
    "g1": """\
0 a 1
1 a 2
2 a 0
2 b 3
3 b 2
""",
    "g2": """\
0 a 1
1 a 0
1 b 2
2 b 1
""",
    "g3": """\
0 a 1
1 a 2
2 a 0
2 b 3
3 b 4
4 b 2
""",
    "g4": """\
0 a 0
0 b 1
1 b 2
2 a 2
""",
    "g5": ""
}
