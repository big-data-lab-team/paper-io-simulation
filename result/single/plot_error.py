import evaluate
import matplotlib.pyplot as plt
import numpy as np


def grouped_bar_chart(ax, labels, xlabel, ylabel, *argv):
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    bars = len(argv)

    for i in range(len(argv)):
        arg = argv[i]
        ax.bar(x + (2 * i + 1 - bars) * width / 2, arg[1], width, label=arg[0], color=arg[2])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(bottom=0, top=700)


def plot_task_error(ax, size, ylabel):
    labels = ["Read 1", "Write 1", "Read 2", "Write 2", "Read 3", "Write 3"]

    # atop_file =     "log/cluster/100gb/atop_mem.log"
    real_time_log = "real/%dgb/timestamps.csv" % size
    sim_py_log = "pysim/%dgb_sim_time.csv" % size
    wrench_org_log = "wrench/original/%dgb_sim_time.csv" % size
    wrench_ext_log = "wrench/pagecache/%dgb_sim_time.csv" % size

    py_error = [item * 100 for item in evaluate.task_time_error(real_time_log, sim_py_log)]
    wrench_org_error = [item * 100 for item in evaluate.task_time_error(real_time_log, wrench_org_log)]
    wrench_ext_error = [item * 100 for item in evaluate.task_time_error(real_time_log, wrench_ext_log)]

    if ylabel:
        ylabel = "error (%)"
    else:
        ylabel = ""
    grouped_bar_chart(ax, labels, "", ylabel,
                      ("Python prototype", py_error, "#994F88"), ("WRENCH", wrench_org_error, '#7BAFDE'),
                      ("WRENCH-cache", wrench_ext_error, '#1965B0'))
    ax.set_title("%d GB" % size)

def plot_error():
    fig, (ax1, ax2) = plt.subplots(figsize=(11, 3), ncols=2, nrows=1)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.8, wspace=0.1)
    plt.rcParams.update({'font.size': 9})

    plot_task_error(ax1, 20, ylabel=True)
    plot_task_error(ax2, 100, ylabel=False)

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(-0.12, 1.25), ncol=3)

    plt.savefig("figures/single_errors.svg", format="svg", bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.savefig("figures/single_errors.pdf", format="pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()
