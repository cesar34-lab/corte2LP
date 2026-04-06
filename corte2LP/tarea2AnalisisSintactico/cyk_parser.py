import sys
from typing import Dict, List, Set, Tuple


class CYKParser:
    def __init__(self):
        self.grammar: Dict[str, List[Tuple[str, str]]] = {}
        self.terminals: Dict[str, List[str]] = {}

    def load_grammar(self, path: str):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or "->" not in line:
                    continue

                left, right = line.split("->")
                left = left.strip()
                symbols = right.strip().split()

                if len(symbols) == 1 and not symbols[0].isupper():
                    self.terminals.setdefault(left, []).append(symbols[0])
                elif len(symbols) == 2:
                    self.grammar.setdefault(left, []).append((symbols[0], symbols[1]))

    def parse(self, string: str) -> bool:
        n = len(string)
        if n == 0:
            return False

        table: List[List[Set[str]]] = [
            [set() for _ in range(n)] for _ in range(n)
        ]

        for i, char in enumerate(string):
            for var, terms in self.terminals.items():
                if char in terms:
                    table[i][i].add(var)

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for A, productions in self.grammar.items():
                        for B, C in productions:
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(A)

        return "S" in table[0][n - 1]


def main():
    if len(sys.argv) != 3:
        print("Usage: python cyk_parser.py grammar.txt cadena.txt")
        sys.exit(1)

    grammar_file = sys.argv[1]
    input_file = sys.argv[2]

    parser = CYKParser()
    parser.load_grammar(grammar_file)

    with open(input_file, "r") as f:
        string = f.read().strip()

    result = parser.parse(string)
    print("Accepted" if result else "Rejected")


if __name__ == "__main__":
    main()
