import matplotlib.pyplot as plt
import numpy as np
import log_parse


def compare_size(axes, real_time_file, real_mem_file,
                 pysim_time_file, pysim_mem_file,
                 simgrid_time_file, simgrid_mem_file,
                 size, title, xmin, xmax, ymin, ymax):
    # REAL RESULTS
    real_subplot(axes[0], real_time_file, real_mem_file, xmin, xmax, ymin, ymax, bar_alpha=0.2, linestyle="-",
                 linewidth=1)

    # SIMULATION RESULTS
    sim_subplot(axes[1], pysim_time_file, pysim_mem_file, "Python simulator", bar_alpha=0.2)
    sim_subplot(axes[2], simgrid_time_file, simgrid_mem_file, "WRENCH-Ext simulator", bar_alpha=0.2)

    for ax in axes:
        ax.set_xlim(right=xmax, left=xmin)

    axes[2].set_xlabel("%d GB" % size)


def real_subplot(subplot_ax, real_time_file, real_mem_file, xmin, xmax, ymin, ymax,
                 bar_alpha=0.2, line_alpha=1, linestyle=".-", linewidth=1.5):
    timestamps = log_parse.read_timelog(real_time_file, skip_header=False)
    atop_log = log_parse.read_atop_log(real_mem_file, dirty_ratio=0.4, dirty_bg_ratio=0.1)
    dirty_data = np.array(atop_log["total"])
    intervals = len(dirty_data)
    time = np.arange(0, intervals)

    start = timestamps[0][1]

    for i in range(len(timestamps)):
        if timestamps[i][0] == "read":
            subplot_ax.axvspan(xmin=timestamps[i][1] - start, xmax=timestamps[i][2] - start, color="k", alpha=0.1,
                               label="Read" if i == 0 else "")
        else:
            subplot_ax.axvspan(xmin=timestamps[i - 1][2] - start, xmax=timestamps[i][1] - start, color="k", alpha=0.25,
                               label="Computation" if i == 1 else "")
            subplot_ax.axvspan(xmin=timestamps[i][1] - start, xmax=timestamps[i][2] - start, color="k", alpha=0.4,
                               label="write" if i == 1 else "")

    # app_cache = list(np.array(app_mem) + np.array(cache_used))
    subplot_ax.plot(time, atop_log["total"], color='k', linewidth=1, linestyle=":", label="Total memory",
                    alpha=line_alpha)
    subplot_ax.plot(time, atop_log["used_mem"], color='g', linewidth=linewidth, linestyle=linestyle,
                    label="Used memory", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["cache"], color='purple', linewidth=linewidth, linestyle=linestyle,
                    label="Cache", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["dirty_data"], color='r', linewidth=linewidth, linestyle=linestyle,
                    label="Dirty data", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["avai_mem"], color='b', linewidth=linewidth, linestyle=linestyle,
                    label="Available memory", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["dirty_ratio"], color='k', linewidth=linewidth, linestyle="-.",
                    label="dirty_ratio", alpha=line_alpha)
    # subplot_ax.plot(time, atop_log["dirty_bg_ratio"], color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio",
    #                 alpha=alpha)
    subplot_ax.set_title("Real execution", fontsize=10)


def sim_subplot(subplot_ax, sim_time_file, sim_mem_file, title, bar_alpha=0.4, line_alpha=1):
    sim_time_log = log_parse.read_timelog(sim_time_file)
    sim_mem_log = log_parse.read_sim_log(sim_mem_file)

    read_starts = []
    read_ends = []
    write_starts = []
    write_ends = []
    for i in range(len(sim_time_log)):
        if sim_time_log[i][0] == "read":
            read_starts.append(sim_time_log[i][1])
            read_ends.append(sim_time_log[i][2])
        if sim_time_log[i][0] == "write":
            write_starts.append(sim_time_log[i][1])
            write_ends.append(sim_time_log[i][2])

    time = sim_mem_log["time"]
    total = sim_mem_log["total"]
    cache = sim_mem_log["cache"]
    dirty = sim_mem_log["dirty"]
    used = sim_mem_log["used"]

    free = list(np.array(total) - np.array(used))
    available = list(np.array(free) + np.array(cache) - np.array(dirty))
    dirty_ratio = list(np.array(available) * 0.4)
    dirty_bg_ratio = list(np.array(available) * 0.1)

    start = read_starts[0]
    for idx in range(len(read_starts)):
        if idx == 0:
            subplot_ax.axvspan(xmin=0, xmax=read_ends[idx] - start, color="k", alpha=0.1, label="Read")
            subplot_ax.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k",
                               alpha=0.25, label="Computation")
            subplot_ax.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="k", alpha=0.4,
                               label="Write")
        else:
            subplot_ax.axvspan(xmin=read_starts[idx] - start, xmax=read_ends[idx] - start, color="k", alpha=0.1)
            subplot_ax.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k", alpha=0.25)
            subplot_ax.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="k", alpha=0.4)

    subplot_ax.plot(time, total, color='k', linewidth=1, linestyle=":", label="Total memory", alpha=line_alpha)
    subplot_ax.plot(time, used, color='g', linewidth=1, label="Used memory", alpha=line_alpha)
    subplot_ax.plot(time, cache, color='purple', linewidth=1, label="Cache", alpha=line_alpha)
    subplot_ax.plot(time, dirty, color='r', linewidth=1, label="Dirty data", alpha=line_alpha)
    subplot_ax.plot(time, available, color='b', linewidth=1, label="Available memory", alpha=line_alpha)
    subplot_ax.plot(time, dirty_ratio, color='k', linewidth=1, linestyle="-.", label="dirty_ratio", alpha=line_alpha)
    # subplot_ax.plot(time, dirty_bg_ratio, color='r', linewidth=1, label="dirty_bg_ratio", alpha=alpha)

    subplot_ax.set_title(title, fontsize=10)


def compare_plot(input_sizes=[20, 100], makespan=[200, 1300]):
    fig, axes = plt.subplots(figsize=(15, 8), ncols=2, nrows=3)
    plt.subplots_adjust(left=0.07, bottom=0.08, right=0.95, top=0.85, wspace=0.12, hspace=0.3)

    compare_size([axes[0][0], axes[1][0], axes[2][0]],
                 real_time_file="real/%dgb/timestamps.csv" % input_sizes[0],
                 real_mem_file="real/%dgb/atop_mem.log" % input_sizes[0],
                 pysim_time_file="pysim/%dgb_sim_time.csv" % input_sizes[0],
                 pysim_mem_file="pysim/%dgb_sim_mem.csv" % input_sizes[0],
                 simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % input_sizes[0],
                 simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % input_sizes[0],
                 size=input_sizes[0], title="", xmin=0, xmax=makespan[0], ymin=-1000, ymax=280000)
    compare_size([axes[0][1], axes[1][1], axes[2][1]],
                 real_time_file="real/%dgb/timestamps.csv" % input_sizes[1],
                 real_mem_file="real/%dgb/atop_mem.log" % input_sizes[1],
                 pysim_time_file="pysim/%dgb_sim_time.csv" % input_sizes[1],
                 pysim_mem_file="pysim/%dgb_sim_mem.csv" % input_sizes[1],
                 simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % input_sizes[1],
                 simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % input_sizes[1],
                 size=input_sizes[1], title="", xmin=0, xmax=makespan[1], ymin=-1000, ymax=280000)

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(-0.05, 4.2), ncol=3)

    fig.text(0.5, 0.02, 'time (s)', ha='center')
    fig.text(0.02, 0.5, 'memory (GB)', va='center', rotation='vertical')

    plt.savefig("figures/single_memprof.svg", format="svg")
    plt.savefig("figures/single_memprof.pdf", format="pdf")
    plt.show()
