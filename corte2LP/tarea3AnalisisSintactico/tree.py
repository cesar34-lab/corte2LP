class ParseTree:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []

    def __repr__(self):
        if not self.children:
            return self.symbol
        return f"({self.symbol} {' '.join(map(str, self.children))})"

    def pretty(self, level=0):
        indent = "  " * level
        result = indent + self.symbol + "\n"

        for child in self.children:
            if isinstance(child, ParseTree):
                result += child.pretty(level + 1)
            else:
                result += "  " * (level + 1) + child + "\n"

        return result
