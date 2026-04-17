# Punto 4 — CYK vs Parser Predictivo LL(1)

## Archivos

| Archivo | Descripción |
|---|---|
| `punto4_cyk_parser.py` | Parser CYK sobre gramática en CNF |
| `punto4_predictive_parser.py` | Parser predictivo LL(1) |
| `punto4_comparison.py` | Comparación de rendimiento |

---

## Gramáticas

### CYK — Chomsky Normal Form (CNF)
Toda producción debe ser `A → a` (un terminal) o `A → BC` (dos no-terminales).

```
E     → n  |  E EA  |  E EM
EA    → PLUS E
EM    → TIMES E
PLUS  → +
TIMES → *
```

### LL(1) Predictivo — sin recursión izquierda
```
E  → T E'
E' → + T E'  |  ε
T  → F T'
T' → * F T'  |  ε
F  → n
```

---

## CYK (`punto4_cyk_parser.py`)

### Estructura

- `tokenize(expr)` — convierte números a `'n'` y devuelve lista de tokens.
- `cyk_parse(tokens)` — tabla `dp[i][j]` donde cada celda es el conjunto
  de no-terminales que derivan `tokens[i..j]`.

### Llenado de la tabla

```
# Caso base (longitud 1):
dp[i][i] ← {NT | NT → token[i] está en la gramática}

# Inducción (longitud 2..n):
for cada corte k entre i y j:
    si B ∈ dp[i][k] y C ∈ dp[k+1][j]:
        agregar A a dp[i][j]  para toda producción A → BC
```

### Complejidad
- Tiempo: **O(n³ · |G|)** — tres loops anidados sobre la longitud de entrada.
- Espacio: **O(n²)** — tabla triangular de conjuntos.

---

## Parser Predictivo LL(1) (`punto4_predictive_parser.py`)

### Estructura

Cada producción de la gramática es un método:

```python
parse_E()        # E  → T E'
parse_E_prime()  # E' → + T E' | ε
parse_T()        # T  → F T'
parse_T_prime()  # T' → * F T' | ε
parse_F()        # F  → n
```

La selección de producción se hace mirando el token actual (`current()`),
sin backtracking ni tabla explícita.

### Complejidad
- Tiempo: **O(n)** — cada token se consume exactamente una vez.
- Espacio: **O(n)** — profundidad del stack de llamadas recursivas.

---

## Comparación de rendimiento

### Resultados experimentales
```
Operandos   Tokens     CYK (ms)   LL(1) (ms)     CYK/LL
--------------------------------------------------------
        1        1       ~0.00       ~0.00         ~1.5x
        5        9       ~0.18       ~0.01        ~25x
       10       19       ~1.60       ~0.01       ~193x
       20       39      ~11.95       ~0.01       ~845x
       50       99     ~204.55       ~0.03      ~5904x
      100      199    ~1621.37       ~0.08     ~19553x
```

### Análisis teórico

**CYK:**
- Complejidad: O(n³ · |G|)
- Acepta cualquier CFG convertida a CNF (gramáticas ambiguas incluidas).
- Inviable para producción; útil en NLP y reconocimiento general.

**LL(1) Predictivo:**
- Complejidad: O(n)
- Solo funciona con gramáticas LL(1) (sin ambigüedad, sin recursión izquierda).
- Elección natural para lenguajes de programación deterministas.

### Conclusión

Para una calculadora el LL(1) es la elección correcta: lineal y predecible.
CYK tiene sentido cuando la gramática no puede ser LL(1) o cuando se necesita
parsing de lenguaje natural con gramáticas ambiguas.

---

## Cómo ejecutar

```bash
python punto4_cyk_parser.py
python punto4_predictive_parser.py
python punto4_comparison.py
```
