# Punto 4 — Comparación de rendimiento CYK vs LL(1)
# Ejecutar: python3 comparison.py

import time

from cyk_parser import tokenize, cyk_parse
from predictive_parser import ll1_parse


def generate_expression(n_operands):
    return ' + '.join(['1'] * n_operands)


def measure(parse_fn, tokens, runs=10):
    total = 0.0
    for _ in range(runs):
        start = time.perf_counter()
        parse_fn(tokens)
        total += time.perf_counter() - start
    return total / runs


def run_comparison():
    sizes = [1, 5, 10, 20, 50, 100]

    print("=" * 70)
    print("Comparación de rendimiento: CYK vs Parser Predictivo LL(1)")
    print("Expresión de prueba: '1 + 1 + 1 + ... + 1' (n sumandos)")
    print("=" * 70)
    print(f"{'Operandos':>10} {'Tokens':>8} {'CYK (ms)':>12} {'LL(1) (ms)':>12} {'CYK/LL':>10}")
    print("-" * 56)

    for n in sizes:
        expr = generate_expression(n)
        tokens = tokenize(expr)
        n_tokens = len(tokens)

        cyk_t = measure(cyk_parse, tokens)
        ll1_t = measure(ll1_parse, tokens)

        ratio = cyk_t / ll1_t if ll1_t > 0 else float('inf')
        print(f"{n:>10} {n_tokens:>8} {cyk_t*1000:>12.4f} {ll1_t*1000:>12.4f} {ratio:>9.1f}x")


if __name__ == '__main__':
    run_comparison()
