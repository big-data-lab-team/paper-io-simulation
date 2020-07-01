import log_parse
import matplotlib.pyplot as plt
import numpy as np


def get_atop_mem_prop(time_log, mem_log, key):
    """
    :param time_log: real time log tuple
    :param mem_log: real mem log dictionary
    :param key: key of the memory property to be returned
    :return: list of values of mem properties corresponding to task end time in log
    """

    task_ends = [task[2] for task in time_log]
    start = time_log[0][1]

    arr = mem_log[key]
    result = []
    for i in range(len(task_ends)):
        time = task_ends[i] - start
        prop = arr[int(time)] + (arr[int(time) + 1] - arr[int(time)]) * (time - int(time))
        result.append(prop)

    return result


def get_sim_mem_prop(time_log, mem_log, key):
    """
    :param time_log: simulation time log tuple
    :param mem_log: simulation mem log dictionary
    :param key: key of the memory property to be returned
    :return: list of values of mem properties corresponding to task end time in log
    """

    task_ends = [task[2] for task in time_log]
    result = []
    for i in range(len(task_ends)):
        idx = mem_log["time"].index(task_ends[i])
        if idx >= 0:
            result.append(mem_log[key][idx])
        else:
            result.append(-1000)

    return result


def task_time_error(realtime_logfile, simtime_logfile):
    real_time = log_parse.read_timelog(realtime_logfile, skip_header=False)
    sim_time = log_parse.read_timelog(simtime_logfile)

    time_acc = []

    for i in range(len(sim_time)):
        sim = sim_time[i][2] - sim_time[i][1]
        real = real_time[i][2] - real_time[i][1]
        time_acc.append(abs(sim - real) / real)

    return time_acc


def mem_error(real_time_logfile, sim_time_logfile, real_mem_logfile, sim_mem_logfile):
    real_time_log = log_parse.read_timelog(real_time_logfile, skip_header=False)
    real_mem_log = log_parse.read_atop_log(real_mem_logfile)

    dirty_origin = real_mem_log["dirty_data"][0]
    cache_origin = real_mem_log["cache"][0]

    real_dirty_amt = [amt for amt in get_atop_mem_prop(real_time_log, real_mem_log, "dirty_data")]
    real_cache_amt = [amt for amt in get_atop_mem_prop(real_time_log, real_mem_log, "cache")]

    # print(dirty_origin)
    print("real:")
    print(get_atop_mem_prop(real_time_log, real_mem_log, "dirty_data"))
    # print(real_mem_log["dirty_data"])

    sim_time_log = log_parse.read_timelog(sim_time_logfile)
    sim_mem_log = log_parse.read_sim_log(sim_mem_logfile)

    sim_dirty_amt = get_sim_mem_prop(sim_time_log, sim_mem_log, "dirty_data")
    sim_cache_amt = get_sim_mem_prop(sim_time_log, sim_mem_log, "cache")

    print("sim:")
    print(sim_dirty_amt)

    dirty_err = [abs(sim - real) / real for real, sim in zip(real_dirty_amt, sim_dirty_amt)]
    cache_err = [abs(sim - real) / real for real, sim in zip(real_cache_amt, sim_cache_amt)]

    return dirty_err, cache_err


def grouped_bar_chart(labels, title, xlabel, ylabel, *argv):
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    bars = len(argv)

    fig, ax = plt.subplots()
    for i in range(len(argv)):
        arg = argv[i]
        ax.bar(x + (2 * i + 1 - bars) * width / 2, arg[1], width, label=arg[0])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(bottom=0, top=8)
    ax.legend()

    plt.show()


def plot_task_error(size):
    labels = ["read1", "write1", "read2", "write2", "read3", "write3"]

    # atop_file =     "log/cluster/100gb/atop_mem.log"
    real_time_log = "real_log/ex1/%dgb/timestamps_pipeline.csv" % size
    sim_py_log = "py_log/ex1/new/%dgb_sim_time.csv" % size
    simgrid_log = "simgrid/ex1/timestamp_sim_exp1_%dgb.csv" % size

    py_error = task_time_error(real_time_log, sim_py_log)
    simgrid_error = task_time_error(real_time_log, simgrid_log)

    grouped_bar_chart(labels, "Simulation error of tasks with %dGB" % size, "tasks", "error",
                      ("Python", py_error), ("Original SimGrid", simgrid_error))


sizes = [20, 50, 75, 100]
for size in sizes:
    plot_task_error(size)

# dirty_acc, cache_acc = mem_error(real_time_log, sim_time_log, atop_file, sim_logfile)


# print("\nTime error:")
# print(time_acc)

# print("\nDirty data error:")
# print(dirty_acc)
#
# print("\nCache error:")
# print(cache_acc)
