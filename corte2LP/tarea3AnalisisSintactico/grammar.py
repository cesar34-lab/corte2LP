from collections import defaultdict
from typing import List, Dict


class Grammar:
    def __init__(self):
        self.productions: Dict[str, List[List[str]]] = defaultdict(list)

    def add_production(self, left: str, right: List[str]) -> None:
        self.productions[left].append(right)

    def get_productions(self, non_terminal: str) -> List[List[str]]:
        return self.productions[non_terminal]

    def __str__(self):
        result = []
        for left, rights in self.productions.items():
            for right in rights:
                result.append(f"{left} -> {' '.join(right)}")
        return "\n".join(result)
