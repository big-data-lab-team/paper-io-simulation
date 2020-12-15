import json


def parse_time(logfile, sum_file):
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


def parse_task(logfile, sum_file):
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


parse_time("real/log/timelog_sub001_sess1.json", "real/log/summary_time_sub001_sess1.json")
parse_task("real/log/timelog_sub001_sess1.json", "real/log/summary_file_sub001_sess1.json")
