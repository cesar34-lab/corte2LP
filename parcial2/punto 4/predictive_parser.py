# Punto 4 — Parser predictivo LL(1) para expresiones aritméticas
# Gramática (sin recursión izquierda):
#
#   E  → T E'
#   E' → + T E' | ε
#   T  → F T'
#   T' → * F T' | ε
#   F  → n
#
# Complejidad: O(n) — cada token se consume exactamente una vez

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


class PredictiveParser:
    def __init__(self, tokens):
        self.tokens = tokens + ['$']
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def consume(self, expected):
        if self.current() != expected:
            raise SyntaxError(
                f"Esperado '{expected}', encontrado '{self.current()}'"
            )
        self.pos += 1

    # E → T E'
    def parse_E(self):
        self.parse_T()
        self.parse_E_prime()

    # E' → + T E' | ε
    def parse_E_prime(self):
        if self.current() == '+':
            self.consume('+')
            self.parse_T()
            self.parse_E_prime()
        # ε: no hacer nada

    # T → F T'
    def parse_T(self):
        self.parse_F()
        self.parse_T_prime()

    # T' → * F T' | ε
    def parse_T_prime(self):
        if self.current() == '*':
            self.consume('*')
            self.parse_F()
            self.parse_T_prime()
        # ε

    # F → n
    def parse_F(self):
        if self.current() == 'n':
            self.consume('n')
        else:
            raise SyntaxError(
                f"Esperado número, encontrado '{self.current()}'"
            )

    def parse(self):
        self.parse_E()
        if self.current() != '$':
            raise SyntaxError(f"Token inesperado al final: '{self.current()}'")
        return True


def ll1_parse(tokens):
    """Retorna True si la secuencia de tokens es válida."""
    parser = PredictiveParser(tokens)
    parser.parse()
    return True


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
            result = ll1_parse(toks)
            elapsed = time.perf_counter() - start
        except (SyntaxError, ValueError):
            result = False
            elapsed = 0.0

        match = "✓" if result == expected else "✗"
        print(f"{match} {expr:<28} {'Sí' if expected else 'No':>10} {'Sí' if result else 'No':>10} {elapsed*1000:>12.4f}")
