# Parcial LP — Instrucciones de ejecución

## Punto 1 — Gramática CRUD (solo lectura)
```
punto1_grammar.md
```

## Punto 2 — Parser CRUD NoSQL

### Opción A: Python (corre sin instalar nada)
```bash
python punto2_test_cases.py
```

### Opción B: ANTLR4
```bash
# Instalar ANTLR4
pip install antlr4-tools

# Generar el parser
antlr4 -Dlanguage=Python3 punto2_NoSQLCRUD.g4

# Probar interactivamente
antlr4-parse punto2_NoSQLCRUD.g4 program -tree
# (pegar una sentencia y presionar Ctrl+D)
```

## Punto 3 — Demostración LL(1)
```bash
python punto3_ll1_demo.py
```

## Punto 4 — CYK vs Predictivo

Correr cada parser individualmente:
```bash
python punto4_cyk_parser.py
python punto4_predictive_parser.py
```

Comparación de rendimiento:
```bash
python punto4_comparison.py
```

## Punto 5 — Calculadora booleana YACC

Requiere `bison` y `flex` instalados:
```bash
bison -d punto5_bool_calc.y
flex punto5_bool_calc.l
gcc bool_calc.tab.c lex.yy.c -o bool_calc -lfl
./bool_calc
```

Ejemplos de entrada:
```
true AND false
NOT true OR true
(true OR false) AND NOT false
true AND (false OR true AND NOT false)
```

---

## Dependencias Python
- Python 3.8+
- Sin librerías externas (solo stdlib)
