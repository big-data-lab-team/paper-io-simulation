import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import json
import seaborn as sns


real_color = "#90C987"
wrench_color = "#994F88"
wrench_cache_color = "#1965B0"

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


def export_real_results(folder, filename, step=1):
    """
    Export aggregated results for each repetition of read execution
    :param folder:
    :param filename: aggregated results file
    :param step: increment step of number of pipelines
    :return:
    """
    file = "%s%s" % (folder, filename)
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["no_pipeline", "makespan", "readtime", "writetime"])
        for i in range(0, 32, step):
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


def suplot_prop(ax, real_dir, wrench_dir, propname, title, ylabel, rep_no=1, step=1):
    simg_org_df = pd.read_csv("%s/original/aggregated.csv" % wrench_dir)
    simg_ext_df = pd.read_csv("%s/pagecache/aggregated.csv" % wrench_dir)
    no_pipeline_df = simg_org_df["no_pipeline"]
    no_pipeline_real = list(range(1, len(no_pipeline_df) + 1, step))

    real_df = pd.DataFrame()
    for i in range(rep_no):
        df = pd.read_csv("%s/%d/aggregated.csv" % (real_dir, i + 1))
        real_df[i + 1] = df[propname]

    mean_df = real_df.mean(axis=1)
    max_df = real_df.max(axis=1)
    min_df = real_df.min(axis=1)

    ax.set_title(title)

    ax.plot(no_pipeline_real, mean_df / no_pipeline_real, color=real_color, linewidth=2, label="Real execution mean")
    # ax.plot(no_pipeline_df, max_df / no_pipeline_df, color="green", linewidth=1, alpha=0.5)
    # ax.plot(no_pipeline_df, min_df / no_pipeline_df, color="green", linewidth=1, alpha=0.5)
    ax.fill_between(no_pipeline_real, min_df / no_pipeline_real, max_df / no_pipeline_real, facecolor=real_color, alpha=0.5,
                    label="Real execution min-max interval (5 repetitions)")

    ax.plot(no_pipeline_df, simg_org_df[propname] / no_pipeline_df, linewidth=2, color=wrench_color, label="WRENCH")
    ax.plot(no_pipeline_df, simg_ext_df[propname] / no_pipeline_df, linewidth=2, color=wrench_cache_color, label="WRENCH-cache")

    ax.set_xlabel("Concurrent applications")
    if ylabel:
        ax.set_ylabel("time (s)")


def result_local(rep_no=1, step=1):
    for i in range(rep_no):
        export_real_results("local/real_clearoutput_step5/%d/" % (i + 1), "aggregated.csv", step)

    export_simgrid_result("local/wrench/original/", "aggregated.csv")
    export_simgrid_result("local/wrench/pagecache/", "aggregated.csv")
    plt.rcParams.update({'font.size': 8})
    fig, (ax1, ax2) = plt.subplots(figsize=(10, 5), ncols=2, nrows=1)

    suplot_prop(ax1, "local/real_clearoutput_step5/", "local/wrench/", "readtime", "Read time", True, rep_no=rep_no, step=step)
    suplot_prop(ax2, "local/real_clearoutput_step5/", "local/wrench/", "writetime", "Write time", False, rep_no=rep_no, step=step)

    ax1.set_ylim(bottom=0, top=1500)
    ax2.set_ylim(bottom=0, top=1500)

    plt.legend(loc='upper center', bbox_to_anchor=(-0.2, 1.18), ncol=4)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.7, wspace=0.4)
    # plt.savefig("figures/multi_local.pdf", format="pdf")
    # plt.savefig("figures/multi_local.svg", format="svg")

    plt.show()


def result_nfs(rep_no=1):
    for i in range(rep_no):
        export_real_results("nfs/real/%d/" % (i + 1), "aggregated.csv")

    export_simgrid_result("nfs/wrench/original/", "aggregated.csv")
    export_simgrid_result("nfs/wrench/pagecache/", "aggregated.csv")
    plt.rcParams.update({'font.size': 8})
    fig, (ax1, ax2) = plt.subplots(figsize=(10, 5), ncols=2, nrows=1)

    suplot_prop(ax1, "nfs/real/", "nfs/wrench/", "readtime", "Read time", True, rep_no=rep_no)
    suplot_prop(ax2, "nfs/real/", "nfs/wrench/", "writetime", "Write time", False, rep_no=rep_no)

    ax1.set_ylim(bottom=0, top=1500)
    ax2.set_ylim(bottom=0, top=1500)

    plt.legend(loc='upper center', bbox_to_anchor=(-0.1, 1.2), ncol=4)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.7, wspace=0.4)
    plt.savefig("figures/multi_nfs.pdf", format="pdf")
    plt.savefig("figures/multi_nfs.svg", format="svg")

    # plt.show()


def run_time():
    # WRENCH data
    local_org_df = pd.read_csv("local/wrench/run_time_original.csv")
    nfs_org_df = pd.read_csv("nfs/wrench/run_time_original.csv")
    org_df = pd.concat([local_org_df, nfs_org_df])

    # WRENCH-cache data
    local_cache_df = pd.read_csv("local/wrench/run_time_pagecache.csv")
    nfs_cache_df = pd.read_csv("nfs/wrench/run_time_pagecache.csv")

    fig, ax1 = plt.subplots(figsize=(5,5), ncols=1, nrows=1)
    plt.rcParams.update({'font.size': 8})

    from scipy import stats


    ax1.set_ylim(top=2)
    s = 10

    # WRENCH original
    slope, intercept, r_value, p_value, std_err = stats.linregress(org_df["no_pipeline"],org_df["run_time"])
    print(f'WRENCH original: p={p_value}')
    ax1.scatter(local_org_df["no_pipeline"], local_org_df["run_time"],
                label = "WRENCH (local)", s=s, color=wrench_color)
    ax1.scatter(nfs_org_df["no_pipeline"], nfs_org_df["run_time"],
                label="WRENCH (NFS)", s=s, color=wrench_color, facecolor="none")
    ax1.plot(org_df["no_pipeline"], intercept+slope*org_df["no_pipeline"], lw=1, color=wrench_color)
    plt.text(20, 0.1, f'y={round(slope,2)}x+{round(intercept,2)}', color=wrench_color)

    # WRENCH-cache Local I/Os
    slope, intercept, r_value, p_value, std_err = stats.linregress(local_cache_df["no_pipeline"],
                                                                   local_cache_df["run_time"])
    print(f'WRENCH-cache local: p={p_value}')
    ax1.plot(local_cache_df["no_pipeline"], intercept+slope*local_cache_df["no_pipeline"],
             color=wrench_cache_color, lw=1)
    ax1.scatter(local_cache_df["no_pipeline"], local_cache_df["run_time"],
                label="WRENCH-cache (local)", s=s, color=wrench_cache_color)
    plt.text(17, 1, f'y={round(slope,2)}x{round(intercept,2)}', color=wrench_cache_color)


    # WRENCH-cache NFS
    slope, intercept, r_value, p_value, std_err = stats.linregress(nfs_cache_df["no_pipeline"],
                                                                   nfs_cache_df["run_time"])
    print(f'WRENCH-cache NFS: p={p_value}')
    ax1.plot(nfs_cache_df["no_pipeline"], intercept+slope*nfs_cache_df["no_pipeline"],
             color=wrench_cache_color, lw=1, linestyle='dotted')
    ax1.scatter(nfs_cache_df["no_pipeline"], nfs_cache_df["run_time"],
                label = "WRENCH-cache (NFS)", s=s, color=wrench_cache_color, facecolor="none")
    plt.text(27, 0.8, f'y={round(slope,2)}x{round(intercept,2)}', color=wrench_cache_color)

    plt.xlabel("Concurrent applications")
    plt.ylabel("Simulation time (seconds)")
    plt.legend()

    plt.savefig("figures/simulation_time.pdf", format="pdf")
    plt.savefig("figures/simulation_time.svg", format="svg")

