# Punto 3 — Demostración LL(1)
# Gramática:
#   S -> AaAb | BbBa
#   A -> epsilon
#   B -> epsilon
# Ejecutar: python punto3_ll1_demo.py

GRAMMAR = {
    'S': [['A', 'a', 'A', 'b'], ['B', 'b', 'B', 'a']],
    'A': [['epsilon']],
    'B': [['epsilon']],
}

NON_TERMINALS = set(GRAMMAR.keys())
START = 'S'


def is_terminal(symbol):
    return symbol not in NON_TERMINALS and symbol != 'epsilon'


def first_of_sequence(seq, first_sets):
    result = set()
    for symbol in seq:
        if symbol == 'epsilon':
            result.add('epsilon')
            return result
        if is_terminal(symbol):
            result.add(symbol)
            return result
        result.update(first_sets[symbol] - {'epsilon'})
        if 'epsilon' not in first_sets[symbol]:
            return result
    result.add('epsilon')
    return result


def compute_first():
    first = {nt: set() for nt in GRAMMAR}
    changed = True
    while changed:
        changed = False
        for nt, productions in GRAMMAR.items():
            for prod in productions:
                if prod == ['epsilon']:
                    if 'epsilon' not in first[nt]:
                        first[nt].add('epsilon')
                        changed = True
                    continue
                for symbol in prod:
                    if is_terminal(symbol):
                        if symbol not in first[nt]:
                            first[nt].add(symbol)
                            changed = True
                        break
                    else:
                        added = first[symbol] - {'epsilon'} - first[nt]
                        if added:
                            first[nt].update(added)
                            changed = True
                        if 'epsilon' not in first[symbol]:
                            break
                else:
                    if 'epsilon' not in first[nt]:
                        first[nt].add('epsilon')
                        changed = True
    return first


def compute_follow(first_sets):
    follow = {nt: set() for nt in GRAMMAR}
    follow[START].add('$')
    changed = True
    while changed:
        changed = False
        for nt, productions in GRAMMAR.items():
            for prod in productions:
                if prod == ['epsilon']:
                    continue
                for i, symbol in enumerate(prod):
                    if symbol not in NON_TERMINALS:
                        continue
                    rest = prod[i + 1:]
                    f = first_of_sequence(rest, first_sets) if rest else {'epsilon'}
                    before = len(follow[symbol])
                    follow[symbol].update(f - {'epsilon'})
                    if 'epsilon' in f:
                        follow[symbol].update(follow[nt])
                    if len(follow[symbol]) > before:
                        changed = True
    return follow


def build_ll1_table(first_sets, follow_sets):
    table = {}
    for nt, productions in GRAMMAR.items():
        for prod in productions:
            if prod == ['epsilon']:
                first_prod = {'epsilon'}
            else:
                first_prod = first_of_sequence(prod, first_sets)
            for terminal in first_prod - {'epsilon'}:
                key = (nt, terminal)
                if key in table:
                    table[key].append(prod)
                else:
                    table[key] = [prod]
            if 'epsilon' in first_prod:
                for terminal in follow_sets[nt]:
                    key = (nt, terminal)
                    if key in table:
                        table[key].append(['epsilon'])
                    else:
                        table[key] = [['epsilon']]
    return table


def print_table(table, terminals):
    col_w = 18
    header = f"{'':6}" + "".join(f"{('[' + t + ']'):<{col_w}}" for t in terminals)
    print(header)
    print("-" * (6 + col_w * len(terminals)))
    for nt in sorted(GRAMMAR.keys()):
        row = f"{nt:<6}"
        for t in terminals:
            key = (nt, t)
            if key in table:
                prods = table[key]
                cell = f"{nt}→{'|'.join(' '.join(p) for p in prods)}"
                if len(prods) > 1:
                    cell += " !!CONFLICTO"
            else:
                row += f"{'':>{col_w}}"
                continue
            row += f"{cell:<{col_w}}"
        print(row)


def main():
    print("Gramática:")
    print("  S → AaAb | BbBa")
    print("  A → epsilon")
    print("  B → epsilon")

    first_sets = compute_first()
    print("\n── Conjuntos FIRST ──")
    for nt in sorted(GRAMMAR.keys()):
        print(f"  FIRST({nt}) = {sorted(first_sets[nt])}")

    follow_sets = compute_follow(first_sets)
    print("\n── Conjuntos FOLLOW ──")
    for nt in sorted(GRAMMAR.keys()):
        print(f"  FOLLOW({nt}) = {sorted(follow_sets[nt])}")

    terminals = sorted({'a', 'b', '$'})
    table = build_ll1_table(first_sets, follow_sets)
    print("\n── Tabla predictiva LL(1) ──")
    print_table(table, terminals)


if __name__ == '__main__':
    main()
