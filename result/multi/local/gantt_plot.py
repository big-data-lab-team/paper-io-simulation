import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def parse_pipeline(filename):
    df = pd.read_csv(filename)
    task_1 = {
        "read_start": df["read_start"][0],
        "read_end": df["read_end"][0],
        "cpu_start": df["cpu_start"][0],
        "cpu_end": df["cpu_end"][0],
        "write_start": df["write_start"][0],
        "write_end": df["write_end"][0]
    }
    task_2 = {
        "read_start": df["read_start"][1],
        "read_end": df["read_end"][1],
        "cpu_start": df["cpu_start"][1],
        "cpu_end": df["cpu_end"][1],
        "write_start": df["write_start"][1],
        "write_end": df["write_end"][1]
    }
    task_3 = {
        "read_start": df["read_start"][2],
        "read_end": df["read_end"][2],
        "cpu_start": df["cpu_start"][2],
        "cpu_end": df["cpu_end"][2],
        "write_start": df["write_start"][2],
        "write_end": df["write_end"][2]
    }

    return [task_1, task_2, task_3]


def gantt_plot(no_pipelines=20):
    pipelines = [parse_pipeline("indv_logs/time_pipeline_%d_%d.csv" % (no_pipelines, i + 1)) for i in
                 range(no_pipelines)]

    fig, ax = plt.subplots()

    starts = [min(task1["read_start"], task2["read_start"], task3["read_start"]) for (task1, task2, task3) in pipelines]
    start = min(starts)

    for i in range(no_pipelines):
        tasks = pipelines[i]
        for j in range(3):
            task = tasks[j]
            ax.broken_barh([(task["read_start"] - start, task["read_end"] - task["read_start"]),
                            (task["cpu_start"] - start, task["cpu_end"] - task["cpu_start"]),
                            (task["write_start"] - start, task["write_end"] - task["write_start"])],
                           (10 * i + j * 3, 3),
                           facecolors=('tab:purple', 'tab:orange', 'tab:cyan'),
                           alpha=0.7)
    ax.grid(True)
    # plt.xticks([])
    plt.yticks([])
    plt.xlabel("Time (s)")
    plt.ylabel("Tasks")
    plt.title("no. pipelines = %d" % no_pipelines)
    plt.show()


gantt_plot(32)
