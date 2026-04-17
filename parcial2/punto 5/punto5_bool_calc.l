/* Punto 5 — Lexer (Flex) para calculadora booleana
   Compilar:
     bison -d punto5_bool_calc.y
     flex punto5_bool_calc.l
     gcc punto5_bool_calc.tab.c lex.yy.c -o bool_calc -lfl
     ./bool_calc
*/

%{
#include <stdio.h>
#include "punto5_bool_calc.tab.h"
%}

%%

"true"          { return TRUE; }
"false"         { return FALSE; }
"AND"           { return AND; }
"OR"            { return OR; }
"NOT"           { return NOT; }

[()]            { return yytext[0]; }
\n              { return '\n'; }
[ \t]           { /* ignorar espacios */ }

.               {
                  fprintf(stderr, "Token no reconocido: '%s'\n", yytext);
                }

%%

int yywrap(void) {
    return 1;
}
