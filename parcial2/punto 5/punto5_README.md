# Punto 5 — Calculadora booleana (YACC/Bison)

## Archivos

| Archivo | Descripción |
|---|---|
| `punto5_bool_calc.y` | Gramática YACC/Bison con acciones semánticas |
| `punto5_bool_calc.l` | Lexer Flex |

---

## Gramática

```
expr → expr OR expr
     | expr AND expr
     | NOT expr
     | '(' expr ')'
     | true
     | false
```

### Precedencia (menor → mayor)
```
%left  OR          — menor prioridad
%left  AND
%right NOT         — mayor prioridad (operador unario)
```

Esto resuelve automáticamente los conflictos shift/reduce que Bison detecta
en expresiones como `true OR false AND true` → se evalúa como `true OR (false AND true)`.

---

## Compilar y ejecutar

```bash
# 1. Generar parser
bison -d punto5_bool_calc.y

# 2. Generar lexer
flex punto5_bool_calc.l

# 3. Compilar
gcc punto5_bool_calc.tab.c lex.yy.c -o bool_calc -lfl

# 4. Ejecutar
./bool_calc
```

### Ejemplos de entrada
```
true AND false
NOT true OR true
(true OR false) AND NOT false
true AND (false OR true AND NOT false)
```

---

## Desempeño del analizador LALR(1)

### Tipo de parser
LALR(1) — *Look-Ahead LR con 1 token de lookahead*. Construye el árbol
de abajo hacia arriba (bottom-up). Acepta más gramáticas que LL(1) porque
puede manejar recursión izquierda y más patrones de expresión.

### Resolución de conflictos shift/reduce
La gramática de expresiones booleanas genera conflictos shift/reduce
por naturaleza: al ver `AND` después de `expr OR expr`, Bison no sabe si
reducir el `OR` primero o desplazar el `AND`. Las directivas `%left OR` y
`%left AND` le indican que `AND` tiene más precedencia → desplazar siempre
ante ese conflicto.

### Complejidad
- **O(n)** — el stack LALR crece a lo sumo O(n) y cada token se procesa
  en O(1) amortizado (lookup en tabla de estados precompilada).

### Manejo de errores
- La regla `error '\n'` activa la recuperación estándar de Bison.
- `yyerrok` reinicia el estado del parser para continuar con la línea siguiente.
- Paréntesis desbalanceados producen `"Error de sintaxis"` sin abortar el programa.

### Evaluación semántica
Cada producción retorna directamente un `int` (0 = false, 1 = true):
```c
expr OR expr   → $$ = $1 || $3;
expr AND expr  → $$ = $1 && $3;
NOT expr       → $$ = !$2;
```
La evaluación es bottom-up: las hojas se evalúan primero y los resultados
se propagan hacia la raíz del árbol de derivación.
