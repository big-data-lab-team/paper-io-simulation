import json
import matplotlib.pyplot as plt
import numpy as np

def parse_time_real(logfile, sum_file):
    with open(logfile, "r") as logfile:
        log = json.load(logfile)

        summary = {}
        for task in log:
            makespan = log[task]["makespan"][0]["duration"]

            read_total = 0
            write_total = 0
            for fileread in log[task]["read"]:
                read_total += fileread["duration"]
            for filewrite in log[task]["write"]:
                write_total += filewrite["duration"]

            summary[task] = {
                "cputime": makespan - read_total - write_total,
                "read": read_total,
                "write": write_total
            }

    with open(sum_file, "w") as outfile:
        json.dump(summary, outfile)


def parse_time_wrench(dumpfile, sum_file):
    with open(dumpfile, "r") as logfile:
        log = json.load(logfile)

        summary = {}
        for task in log["workflow_execution"]["tasks"]:
            makespan = task["whole_task"]["end"] - task["whole_task"]["start"]

            read_start = min(read["start"] for read in task["read"])
            read_end = max(read["end"] for read in task["read"])
            read_duration = read_end - read_start

            write_start = min(write["start"] for write in task["write"])
            write_end = max(write["end"] for write in task["write"])
            write_duration = write_end - write_start

            summary[task["task_id"]] = {
                "cputime": makespan - write_duration - read_duration,
                "read": read_duration,
                "write": write_duration
            }

    with open(sum_file, "w") as outfile:
        json.dump(summary, outfile)


def parse_task_real(logfile, sum_file):
    with open(logfile, "r") as logfile:
        log = json.load(logfile)

        summary = {}
        for task in log:
            _input = {}
            _output = {}
            for fileread in log[task]["read"]:
                _input[fileread["filename"]] = fileread["filesize"]
            for filewrite in log[task]["write"]:
                _output[filewrite["filename"]] = filewrite["filesize"]

            summary[task] = {
                "input": _input,
                "output": _output
            }

    with open(sum_file, "w") as outfile:
        json.dump(summary, outfile)


def grouped_bar_chart(ax, labels, xlabel, ylabel, *argv):
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    bars = len(argv)

    for i in range(len(argv)):
        arg = argv[i]
        plt.bar(x + (2 * i + 1 - bars) * width / 2, arg[1], width, label=arg[0], color=arg[2])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(bottom=0)


def plot_error():
    real_log_file = "real/timelog_sub001_sess1.json"
    real_time_file = "real/summary_real_time_sub001_sess1.json"

    wrench_log_file = "wrench/original/dump_nighres_original_sim_time.json"
    wrench_time_file = "wrench/original/summary_wrench_nighres_original.json"

    wrench_cache_log_file = "wrench/pagecache/dump_nighres_pagecache_sim_time.json"
    wrench_cache_time_file = "wrench/pagecache/summary_wrench_nighres_pagecache.json"

    parse_time_real(real_log_file, real_time_file)
    parse_task_real(real_log_file, "real/summary_file_sub001_sess1.json")

    parse_time_wrench(wrench_log_file, wrench_time_file)
    parse_time_wrench(wrench_cache_log_file, wrench_cache_time_file)

    tasks = ["mp2rage_skullstripping", "mgdm_segmentation", "extract_brain_region", "cruise_cortex_extraction"]

    # reads_real = []
    # reads_wrench = []
    # reads_wrench_cache = []
    # writes_real = []
    # writes_wrench = []
    # writes_wrench_cache = []

    real_arr = []
    wrench_arr = []
    wrench_cache_arr = []

    with open(real_time_file, "r") as time_file:
        real = json.load(time_file)
        for task_id in tasks:
            # reads_real.append(real[task_id]["read"])
            # writes_real.append(real[task_id]["write"])
            real_arr.append(real[task_id]["read"])
            real_arr.append(real[task_id]["write"])

    with open(wrench_time_file, "r") as time_file:
        wrench = json.load(time_file)
        for task_id in tasks:
            # reads_wrench.append(wrench[task_id]["read"])
            # writes_wrench.append(wrench[task_id]["write"])
            wrench_arr.append(wrench[task_id]["read"])
            wrench_arr.append(wrench[task_id]["write"])

    with open(wrench_cache_time_file, "r") as time_file:
        wrench_cache = json.load(time_file)
        for task_id in tasks:
            # reads_wrench_cache.append(wrench_cache[task_id]["read"])
            # writes_wrench_cache.append(wrench_cache[task_id]["write"])
            wrench_cache_arr.append(wrench_cache[task_id]["read"])
            wrench_cache_arr.append(wrench_cache[task_id]["write"])


    # print("WRENCH Read errors:")
    # print(abs(np.array(reads_wrench) - np.array(reads_real)) / np.array(reads_real) % 100)
    # print("WRENCH-cache Read errors:")
    # print(abs(np.array(reads_wrench_cache) - np.array(reads_real)) / np.array(reads_real)% 100)
    #
    # print("\nWRENCH Write errors:")
    # print(abs(np.array(writes_wrench) - np.array(writes_real)) / np.array(writes_real)% 100)
    # print("WRENCH-cache Write errors:")
    # print(abs(np.array(writes_wrench_cache) - np.array(writes_real)) / np.array(writes_real)% 100)

    plt.rcParams.update({'font.size': 12})
    fig, ax = plt.subplots(figsize=(9, 4))
    wrench_error = abs(np.array(wrench_arr) - np.array(real_arr)) / np.array(real_arr) * 100
    wrench_cache_error = abs(np.array(wrench_cache_arr) - np.array(real_arr)) / np.array(real_arr) * 100

    labels = ["Read 1", "Write 1", "Read 2", "Write 2", "Read 3", "Write 3", "Read 4", "Write 4"]
    # labels = ["Read 1", "Read 2", "Read 3",  "Read 4"]
    # labels = ["Write 1", "Write 2", "Write 3",  "Write 4"]
    grouped_bar_chart(ax, labels, "", "error (%)",  ("WRENCH", wrench_error, '#994F88'),
                      ("WRENCH-cache", wrench_cache_error, '#1965B0'))
    lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.55, 1), ncol=2)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.85, wspace=0.3)

    plt.savefig("figures/nighres_errors.svg", format="svg", bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.savefig("figures/nighres_errors.pdf", format="pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
