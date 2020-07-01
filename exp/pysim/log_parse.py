import csv


def read_timelog(filename, skip_header=True):
    result = []

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        if skip_header:
            next(csv_reader)

        for line in csv_reader:
            result.append((line[0], float(line[1]), float(line[2])))

    return result


def read_atop_log(filename):
    sys_mem = []
    free_mem = []
    used_mem = []
    cache_used = []
    dirty_data = []

    f = open(filename)
    lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("MEM"):
            values = line.split(" ")

            sys_mem_mb = int(values[7]) * 4096 / 1000 ** 2
            sys_mem.append(sys_mem_mb)

            cache_in_mb = int(values[9]) * 4096 / 1000 ** 2
            cache_used.append(cache_in_mb)

            dirty_amt_mb = int(values[12]) * 4096 / 1000 ** 2
            dirty_data.append(dirty_amt_mb)

    return {
        "total": sys_mem,
        "used_mem": used_mem,
        "cache": cache_used,
        "dirty_data": dirty_data
    }


def read_sim_log(filename):
    time = []
    sys_mem = []
    cache_used = []
    dirty_data = []

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for line in csv_reader:
            time.append(float(line[0]))
            sys_mem.append(float(line[1]))
            dirty_data.append(float(line[2]))
            cache_used.append(float(line[3]))

    return {
        "time": time,
        "total": sys_mem,
        "dirty_data": dirty_data,
        "cache": cache_used
    }
