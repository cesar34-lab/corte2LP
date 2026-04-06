import time
import tracemalloc
from cyk_parser import CYKParser
from antlr_parser import parse_input
import matplotlib.pyplot as plt


def run_cyk(grammar_file, string_file):
    parser = CYKParser()
    parser.load_grammar(grammar_file)

    with open(string_file) as f:
        w = f.read().strip()

    tracemalloc.start()
    start = time.time()

    parser.parse(w)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return end - start, peak


def run_antlr(string_file):
    with open(string_file) as f:
        text = f.read().strip()

    tracemalloc.start()
    start = time.time()

    parse_input(text)

    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return end - start, peak


def main():
    grammar_file = "grammar.txt"
    string_file = "cadena.txt"

    cyk_time, cyk_mem = run_cyk(grammar_file, string_file)
    antlr_time, antlr_mem = run_antlr(string_file)

    print("CYK time:", cyk_time)
    print("CYK memory:", cyk_mem)
    print("ANTLR time:", antlr_time)
    print("ANTLR memory:", antlr_mem)

    labels = ["CYK", "ANTLR"]
    times = [cyk_time, antlr_time]
    memory = [cyk_mem, antlr_mem]

    plt.figure()
    plt.bar(labels, times)
    plt.title("Execution Time Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Time (seconds)")
    plt.show()

    plt.figure()
    plt.bar(labels, memory)
    plt.title("Memory Usage Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Memory (bytes)")
    plt.show()


if __name__ == "__main__":
    main()
