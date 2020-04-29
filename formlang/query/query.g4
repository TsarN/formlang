grammar query;

/*
 * Parser rules:
 */

script : statement* EOF ;

statement : (connect_statement     |
             list_graphs_statement |
             rule_statement        |
             select_statement) SEMICOLON ;

connect_statement : KW_CONNECT STRING;

list_graphs_statement : KW_LIST KW_GRAPHS;

rule_statement : NONTERMINAL EQ pattern;

select_statement : KW_SELECT objexpr KW_FROM STRING KW_WHERE whereexpr;

objexpr : vsinfo | KW_COUNT LBR vsinfo RBR | KW_EXISTS LBR vsinfo RBR;

vsinfo : IDENT | IDENT COMMA IDENT;

whereexpr : KW_PATH LBR vexpr COMMA vexpr COMMA pattern RBR;

vexpr : IDENT | UNDERSCORE | IDENT DOT KW_ID EQ INT;

pattern : seq (PIPE pattern)?;
seq : star+;
star : unit STAR?;
unit : NONTERMINAL | IDENT | LBR pattern RBR;

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
KW_ID : 'id';
KW_COUNT : 'count';
KW_EXISTS : 'exists';
KW_FROM : 'from';
KW_WHERE : 'where';
KW_LIST : 'list';
KW_CONNECT : 'connect';
KW_GRAPHS : 'graphs';
KW_SELECT : 'select';
KW_PATH: 'path';
IDENT : [a-z]+;
INT : '0' | [1-9][0-9]*;
NONTERMINAL : [A-Z][a-z]*;
STRING : '"' ~('\r' | '\n' | '"')* '"' ;

ERR_CHAR : . ;