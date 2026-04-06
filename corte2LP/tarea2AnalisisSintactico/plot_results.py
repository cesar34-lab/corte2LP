import matplotlib.pyplot as plt


def plot_results(sizes, cyk_times, antlr_times, cyk_mem, antlr_mem):
    plt.figure()
    plt.plot(sizes, cyk_times, label="CYK Time")
    plt.plot(sizes, antlr_times, label="ANTLR Time")
    plt.xlabel("Input Size")
    plt.ylabel("Time (seconds)")
    plt.title("Time Comparison")
    plt.legend()
    plt.show()

    plt.figure()
    plt.plot(sizes, cyk_mem, label="CYK Memory")
    plt.plot(sizes, antlr_mem, label="ANTLR Memory")
    plt.xlabel("Input Size")
    plt.ylabel("Memory (bytes)")
    plt.title("Memory Comparison")
    plt.legend()
    plt.show()
