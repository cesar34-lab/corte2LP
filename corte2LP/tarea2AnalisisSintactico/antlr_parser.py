import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser


def parse_input(text: str):
    input_stream = InputStream(text)
    lexer = ExprLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ExprParser(token_stream)
    tree = parser.expr()
    return tree, parser


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 antlr_parser.py Expr.g4 cadena.txt")
        sys.exit(1)

    input_file = sys.argv[2]

    with open(input_file, "r") as f:
        text = f.read().strip()

    tree, parser = parse_input(text)

    print("Parsed successfully")
    print(tree.toStringTree(recog=parser))


if __name__ == "__main__":
    main()
