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
