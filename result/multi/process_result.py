import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import json
import seaborn as sns


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
            dump_file = "%sdump_%d.json" % (folder, i + 1)
            writer.writerow(list(parse_simgrid_result(dump_file, i + 1)))


def parse_simgrid_result(filename, no_pipeline):
    with open(filename) as json_file:
        res = json.load(json_file)
        tasks = res["workflow_execution"]["tasks"]

        makespan = sum([task["whole_task"]["end"] - task["whole_task"]["start"] for task in tasks])
        read = sum([sum([read["end"] - read["start"] for read in task["read"]]) for task in tasks])
        write = sum([sum([write["end"] - write["start"] for write in task["write"]]) for task in tasks])

    return no_pipeline, makespan, read, write


def suplot_prop(ax, real_dir, wrench_dir, propname, title, rep_no=1):
    simg_org_df = pd.read_csv("%s/original/aggregated.csv" % wrench_dir)
    simg_ext_df = pd.read_csv("%s/pagecache/aggregated.csv" % wrench_dir)
    no_pipeline_df = simg_org_df["no_pipeline"]

    real_df = pd.DataFrame()
    for i in range(rep_no):
        df = pd.read_csv("%s/%d/aggregated.csv" % (real_dir, i + 1))
        real_df[i + 1] = df[propname]

    mean_df = real_df.mean(axis=1)
    max_df = real_df.max(axis=1)
    min_df = real_df.min(axis=1)

    ax.set_title(title)

    ax.plot(no_pipeline_df, mean_df / no_pipeline_df, color="k", linewidth=1, label="Real execution mean")
    ax.plot(no_pipeline_df, max_df / no_pipeline_df, color="k", linewidth=1, alpha=0.5)
    ax.plot(no_pipeline_df, min_df / no_pipeline_df, color="k", linewidth=1, alpha=0.5)
    ax.fill_between(no_pipeline_df, min_df / no_pipeline_df, max_df / no_pipeline_df, facecolor='lightgrey', alpha=0.5,
                    label="Real execution")

    ax.plot(no_pipeline_df, simg_org_df[propname] / no_pipeline_df, linewidth=1, color="tab:orange", label="WRENCH")
    ax.plot(no_pipeline_df, simg_ext_df[propname] / no_pipeline_df, linewidth=1, color="tab:cyan", label="WRENCH-Ext")

    ax.set_xlabel("number of pipelines")
    ax.set_ylabel("time (s)")


def result_local(rep_no=1):
    for i in range(rep_no):
        export_real_results("local/real/%d/" % (i + 1), "aggregated.csv")

    export_simgrid_result("local/wrench/original/", "aggregated.csv")
    export_simgrid_result("local/wrench/pagecache/", "aggregated.csv")
    plt.rcParams.update({'font.size': 8})
    fig, (ax1, ax2) = plt.subplots(figsize=(10, 5), ncols=2, nrows=1)

    suplot_prop(ax1, "local/real/", "local/wrench/", "readtime", "average read time", rep_no=rep_no)
    suplot_prop(ax2, "local/real/", "local/wrench/", "writetime", "average write time", rep_no=rep_no)

    ax1.set_ylim(bottom=0, top=1500)
    ax2.set_ylim(bottom=0, top=1500)

    plt.legend(loc='upper center', bbox_to_anchor=(-0.2, 1.3), ncol=2)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.7, wspace=0.3)
    plt.savefig("figures/multi_local.pdf", format="pdf")
    plt.savefig("figures/multi_local.svg", format="svg")

    plt.show()


def result_nfs(rep_no=1):
    for i in range(rep_no):
        export_real_results("nfs/real/%d/" % (i + 1), "aggregated.csv")

    export_simgrid_result("nfs/wrench/original/", "aggregated.csv")
    export_simgrid_result("nfs/wrench/pagecache/", "aggregated.csv")
    plt.rcParams.update({'font.size': 8})
    fig, (ax1, ax2) = plt.subplots(figsize=(10, 5), ncols=2, nrows=1)

    suplot_prop(ax1, "nfs/real/", "nfs/wrench/", "readtime", "average read time", rep_no=rep_no)
    suplot_prop(ax2, "nfs/real/", "nfs/wrench/", "writetime", "average write time", rep_no=rep_no)

    ax1.set_ylim(bottom=0, top=1500)
    ax2.set_ylim(bottom=0, top=1500)

    plt.legend(loc='upper center', bbox_to_anchor=(-0.2, 1.3), ncol=2)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.7, wspace=0.3)
    plt.savefig("figures/multi_nfs.pdf", format="pdf")
    plt.savefig("figures/multi_nfs.svg", format="svg")

    plt.show()
