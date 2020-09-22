import matplotlib.pyplot as plt
import numpy as np
import log_parse


def plot_pysim_log(mem_log, time_stamps, text, xmin, xmax, ymin, ymax):
    time = mem_log["time"]
    total = mem_log["total"]
    dirty = mem_log["dirty"]
    cache = mem_log["cache"]
    used = mem_log["used"]
    # free = mem_log["free"]
    # available = list(np.array(free) + np.array(cache) - np.array(dirty))
    # dirty_ratio = list(np.array(available) * 0.4)
    # dirty_bg_ratio = list(np.array(available) * 0.1)

    read_starts = time_stamps["read_start"]
    read_ends = time_stamps["read_end"]
    write_starts = time_stamps["write_start"]
    write_ends = time_stamps["write_end"]

    plot_log(time, read_starts, read_ends, write_starts, write_ends, total, cache, dirty, used,
             "python simulator result", xmax, xmin, ymax, ymin)


def plot_sim_result(time_log_file, mem_log_file, title, xmin, xmax, ymin, ymax):
    sim_time_log = log_parse.read_timelog(time_log_file)

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

    sim_mem_log = log_parse.read_sim_log(mem_log_file)
    time = sim_mem_log["time"]
    total = sim_mem_log["total"]
    cache = sim_mem_log["cache"]
    dirty = sim_mem_log["dirty"]
    used = sim_mem_log["used"]

    plot_log(time, read_starts, read_ends, write_starts, write_ends, total, cache, dirty, used,
             title, xmax, xmin, ymax, ymin)


def plot_log(time, read_starts, read_ends, write_starts, write_ends, total, cache, dirty, used,
             title, xmax, xmin, ymax, ymin):
    free = list(np.array(total) - np.array(used))
    available = list(np.array(free) + np.array(cache) - np.array(dirty))
    dirty_ratio = list(np.array(available) * 0.4)
    dirty_bg_ratio = list(np.array(available) * 0.1)

    plt.figure()
    plt.title(title)

    start = read_starts[0]
    for idx in range(len(read_starts)):
        if idx == 0:
            plt.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k",
                        alpha=0.2, label="computation")
            plt.axvspan(xmin=0, xmax=read_ends[idx] - start, color="g", alpha=0.2, label="read")
            plt.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="b", alpha=0.2,
                        label="write")
        else:
            plt.axvspan(xmin=read_ends[idx] - start, xmax=write_starts[idx] - start, color="k", alpha=0.2)
            plt.axvspan(xmin=read_starts[idx] - start, xmax=read_ends[idx] - start, color="g", alpha=0.2)
            plt.axvspan(xmin=write_starts[idx] - start, xmax=write_ends[idx] - start, color="b", alpha=0.2)

    plt.plot(time, total, color='k', linewidth=1, linestyle="-.", label="total mem")
    plt.plot(time, used, color='g', linewidth=1, label="used mem")
    plt.plot(time, cache, color='m', linewidth=1, label="cache")
    plt.plot(time, dirty, color='r', linewidth=1, label="dirty")
    plt.plot(time, available, color='b', linewidth=1, linestyle="-.", label="available mem")
    plt.plot(time, dirty_ratio, color='k', linewidth=1, linestyle="-.", label="dirty_ratio")
    plt.plot(time, dirty_bg_ratio, color='r', linewidth=1, linestyle="-.", label="dirty_bg_ratio")
    plt.legend(loc="upper right")

    plt.ylim(top=ymax, bottom=ymin)
    plt.xlim(right=xmax, left=xmin)
    # plt.text(1, 200000, text, fontsize=9)

    plt.show()


# input_size = 50
# plot_sim_result("simgrid_ext/%dgb_sim_time.csv" % input_size, "simgrid_ext/%dgb_sim_mem.csv" % input_size,
#                     "Sim %dGB" % input_size, 0, 500, -1000, 280000)
