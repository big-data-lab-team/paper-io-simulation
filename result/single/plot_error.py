import evaluate
import matplotlib.pyplot as plt
import numpy as np


def grouped_bar_chart(labels, size, xlabel, ylabel, *argv):
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    bars = len(argv)

    fig, ax = plt.subplots()
    for i in range(len(argv)):
        arg = argv[i]
        ax.bar(x + (2 * i + 1 - bars) * width / 2, arg[1], width, label=arg[0], color=arg[2])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(bottom=0, top=800)
    if size == 20: ax.legend()
    plt.savefig("figures/error_%d.svg" % size, format="svg")
    plt.savefig("figures/error_%d.pdf" % size, format="pdf")
    plt.show()


def plot_task_error(size):
    labels = ["read1", "write1", "read2", "write2", "read3", "write3"]

    # atop_file =     "log/cluster/100gb/atop_mem.log"
    real_time_log = "real/%dgb/timestamps.csv" % size
    sim_py_log = "pysim/%dgb_sim_time.csv" % size
    simgrid_org_log = "wrench/original/%dgb_sim_time.csv" % size
    simgrid_ext_log = "wrench/pagecache/%dgb_sim_time.csv" % size

    py_error = [item * 100 for item in evaluate.task_time_error(real_time_log, sim_py_log)]
    simgrid_org_error = [item * 100 for item in evaluate.task_time_error(real_time_log, simgrid_org_log)]
    simgrid_ext_error = [item * 100 for item in evaluate.task_time_error(real_time_log, simgrid_ext_log)]

    grouped_bar_chart(labels, size, "", "error (%)",
                      ("Python simulator", py_error, "tab:blue"), ("Original WRENCH", simgrid_org_error, 'tab:orange'),
                      ("WRENCH simulator with page cache", simgrid_ext_error, 'tab:green'))


sizes = [20, 50, 75, 100]
for size in sizes:
    plot_task_error(size)
