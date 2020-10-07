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


def aggregate_result(dir, no_pipeline):
    """

    :param no_pipeline:
    :return: makespan, total_readtime, total_writetime
    """

    makespan = 0
    readtime = 0
    writetime = 0
    for i in range(no_pipeline):
        filename = "%s/indv_logs/time_pipeline_%d_%d.csv" % (dir, no_pipeline, i + 1)
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


def export_simgrid_result(dir, filename):
    exported_file = "%s/%s" % (dir, filename)
    with open(exported_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["no_pipeline", "makespan", "readtime", "writetime"])
        for i in range(32):
            dump_file = "%s/dump_%d.json" % (dir, i + 1)
            writer.writerow(list(parse_simgrid_result(dump_file, i + 1)))


def parse_simgrid_result(filename, no_pipeline):
    with open(filename) as json_file:
        res = json.load(json_file)
        tasks = res["workflow_execution"]["tasks"]

        makespan = sum([task["whole_task"]["end"] - task["whole_task"]["start"] for task in tasks])
        read = sum([sum([read["end"] - read["start"] for read in task["read"]]) for task in tasks])
        write = sum([sum([write["end"] - write["start"] for write in task["write"]]) for task in tasks])

    return no_pipeline, makespan, read, write


def plot_prop(propname, title, average=False):
    real_df = pd.read_csv("real/aggregated_result_real.csv")
    simg_org_df = pd.read_csv("wrench_org/aggregated.csv")
    simg_ext_df = pd.read_csv("wrench_ext/aggregated.csv")

    plt.figure()
    plt.title(title)

    if average:
        plt.plot(real_df["no_pipeline"], real_df[propname] / real_df["no_pipeline"], label="real")
        plt.plot(simg_org_df["no_pipeline"], simg_org_df[propname] / simg_org_df["no_pipeline"], label="original WRENCH")
        plt.plot(simg_ext_df["no_pipeline"], simg_ext_df[propname] / simg_ext_df["no_pipeline"], label="extended WRENCH")
    else:
        plt.plot(real_df["no_pipeline"], real_df[propname], label="real")
        plt.plot(simg_org_df["no_pipeline"], simg_org_df[propname], label="original WRENCH")
        plt.plot(simg_ext_df["no_pipeline"], simg_ext_df[propname], label="extended WRENCH")

    plt.xlabel("number of pipelines")
    plt.ylabel("time (s)")

    plt.legend()
    if average:
        plt.savefig("figures/%s_avg.pdf" % propname)
    else:
        plt.savefig("figures/%s.pdf" % propname)
    plt.show()


# export_simgrid_result("wrench_org", "aggregated.csv")
# export_simgrid_result("wrench_ext", "aggregated.csv")
#
# plot_prop("makespan", "total makespan")
# plot_prop("readtime", "cumulative read time")
# plot_prop("readtime", "average read time", average=True)
# plot_prop("writetime", "cumulative write time")
# plot_prop("writetime", "average write time", average=True)
