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
                      ("Python prototype", py_error, "#7BAFDE"), ("WRENCH", wrench_org_error, '#994F88'),
                      ("WRENCH-cache", wrench_ext_error, '#1965B0'))
    ax.set_title("%d GB" % size)


def plot_error():
    fig, (ax1, ax2) = plt.subplots(figsize=(11, 3), ncols=2, nrows=1)
    plt.rcParams.update({'font.size': 10})

    plot_task_error(ax1, 20, ylabel=False)
    plot_task_error(ax2, 100, ylabel=False)

    fig.text(0.01, 0.5, 'error (%)', va='center', rotation='vertical')

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(-0.12, 2.6), ncol=3)
    plt.subplots_adjust(left=0.07, bottom=0.075, right=0.97, top=0.85, wspace=0.2, hspace=0.3)

    plt.savefig("figures/single_errors_v2.svg", format="svg", bbox_extra_artists=(lgd,))
    plt.savefig("figures/single_errors_v2.pdf", format="pdf", bbox_extra_artists=(lgd,))
    # plt.show()
