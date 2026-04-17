# Punto 4 — Parser CYK para expresiones aritméticas
# Gramática en CNF (Chomsky Normal Form):
#
#   E     → n | E EA | E EM
#   EA    → PLUS E
#   EM    → TIMES E
#   PLUS  → +
#   TIMES → *
#
# Verificación CNF:
#   Toda producción es A → a (terminal) o A → BC (dos no-terminales) ✓

GRAMMAR_CNF = {
    'E':     [['n'], ['E', 'EA'], ['E', 'EM']],
    'EA':    [['PLUS', 'E']],
    'EM':    [['TIMES', 'E']],
    'PLUS':  [['+']],
    'TIMES': [['*']],
}

START = 'E'


def tokenize(expr):
    """Convierte '3 + 5 * 2' → ['n', '+', 'n', '*', 'n']"""
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            tokens.append('n')
            while i + 1 < len(expr) and expr[i + 1].isdigit():
                i += 1
            i += 1
        elif c in '+-*':
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"Token no reconocido: '{c}'")
    return tokens


def cyk_parse(tokens):
    """
    Algoritmo CYK — O(n³ · |G|)
    Retorna True si tokens pertenece al lenguaje generado por START.
    """
    n = len(tokens)
    if n == 0:
        return False

    # dp[i][j] = conjunto de NT que derivan tokens[i..j] (inclusive)
    dp = [[set() for _ in range(n)] for _ in range(n)]

    # Caso base: substrings de longitud 1
    for i, tok in enumerate(tokens):
        for nt, prods in GRAMMAR_CNF.items():
            if [tok] in prods:
                dp[i][i].add(nt)

    # Llenar substrings de longitud 2 en adelante
    for length in range(2, n + 1):          # longitud de la subcadena
        for i in range(n - length + 1):     # inicio
            j = i + length - 1              # fin
            for k in range(i, j):           # punto de corte
                for nt, prods in GRAMMAR_CNF.items():
                    for prod in prods:
                        if len(prod) == 2:
                            B, C = prod
                            if B in dp[i][k] and C in dp[k + 1][j]:
                                dp[i][j].add(nt)

    return START in dp[0][n - 1]


if __name__ == '__main__':
    import time

    test_cases = [
        ("1 + 2",             True),
        ("3 * 4",             True),
        ("1 + 2 + 3",         True),
        ("1 + 2 * 3",         True),
        ("10 * 20 + 30",      True),
        ("1 + 2 + 3 + 4 + 5", True),
        ("+",                  False),
        ("1 +",                False),
        ("* 2",                False),
    ]

    print(f"{'Expresión':<30} {'Esperado':>10} {'Resultado':>10} {'Tiempo (ms)':>12}")
    print("-" * 66)

    for expr, expected in test_cases:
        try:
            toks = tokenize(expr)
            start = time.perf_counter()
            result = cyk_parse(toks)
            elapsed = time.perf_counter() - start
        except ValueError:
            result = False
            elapsed = 0.0

        match = "✓" if result == expected else "✗"
        print(f"{match} {expr:<28} {'Sí' if expected else 'No':>10} {'Sí' if result else 'No':>10} {elapsed*1000:>12.4f}")
