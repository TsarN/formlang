grammar query;

/*
 * Parser rules:
 */

script : statement* EOF ;

statement : (connect_statement     |
             list_graphs_statement |
             list_labels_statement |
             rule_statement        |
             select_statement) SEMICOLON ;

connect_statement : KW_CONNECT STRING;

list_graphs_statement : KW_LIST KW_GRAPHS (KW_IN STRING)?;

list_labels_statement : KW_LIST KW_LABELS KW_IN STRING;

rule_statement : NONTERMINAL EQ pattern;

select_statement : KW_SELECT objexpr KW_FROM STRING KW_WHERE whereexpr (KW_USING STRING)?;

objexpr : vsinfo | KW_COUNT LBR vsinfo RBR | KW_EXISTS LBR vsinfo RBR | KW_UNIQUE LBR vsinfo RBR;

vsinfo : IDENT | IDENT COMMA IDENT;

whereexpr : KW_PATH LBR vexpr COMMA vexpr COMMA pattern RBR;

vexpr : IDENT | UNDERSCORE | IDENT DOT KW_ID EQ INT;

pattern : seq (PIPE seq)*;
seq : star+;
star : unit STAR?;
unit : KW_EPS | NONTERMINAL | IDENT | LBR pattern RBR;

/*
 * Lexer rules:
 */

WS : [ \r\n\t] + -> skip;

LBR : '(';
RBR : ')';
COMMA : ',';
SEMICOLON : ';';
PIPE : '|';
DOT : '.';
STAR : '*';
EQ : '=';
UNDERSCORE : '_';
KW_IN : 'in';
KW_ID : 'id';
KW_EPS : 'eps';
KW_USING : 'using';
KW_COUNT : 'count';
KW_EXISTS : 'exists';
KW_UNIQUE : 'unique';
KW_LABELS : 'labels';
KW_FROM : 'from';
KW_WHERE : 'where';
KW_LIST : 'list';
KW_CONNECT : 'connect';
KW_GRAPHS : 'graphs';
KW_SELECT : 'select';
KW_PATH: 'path';
IDENT : [a-z]+;
INT : '0' | [1-9][0-9]*;
NONTERMINAL : [A-Z][a-zA-Z0-9]*;
STRING : '"' ~('\r' | '\n' | '"')* '"' ;

ERR_CHAR : . ;