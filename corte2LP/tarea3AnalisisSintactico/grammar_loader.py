from grammar import Grammar


def load_grammar(file_path: str) -> Grammar:
    grammar = Grammar()

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "->" not in line:
                raise ValueError(f"Invalid production: {line}")

            left, right = line.split("->")
            left = left.strip()
            right_symbols = right.strip().split()

            grammar.add_production(left, right_symbols)

    return grammar
