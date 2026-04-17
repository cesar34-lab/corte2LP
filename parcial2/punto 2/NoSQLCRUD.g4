// Punto 2 — Gramática ANTLR4 para CRUD NoSQL
// Compilar: antlr4 -Dlanguage=Python3 NoSQLCRUD.g4
// Ejecutar:  grun NoSQLCRUD program -tree < input.txt

grammar NoSQLCRUD;

// ========================
// PARSER RULES
// ========================

program
    : statement* EOF
    ;

statement
    : insertStmt
    | findStmt
    | updateStmt
    | deleteStmt
    ;

insertStmt
    : INSERT INTO ID document SEMI
    ;

findStmt
    : FIND IN ID (WHERE filter)? SEMI
    ;

updateStmt
    : UPDATE ID SET fieldList (WHERE filter)? SEMI
    ;

deleteStmt
    : DELETE FROM ID WHERE filter SEMI
    ;

document
    : LBRACE fieldList? RBRACE
    ;

fieldList
    : field (COMMA field)*
    ;

field
    : STRING COLON value
    ;

filter
    : condition (AND condition)*
    ;

condition
    : ID OP value
    ;

value
    : STRING
    | NUMBER
    | BOOLEAN
    | document
    ;

// ========================
// LEXER RULES
// ========================

INSERT  : 'INSERT' ;
INTO    : 'INTO'   ;
FIND    : 'FIND'   ;
IN      : 'IN'     ;
UPDATE  : 'UPDATE' ;
SET     : 'SET'    ;
DELETE  : 'DELETE' ;
FROM    : 'FROM'   ;
WHERE   : 'WHERE'  ;
AND     : 'AND'    ;

BOOLEAN : 'true' | 'false' ;

OP      : '==' | '!=' | '<=' | '>=' | '<' | '>' ;
SEMI    : ';'  ;
COMMA   : ','  ;
COLON   : ':'  ;
LBRACE  : '{'  ;
RBRACE  : '}'  ;

NUMBER  : [0-9]+ ('.' [0-9]+)? ;
STRING  : '"' (~["\r\n])* '"'  ;
ID      : [a-zA-Z][a-zA-Z0-9_]* ;

WS      : [ \t\r\n]+ -> skip ;
COMMENT : '//' ~[\r\n]* -> skip ;
