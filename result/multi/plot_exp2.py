import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import json


def parse_single_pipeline(filename):
    """
    :param filename:
    :return: tuple (start, end, readtime, writetime)
    """
    df = pd.read_csv(filename)
    readtime = sum(df["read_end"] - df["read_start"])
    writetime = sum(df["write_end"] - df["write_start"])

    return min(df["read_start"]), max(df["write_end"]), readtime, writetime


def aggregate_result(no_pipeline):
    """

    :param no_pipeline:
    :return: makespan, total_readtime, total_writetime
    """

    makespan = 0
    readtime = 0
    writetime = 0
    for i in range(no_pipeline):
        filename = "export/cluster/multi/time/time_pipeline_%d_%d.csv" % (no_pipeline, i + 1)
        start, end, read, write = parse_single_pipeline(filename)
        makespan += end - start
        readtime += read
        writetime += write

    return no_pipeline, makespan, readtime, writetime


def export_real_results(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["no_pipeline", "makespan", "readtime", "writetime"])
        for i in range(32):
            writer.writerow(list(aggregate_result(i + 1)))


def export_simgrid_result(filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["no_pipeline", "makespan", "readtime", "writetime"])
        for i in range(32):
            writer.writerow(list(parse_simgrid_result(i + 1)))


def parse_simgrid_result(no_pipeline):
    filename = "simgrid/multi/unified_%d.json" % no_pipeline
    with open(filename) as json_file:
        res = json.load(json_file)
        tasks = res["workflow_execution"]["tasks"]

        makespan = sum([task["whole_task"]["end"] - task["whole_task"]["start"] for task in tasks])
        read = sum([sum([read["end"] - read["start"] for read in task["read"]]) for task in tasks])
        write = sum([sum([write["end"] - write["start"] for write in task["write"]]) for task in tasks])

    return no_pipeline, makespan, read, write


def plot_prop(propname, title, average=False):
    real_df = pd.read_csv("export/cluster/multi/aggregated_result_real.csv")
    simgrid_df = pd.read_csv("simgrid/multi/aggregated_result_simgrid.csv")

    plt.figure()
    plt.title(title)

    if average:
        plt.plot(real_df["no_pipeline"], real_df[propname] / real_df["no_pipeline"], label="real")
        plt.plot(simgrid_df["no_pipeline"], simgrid_df[propname] / simgrid_df["no_pipeline"], label="original simgrid")
    else:
        plt.plot(real_df["no_pipeline"], real_df[propname], label="real")
        plt.plot(simgrid_df["no_pipeline"], simgrid_df[propname], label="original simgrid")

    plt.xlabel("number of pipelines")
    plt.ylabel("time (s)")

    plt.legend()
    plt.show()


plot_prop("makespan", "makespan total")
plot_prop("readtime", "accumulative read time")
plot_prop("readtime", "average read time", average=True)
plot_prop("writetime", "accumulative write time")
plot_prop("writetime", "average write time", average=True)
