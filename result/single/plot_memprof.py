import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import log_parse


def compare_size(axes, real_time_file, real_mem_file,
                 pysim_time_file, pysim_mem_file,
                 simgrid_time_file, simgrid_mem_file,
                 size, title, xmin, xmax, ymin, ymax,
                 real_cond=None, py_cond=None, wrench_cond=None, label=False):
    # REAL RESULTS
    real_subplot(axes[0], real_time_file, real_mem_file, xmin, xmax, ymin, ymax, bar_alpha=0.2, linestyle="-",
                 linewidth=3, cond_text=real_cond)

    # SIMULATION RESULTS
    sim_subplot(axes[1], pysim_time_file, pysim_mem_file, "Python prototype", bar_alpha=0.2, cond_text=py_cond,
                color='deeppink')
    sim_subplot(axes[2], simgrid_time_file, simgrid_mem_file, "WRENCH-cache", bar_alpha=0.2,
                cond_text=wrench_cond, color='darkcyan')

    for ax in axes:
        ax.set_xlim(right=xmax, left=xmin)

    axes[2].set_xlabel('time (s)', fontsize=10)
    axes[0].text(0.45 * xmax, 300, "%d GB" % size, fontsize=14)

    if label:

        axes[0].text(1.04 * xmax, 30, 'Real execution', fontsize=12, color='white', bbox={'pad': 5, 'color': '#90C987'},
                     rotation=-90)
        axes[1].text(1.04 * xmax, 15, 'Python prototype', fontsize=12, color='white',
                     bbox={'pad': 5, 'color': '#7BAFDE'},
                     rotation=-90)
        axes[2].text(1.04 * xmax, 25, 'WRENCH-cache', fontsize=12, color='white', bbox={'pad': 5, 'color': '#1965B0'},
                     rotation=-90)
    # else:
    #     axes[0].set_title('Real execution')
    #     axes[1].set_title('Python prototype')
    #     axes[2].set_title('WRENCH-cache')
    #
    #     axes[1].set_ylabel('memory (GB)', fontsize=10)


def real_subplot(subplot_ax, real_time_file, real_mem_file, xmin, xmax, ymin, ymax,
                 bar_alpha=0.2, line_alpha=1, linestyle=".-", linewidth=2, cond_text=None):
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
                               label="Compute" if i == 1 else "")
            subplot_ax.axvspan(xmin=timestamps[i][1] - start, xmax=timestamps[i][2] - start, color="k", alpha=0.4,
                               label="write" if i == 1 else "")

    # app_cache = list(np.array(app_mem) + np.array(cache_used))
    subplot_ax.plot(time, atop_log["total"], color='black', linewidth=linewidth, label="Total memory",
                    alpha=line_alpha)
    subplot_ax.plot(time, atop_log["dirty_ratio"], color='black', linewidth=linewidth, linestyle=":",
                    label="dirty_ratio", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["used_mem"], color='#72190E', linewidth=linewidth, linestyle=linestyle,
                    label="Used memory", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["cache"], color='#DC050C', linewidth=linewidth, linestyle=linestyle,
                    label="Cache", alpha=line_alpha)
    subplot_ax.plot(time, atop_log["dirty_data"], color='#F4A736', linewidth=linewidth, linestyle=linestyle,
                    label="Dirty data", alpha=line_alpha)
    # subplot_ax.plot(time, atop_log["avai_mem"], color='#FDB36', linewidth=linewidth, linestyle=linestyle,
    #                 label="Available memory", alpha=line_alpha)

    # subplot_ax.plot(time, atop_log["dirty_bg_ratio"], color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio",
    #                 alpha=alpha)
    # subplot_ax.set_title("Real execution", fontsize=12)

    # if cond_text is not None:
    #     subplot_ax.text(120, 125, cond_text, style='italic', fontsize=10,
    #                     bbox={'alpha': 0.1, 'pad': 5})


def sim_subplot(subplot_ax, sim_time_file, sim_mem_file, title, bar_alpha=0.4, line_alpha=1, cond_text=None,
                color=None):
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
                               alpha=0.25, label="Compute")
            subplot_ax.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="k", alpha=0.4,
                               label="Write")
        else:
            subplot_ax.axvspan(xmin=read_starts[idx] - start, xmax=read_ends[idx] - start, color="k", alpha=0.1)
            subplot_ax.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k", alpha=0.25)
            subplot_ax.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="k", alpha=0.4)

    lw = 3
    subplot_ax.plot(time, total, color='black', linewidth=lw, label="Total memory", alpha=line_alpha)
    subplot_ax.plot(time, dirty_ratio, color='black', linewidth=lw, linestyle=":", label="dirty_ratio",
                    alpha=line_alpha)
    subplot_ax.plot(time, used, color='#72190E', linewidth=lw, label="Used memory", alpha=line_alpha)
    subplot_ax.plot(time, cache, color='#DC050C', linewidth=lw, label="Cache", alpha=line_alpha)
    subplot_ax.plot(time, dirty, color='#F4A736', linewidth=lw, label="Dirty data", alpha=line_alpha)
    # subplot_ax.plot(time, available, color='#FDB366', linewidth=lw, label="Available memory", alpha=line_alpha)
    # subplot_ax.plot(time, dirty_bg_ratio, color='r', linewidth=1, label="dirty_bg_ratio", alpha=alpha)

    # subplot_ax.set_title(title, fontsize=12, fontdict={'color': color})

    # if cond_text is not None:
    #     subplot_ax.text(135, 140, cond_text, style='italic', fontsize=10,
    #                     bbox={'alpha': 0.2, 'pad': 5})


def single_plot(input_size=20, makespan=165):
    fig, axes = plt.subplots(figsize=(9, 9), ncols=1, nrows=3)
    plt.subplots_adjust(top=0.85, hspace=0.3)
    plt.rcParams.update({'font.size': 10})

    compare_size([axes[0], axes[1], axes[2]],
                 real_time_file="real/%dgb/timestamps.csv" % input_size,
                 real_mem_file="real/%dgb/atop_mem.log" % input_size,
                 pysim_time_file="pysim/%dgb_sim_time.csv" % input_size,
                 pysim_mem_file="pysim/%dgb_sim_mem.csv" % input_size,
                 simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % input_size,
                 simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % input_size,
                 size=input_size, title="", xmin=0, xmax=makespan, ymin=-1000, ymax=280000,
                 label=False)

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.48, 4.05), ncol=4)
    axes[0].text(0.25 * makespan, 450, "Memory profile with %GB input" % input_size, fontsize=14)

    plt.savefig("figures/single_memprof_%d.svg" % input_size, format="svg", bbox_inches='tight')
    plt.savefig("figures/single_memprof_%d.pdf" % input_size, format="pdf", bbox_inches='tight')
    plt.show()


def compare_plot(input_sizes=[20, 100], makespan=[165, 1300]):
    fig, axes = plt.subplots(figsize=(15, 9), ncols=2, nrows=3)
    plt.subplots_adjust(hspace=0.3, wspace=0.1)
    plt.rcParams.update({'font.size': 10})

    real_condition_desc = "memory read bw = 6860 MBps\nmemory write bw = 2764 MBps\ndisk read bw = 510 MBps\ndisk write bw = 420 MBps"
    py_condition_desc = "memory bw = 4812MBps\ndisk bw = 465 MBps"
    wrench_condition_desc = "memory bw = 4812MBps\ndisk bw = 465 MBps"

    compare_size([axes[0][0], axes[1][0], axes[2][0]],
                 real_time_file="real/%dgb/timestamps.csv" % input_sizes[0],
                 real_mem_file="real/%dgb/atop_mem.log" % input_sizes[0],
                 pysim_time_file="pysim/%dgb_sim_time.csv" % input_sizes[0],
                 pysim_mem_file="pysim/%dgb_sim_mem.csv" % input_sizes[0],
                 simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % input_sizes[0],
                 simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % input_sizes[0],
                 size=input_sizes[0], title="", xmin=0, xmax=makespan[0], ymin=-1000, ymax=280000,
                 real_cond=real_condition_desc,
                 py_cond=py_condition_desc,
                 wrench_cond=wrench_condition_desc)
    compare_size([axes[0][1], axes[1][1], axes[2][1]],
                 real_time_file="real/%dgb/timestamps.csv" % input_sizes[1],
                 real_mem_file="real/%dgb/atop_mem.log" % input_sizes[1],
                 pysim_time_file="pysim/%dgb_sim_time.csv" % input_sizes[1],
                 pysim_mem_file="pysim/%dgb_sim_mem.csv" % input_sizes[1],
                 simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % input_sizes[1],
                 simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % input_sizes[1],
                 size=input_sizes[1], title="", xmin=0, xmax=makespan[1], ymin=-1000, ymax=280000, label=True)

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(-0.05, 4), ncol=8)

    # fig.text(0.32, 0.06, 'time (s)', ha='center', fontsize=12)
    # fig.text(0.73, 0.06, 'time (s)', ha='center', fontsize=12)
    # fig.text(0.08, 0.45, 'memory (GB)', va='center', rotation='vertical', fontsize=12)
    # fig.text(0.91, 0.7, 'Real execution', fontsize=14, color='white', bbox={'pad': 5, 'color': '#90C987'},
    #          rotation=-90)
    # fig.text(0.91, 0.41, 'Python prototype', fontsize=14, color='white', bbox={'pad': 5, 'color': '#7BAFDE'},
    #          rotation=-90)
    # fig.text(0.91, 0.14, 'WRENCH-cache', fontsize=14, color='white', bbox={'pad': 5, 'color': '#1965B0'}, rotation=-90)

    plt.savefig("figures/single_memprof.svg", format="svg", bbox_inches='tight')
    plt.savefig("figures/single_memprof.pdf", format="pdf", bbox_inches='tight')
    # plt.show()


def compare_full():
    input_sizes = [20, 50, 75, 100]
    makespan = [165, 500, 800, 1300]

    fig = plt.figure(figsize=(12, 16))
    outer = gridspec.GridSpec(ncols=2, nrows=2, wspace=0.15, hspace=0.2, left=0.05, right=0.95, bottom=0.1, top=0.9, figure=fig)
    plt.rcParams.update({'font.size': 10})

    # real_condition_desc = "memory read bw = 6860 MBps\nmemory write bw = 2764 MBps\ndisk read bw = 510 MBps\ndisk write bw = 420 MBps"
    # py_condition_desc = "memory bw = 4812MBps\ndisk bw = 465 MBps"
    # wrench_condition_desc = "memory bw = 4812MBps\ndisk bw = 465 MBps"

    for i in range(len(input_sizes)):
        file_size = input_sizes[i]
        inner = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=outer[i], wspace=0.2, hspace=0.25)

        axes = []
        for j in range(3):
            ax = plt.Subplot(fig, inner[j])
            axes.append(ax)
            fig.add_subplot(ax)

        compare_size([axes[0], axes[1], axes[2]],
                     real_time_file="real/%dgb/timestamps.csv" % file_size,
                     real_mem_file="real/%dgb/atop_mem.log" % file_size,
                     pysim_time_file="pysim/%dgb_sim_time.csv" % file_size,
                     pysim_mem_file="pysim/%dgb_sim_mem.csv" % file_size,
                     simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % file_size,
                     simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % file_size,
                     size=file_size, title="", xmin=0, xmax=makespan[i], ymin=-1000, ymax=280000, label=(i % 2 != 0))

    # compare_size([axes[0][1], axes[1][1], axes[2][1]],
    #              real_time_file="real/%dgb/timestamps.csv" % input_sizes[1],
    #              real_mem_file="real/%dgb/atop_mem.log" % input_sizes[1],
    #              pysim_time_file="pysim/%dgb_sim_time.csv" % input_sizes[1],
    #              pysim_mem_file="pysim/%dgb_sim_mem.csv" % input_sizes[1],
    #              simgrid_time_file="wrench/pagecache/%dgb_sim_time.csv" % input_sizes[1],
    #              simgrid_mem_file="wrench/pagecache/%dgb_sim_mem.csv" % input_sizes[1],
    #              size=input_sizes[1], title="", xmin=0, xmax=makespan[1], ymin=-1000, ymax=280000)

    lgd = plt.legend(loc='upper center', bbox_to_anchor=(-0.05, 8.25), ncol=8)

    # fig.text(0.91, 0.83, 'Real execution', fontsize=14, color='white', bbox={'pad': 5, 'color': '#90C987'},
    #          rotation=-90)
    # fig.text(0.91, 0.57, 'Python prototype', fontsize=14, color='white', bbox={'pad': 5, 'color': '#7BAFDE'},
    #          rotation=-90)
    # fig.text(0.91, 0.29, 'WRENCH-cache', fontsize=14, color='white', bbox={'pad': 5, 'color': '#1965B0'},
    #          rotation=-90)
    # fig.text(0.32, 0.06, 'time (s)', ha='center', fontsize=12)
    # fig.text(0.73, 0.06, 'time (s)', ha='center', fontsize=12)
    # fig.text(0.08, 0.45, 'memory (GB)', va='center', rotation='vertical', fontsize=12)

    plt.savefig("figures/single_memprof_full.svg", format="svg")
    plt.savefig("figures/single_memprof_full.pdf", format="pdf")
    # plt.show()
