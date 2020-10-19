import pandas as pd
import matplotlib.pyplot as plt


def plot_cache(file, source):
    columns = ["read1", "write1", "read2", "write2", "read3", "write3"]
    files = ["file1", "file2", "file3", "file4"]

    if source == "real":
        df = pd.read_csv("fincore/real.csv", index_col="task")
    if source == "wrench":
        df = pd.read_csv("fincore/sim.csv", index_col="task")

    patterns = ["", "...", "///", "\\\\\\"]

    # axe = df_real[files].plot.bar(stacked=True, rot=0, color="tab:purple", edgecolor="k")
    axe = df[files].plot.bar(stacked=True, rot=0, color="tab:purple", edgecolor="k")

    bars = axe.patches
    hatches = []  # list for hatches in the order of the bars
    for h in patterns:  # loop over patterns to create bar-ordered hatches
        for i in range(int(len(bars) / len(patterns))):
            hatches.append(h)
    for bar, hatch in zip(bars, hatches):  # loop over bars and hatches to set hatches in correct order
        bar.set_hatch(hatch)

    plt.subplots_adjust(left=0.12, bottom=0.15, right=0.92, top=0.9)

    plt.xlabel("")
    plt.ylabel("amount (GB)")

    legend = plt.legend()
    l_hatches = []
    legends = legend.axes.patches
    for h in patterns:  # loop over patterns to create bar-ordered hatches
        for i in range(int(len(legends) / len(patterns))):
            l_hatches.append(h)
    for bar, hatch in zip(legends, l_hatches):  # loop over bars and hatches to set hatches in correct order
        bar.set_hatch(hatch)

    plt.savefig("figures/fincore_%s.svg" % source, format="svg")
    plt.savefig("figures/fincore_%s.pdf" % source, format="pdf")

    plt.show()


plot_cache("fincore/real.csv", "real")
plot_cache("fincore/wrench.csv", "wrench")
