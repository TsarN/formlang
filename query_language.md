# Query language

## Usage

Statements are separated by semicolons.

Connect to database:

```
connect "./path/to/db";
```

List graphs:

```
list graphs;
list graphs in "./path/to/another/db";
```

List edge lables:

```
list labels in "graph";
```

Specify grammar:

```
S = eps | a S b S;
```

Execute a context free path query:

```
select u, v from "graph" where path(u, v, S);
select count(v) from "graph" where path(_, v, S) using "hellings";
select exists(u, v) from "graph" where path(u.id = 10, v, S) using "tensor";
select unique(v) from "graph" where path(u, v.id = 42, S) using "matrix";
```

## Syntax

```
script = statement script | eps
statement = KW_CONNECT STRING SEMICOLON
statement = KW_LIST KW_GRAPHS (KW_IN STRING)? SEMICOLON
statement = NONTERMINAL EQ pattern SEMICOLON
statement = KW_SELECT objexpr KW_FROM STRING KW_WHERE whereexpr SEMICOLON
objexpr = vsinfo
objexpr = KW_COUNT LBR vsinfo RBR
objexpr = KW_EXISTS LBR vsinfo RBR
objexpr = KW_UNIQUE LBR vsinfo RBR
vsinfo = IDENT
vsinfo = IDENT COMMA IDENT
whereexpr = KW_PATH LBR vexpr COMMA vexpr COMMA pattern RBR
vexpr = IDENT
vexpr = UNDERSCORE
vexpr = IDENT DOT KW_ID EQ INT
pattern = seq
pattern = seq PIPE pattern
seq = star
seq = star seq
star = unit
star = unit STAR
unit = KW_EPS
unit = NONTERMINAL
unit = IDENT
unit = LBR pattern RBR
```

## Tokens

```
LBR = '('
RBR = ')'
COMMA = ','
SEMICOLON = ';'
PIPE = '|'
DOT = '.'
STAR = '*'
EQ = '='
UNDERSCORE = '_'
KW_ID = 'id'
KW_IN = 'in'
KW_UNIQUE = 'unique'
KW_USING = 'using'
KW_LABELS = 'labels'
KW_EPS = 'eps'
KW_COUNT = 'count'
KW_EXISTS = 'exists'
KW_FROM = 'from'
KW_WHERE = 'where'
KW_LIST = 'list'
KW_CONNECT = 'connect'
KW_GRAPHS = 'graphs'
KW_SELECT = 'select'
KW_PATH = 'path'
IDENT = [a-z]+
INT = 0 | [1-9][0-9]*
NONTERMINAL = [A-Z][a-zA-Z0-9]*
STRING = '"' [^"]* '"'
```
