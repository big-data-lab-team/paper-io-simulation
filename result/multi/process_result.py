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


def aggregate_result(folder, no_pipeline):
    """

    :param folder:
    :param no_pipeline:
    :return: makespan, total_readtime, total_writetime
    """

    makespan = 0
    readtime = 0
    writetime = 0
    for i in range(no_pipeline):
        filename = "%s/time_pipeline_%d_%d.csv" % (folder, no_pipeline, i + 1)
        start, end, read, write = parse_single_pipeline(filename)
        makespan += end - start
        readtime += read
        writetime += write

    return no_pipeline, makespan, readtime, writetime


def export_real_results(folder, filename):
    file = "%s%s" % (folder, filename)
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["no_pipeline", "makespan", "readtime", "writetime"])
        for i in range(32):
            writer.writerow(list(aggregate_result(folder, i + 1)))


def export_simgrid_result(folder, filename):
    exported_file = "%s%s" % (folder, filename)
    with open(exported_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["no_pipeline", "makespan", "readtime", "writetime"])
        for i in range(32):
            dump_file = "%s/dump_%d.json" % (folder, i + 1)
            writer.writerow(list(parse_simgrid_result(dump_file, i + 1)))


def parse_simgrid_result(filename, no_pipeline):
    with open(filename) as json_file:
        res = json.load(json_file)
        tasks = res["workflow_execution"]["tasks"]

        makespan = sum([task["whole_task"]["end"] - task["whole_task"]["start"] for task in tasks])
        read = sum([sum([read["end"] - read["start"] for read in task["read"]]) for task in tasks])
        write = sum([sum([write["end"] - write["start"] for write in task["write"]]) for task in tasks])

    return no_pipeline, makespan, read, write


def plot_prop(ax, exp_folder, propname, title):
    real_df = pd.read_csv("%s/real/aggregated.csv" % exp_folder)
    simg_org_df = pd.read_csv("%s/wrench/original/aggregated.csv" % exp_folder)
    simg_ext_df = pd.read_csv("%s/wrench/pagecache/aggregated.csv" % exp_folder)

    ax.set_title(title)

    ax.plot(real_df["no_pipeline"], real_df[propname] / real_df["no_pipeline"], color="k", label="Real execution")
    ax.plot(simg_org_df["no_pipeline"], simg_org_df[propname] / simg_org_df["no_pipeline"], color="tab:orange", label="Original WRENCH")
    ax.plot(simg_ext_df["no_pipeline"], simg_ext_df[propname] / simg_ext_df["no_pipeline"], color="tab:cyan",label="WRENCH with page cache")

    ax.set_xlabel("number of pipelines")
    ax.set_ylabel("time (s)")


export_real_results("local/real/", "aggregated.csv")
export_simgrid_result("local/wrench/original/", "aggregated.csv")
export_simgrid_result("local/wrench/pagecache/", "aggregated.csv")

plt.rcParams.update({'font.size': 8})
fig, (ax1, ax2) = plt.subplots(figsize=(10, 5), ncols=2, nrows=1)

plot_prop(ax1, "local", "readtime", "average read time")
plot_prop(ax2, "local", "writetime", "average write time")

plt.legend(loc='upper center', bbox_to_anchor=(-0.2, 1.3), ncol=3)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.7, wspace=0.3)

plt.savefig("figures/multi_local.pdf", format="pdf")
plt.savefig("figures/multi_local.svg", format="svg")

plt.show()
