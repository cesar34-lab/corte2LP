from typing import List, Tuple, Dict
from tree import ParseTree


class CFGParser:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.memo: Dict[Tuple[str, Tuple[str, ...]], List[ParseTree]] = {}

    def parse(self, tokens: List[str]):
        self.memo.clear()
        return self._parse_symbol(self.start_symbol, tuple(tokens))

    def _parse_symbol(self, symbol: str, tokens: Tuple[str, ...]):
        key = (symbol, tokens)

        if key in self.memo:
            return self.memo[key]

        trees = []

        for production in self.grammar.get_productions(symbol):
            if len(production) == 1:
                rhs = production[0]

                if len(tokens) == 1 and tokens[0] == rhs:
                    trees.append(ParseTree(symbol, [rhs]))
                elif rhs.isupper():
                    subtrees = self._parse_symbol(rhs, tokens)
                    for st in subtrees:
                        trees.append(ParseTree(symbol, [st]))
            elif len(production) == 3:
                left, op, right = production

                for i in range(len(tokens)):
                    if tokens[i] == op:
                        left_tokens = tokens[:i]
                        right_tokens = tokens[i + 1:]

                        if not left_tokens or not right_tokens:
                            continue

                        left_trees = self._parse_symbol(left, left_tokens)
                        right_trees = self._parse_symbol(right, right_tokens)

                        for lt in left_trees:
                            for rt in right_trees:
                                trees.append(ParseTree(symbol, [lt, op, rt]))

        self.memo[key] = trees
        return trees
