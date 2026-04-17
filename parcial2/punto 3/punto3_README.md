# Punto 3 — Demostración LL(1)

## Gramática original
```
S → AaAb | BbBa
A → ε
B → ε
```

## Análisis previo

Como A → ε y B → ε:
- `S → AaAb` puede derivar directamente: ε·a·ε·b = 'ab'
- `S → BbBa` puede derivar directamente: ε·b·ε·a = 'ba'
- El primer símbolo visible de `AaAb` es `a`
- El primer símbolo visible de `BbBa` es `b`

## Cálculo de FIRST

Para cada no-terminal, FIRST contiene los terminales que pueden aparecer
al inicio de alguna derivación:

```
FIRST(A) = {ε}        — A solo produce la cadena vacía
FIRST(B) = {ε}        — idem

FIRST(AaAb):
  A puede derivar ε → el siguiente símbolo 'a' entra en FIRST
  → FIRST(AaAb) = {a}

FIRST(BbBa):
  B puede derivar ε → el siguiente símbolo 'b' entra en FIRST
  → FIRST(BbBa) = {b}

FIRST(S) = FIRST(AaAb) ∪ FIRST(BbBa) = {a, b}
```

## Cálculo de FOLLOW

```
FOLLOW(S) = {$}          — S es el símbolo inicial
FOLLOW(A):
  aparece en S → AaAb:  después del primer A está 'a'  → a ∈ FOLLOW(A)
  aparece en S → AaAb:  después del segundo A está 'b' → b ∈ FOLLOW(A)
  → FOLLOW(A) = {a, b}
FOLLOW(B):
  análogo → FOLLOW(B) = {a, b}
```

## Tabla predictiva LL(1)

```
      [$]          [a]               [b]
------------------------------------------------------
A                  A→epsilon         A→epsilon
B                  B→epsilon         B→epsilon
S                  S→A a A b         S→B b B a
```

## Conclusión

✓ **La gramática ES LL(1)**

- `FIRST(AaAb) ∩ FIRST(BbBa) = {a} ∩ {b} = ∅`
- Ninguna celda de la tabla tiene más de una producción → sin conflictos.
- Las producciones con ε (A→ε, B→ε) no generan conflicto porque
  los terminales de sus FOLLOW no colisionan con otros FIRST.

## Cómo ejecutar
```bash
python punto3_ll1_demo.py
```
