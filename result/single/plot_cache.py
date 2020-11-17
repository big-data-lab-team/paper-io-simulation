import pandas as pd
import matplotlib.pyplot as plt


def plot_cache(real_file, sim_file):
    index = ["file_1", "file_2", "file_3", "file_4"]
    columns = ["Read 1", "Write 1", "Read 2", "Write 2", "Read 3", "Write 3"]
    files = ["file 1", "file 2", "file 3", "file 4"]

    df_real = pd.read_csv(real_file, index_col="task")
    df_sim = pd.read_csv(sim_file, index_col="task")

    patterns = ["", "...", "///", "\\\\\\"]

    plt.rcParams.update({'font.size': 8})
    fig, (ax1, ax2) = plt.subplots(figsize=(11, 4), ncols=2, nrows=1)
    plt.subplots_adjust(left=0.12, bottom=0.1, right=0.92, top=0.8)

    ax1 = df_real[index].plot.bar(stacked=True, rot=0, color="tab:cyan", edgecolor="k", ax=ax1,
                                  title="Real execution")
    ax2 = df_sim[index].plot.bar(stacked=True, rot=0, color="tab:cyan", edgecolor="k", ax=ax2,
                                 title="WRENCH with page cache", legend=False)

    ax1.set_xlabel("tasks")
    ax2.set_xlabel("tasks")
    ax1.set_ylabel("amount (GB)")
    ax2.set_ylabel("amount (GB)")
    ax1.set_xticklabels(columns)
    ax2.set_xticklabels(columns)

    bars = ax1.patches
    hatches = []  # list for hatches in the order of the bars
    for h in patterns:  # loop over patterns to create bar-ordered hatches
        for i in range(int(len(bars) / len(patterns))):
            hatches.append(h)
    for bar, hatch in zip(bars, hatches):  # loop over bars and hatches to set hatches in correct order
        bar.set_hatch(hatch)

    bars = ax2.patches
    hatches = []  # list for hatches in the order of the bars
    for h in patterns:  # loop over patterns to create bar-ordered hatches
        for i in range(int(len(bars) / len(patterns))):
            hatches.append(h)
    for bar, hatch in zip(bars, hatches):  # loop over bars and hatches to set hatches in correct order
        bar.set_hatch(hatch)

    legend = ax1.legend(files, loc='upper center', bbox_to_anchor=(1, 1.2), ncol=4)
    l_hatches = []
    legends = legend.axes.patches
    for h in patterns:  # loop over patterns to create bar-ordered hatches
        for i in range(int(len(legends) / len(patterns))):
            l_hatches.append(h)
    for bar, hatch in zip(legends, l_hatches):  # loop over bars and hatches to set hatches in correct order
        bar.set_hatch(hatch)

    plt.savefig("figures/cached_files.svg", format="svg")
    plt.savefig("figures/cached_files.pdf", format="pdf")

    plt.show()
