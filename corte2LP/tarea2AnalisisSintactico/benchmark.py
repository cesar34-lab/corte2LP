import time
import tracemalloc


def measure_time(parser, string):
    start = time.perf_counter()
    parser.parse(string)
    end = time.perf_counter()
    return end - start


def measure_memory(parser, string):
    tracemalloc.start()
    parser.parse(string)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak
