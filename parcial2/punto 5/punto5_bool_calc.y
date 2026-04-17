/* Punto 5 — Parser YACC/Bison: calculadora de expresiones booleanas
   Gramática:
     expr → expr OR expr
          | expr AND expr
          | NOT expr
          | '(' expr ')'
          | true
          | false

   Precedencia (menor → mayor):
     OR < AND < NOT

   El parser es LALR(1). Los conflictos shift/reduce se resuelven
   mediante las declaraciones %left / %right de precedencia.

   Complejidad del analizador: O(n)
     El stack de LALR crece a lo sumo O(n) y cada token se procesa
     una sola vez con acciones shift/reduce en tiempo constante.
*/

%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *msg);
int yylex(void);
%}

/* Activar mensajes de error descriptivos */
%define parse.error verbose

/* Declaración de tokens */
%token TRUE FALSE

/*
   Precedencia: las declaradas al final tienen mayor prioridad.
   %left  → asociatividad izquierda (OR, AND)
   %right → asociatividad derecha (NOT, operador unario)
*/
%left  OR
%left  AND
%right NOT

%%

/* Regla raíz: acepta múltiples líneas */
input
    : /* vacío */
    | input line
    ;

line
    : expr '\n'
        {
            printf("= %s\n", $1 ? "true" : "false");
        }
    | '\n'
        { /* línea vacía */ }
    | error '\n'
        {
            /* Recuperación de error: descartar hasta el siguiente '\n' */
            yyerrok;
            fprintf(stderr, "Expresión ignorada. Intente de nuevo.\n");
        }
    ;

expr
    : expr OR expr
        { $$ = $1 || $3; }

    | expr AND expr
        { $$ = $1 && $3; }

    | NOT expr
        { $$ = !$2; }

    | '(' expr ')'
        { $$ = $2; }

    | TRUE
        { $$ = 1; }

    | FALSE
        { $$ = 0; }
    ;

%%

void yyerror(const char *msg) {
    fprintf(stderr, "Error de sintaxis: %s\n", msg);
}

int main(void) {
    printf("Calculadora booleana (YACC/Bison)\n");
    printf("Operadores: AND  OR  NOT\n");
    printf("Valores:    true  false\n");
    printf("Ejemplo:    NOT true AND (false OR true)\n");
    printf("Salir:      Ctrl+D\n\n");
    return yyparse();
}

/*
   Análisis del desempeño (LALR(1)):
   ─────────────────────────────────
   1. Tipo de parser: LALR(1) — bottom-up, maneja más gramáticas que LL(1).

   2. Resolución de conflictos:
      - La expresión 'true OR true AND false' es ambigua sin precedencia.
      - %left OR / %left AND / %right NOT le indican a Bison cómo resolver
        los conflictos shift/reduce sin errores ni advertencias.
      - Con estas directivas: NOT tiene mayor precedencia que AND > OR.

   3. Complejidad: O(n)
      - El stack LALR crece linealmente.
      - Cada token se procesa en O(1) amortizado (lookup en tabla de estados).

   4. Manejo de errores:
      - La regla 'error '\n'' activa la recuperación automática de Bison.
      - yyerrok reinicia el parser para la siguiente línea.
      - Paréntesis desbalanceados son detectados (falta ')' → error de sintaxis).
*/
