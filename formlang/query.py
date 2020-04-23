from formlang.contextfree import Grammar

QL_SYNTAX = Grammar.deserialize("""\
script statement script | eps
statement KW_CONNECT STRING SEMICOLON
statement KW_LIST KW_GRAPHS SEMICOLON
statement NONTERMINAL EQ pattern SEMICOLON
statement KW_SELECT objexpr KW_FROM STRING KW_WHERE whereexpr SEMICOLON
objexpr vsinfo
objexpr KW_COUNT LBR vsinfo RBR
objexpr KW_EXISTS LBR vsinfo RBR
vsinfo IDENT
vsinfo IDENT COMMA IDENT
whereexpr KW_PATH LBR vexpr COMMA vexpr COMMA pattern RBR
vexpr IDENT
vexpr UNDERSCORE
vexpr IDENT DOT KW_ID EQ INT
pattern seq
pattern seq PIPE patter
seq star
seq star seq
star unit
star unit STAR
unit NONTERMINAL
unit IDENT
unit LBR pattern RBR
""")


def read_tokenized_query(file_obj):
    tokens = []
    for line in file_obj:
        tokens += line.strip().split()
    return tokens


def validate_tokenized_query(query):
    return QL_SYNTAX.recognize(query)
