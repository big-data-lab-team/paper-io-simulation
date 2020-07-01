import matplotlib.pyplot as plt
import numpy as np


def plot_mem_log(mem_log, time_stamps, text, xmin, xmax, ymin, ymax):
    time = mem_log["time"]
    total = mem_log["total"]
    free = mem_log["free"]
    used = mem_log["used"]
    cache = mem_log["cache"]
    dirty = mem_log["dirty"]
    available = list(np.array(free) + np.array(cache) - np.array(dirty))
    dirty_ratio = list(np.array(available) * 0.4)
    dirty_bg_ratio = list(np.array(available) * 0.1)

    read_start = time_stamps["read_start"]
    read_end = time_stamps["read_end"]
    write_start = time_stamps["write_start"]
    write_end = time_stamps["write_end"]
    start = read_start[0]

    plt.figure()
    plt.title("python simulator result")

    for idx in range(len(read_start)):
        if idx == 0:
            plt.axvspan(xmin=read_end[idx] - start, xmax=write_start[idx] - start, color="k",
                        alpha=0.2, label="computation")
            plt.axvspan(xmin=0, xmax=read_end[idx] - start, color="g", alpha=0.2, label="read")
            plt.axvspan(xmin=write_start[idx] - start, xmax=write_end[idx] - start, color="b", alpha=0.2, label="write")
        else:
            plt.axvspan(xmin=read_end[idx] - start, xmax=write_start[idx] - start, color="k", alpha=0.2)
            plt.axvspan(xmin=read_start[idx] - start, xmax=read_end[idx] - start, color="g", alpha=0.2)
            plt.axvspan(xmin=write_start[idx] - start, xmax=write_end[idx] - start, color="b", alpha=0.2)

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
    plt.text(1, 200000, text, fontsize=9)

    plt.show()
