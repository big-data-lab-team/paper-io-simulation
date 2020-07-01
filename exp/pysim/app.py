# i/o simulator in python
import plot
import csv
from components import IOManager
from components import File
from components import Storage
from components import MemoryManager


def export_mem(mem_log, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "total_mem", "dirty", "cache", "used_mem"])
        for i in range(len(mm.get_log()["time"])):
            writer.writerow([mem_log["time"][i], mem_log["total"][i], mem_log["dirty"][i],
                             mem_log["cache"][i], mem_log["used"][i]])


def export_time(task_list, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["type", "start", "end"])
        for i in range(len(task_list)):
            writer.writerow([task_list[i][0], task_list[i][1], task_list[i][2]])


mm = MemoryManager(268600, 268600, read_bw=7100, write_bw=3300)
storage = Storage(450000, read_bw=465, write_bw=465)
kernel = IOManager(mm, storage, dirty_ratio=0.4)

input_size = 20000
compute_time = 28

file1 = File("file1", input_size, input_size)
file2 = File("file2", input_size, input_size)
file3 = File("file3", input_size, input_size)
file4 = File("file4", input_size, input_size)

start_time = 0

task1_read_end = kernel.read(file1, start_time)
task1_compute_end = kernel.compute(task1_read_end, compute_time)
task1_write_end = kernel.write(file2, task1_compute_end)
kernel.release(file2)

task2_read_end = kernel.read(file2, task1_write_end)
task2_compute_end = kernel.compute(task2_read_end, compute_time)
task2_write_end = kernel.write(file3, task2_compute_end)
kernel.release(file3)

task3_read_end = kernel.read(file3, task2_write_end)
task3_compute_end = kernel.compute(task3_read_end, compute_time)
task3_write_end = kernel.write(file4, task3_compute_end)
kernel.release(file4)

task_time = {
    "read_start": [start_time, task1_write_end, task2_write_end],
    "read_end": [task1_read_end, task2_read_end, task3_read_end],
    "write_start": [task1_compute_end, task2_compute_end, task3_compute_end],
    "write_end": [task1_write_end, task2_write_end, task3_write_end],

}

tasks = [("read", start_time, task1_read_end), ("write", task1_compute_end, task1_write_end),
         ("read", task1_write_end, task2_read_end), ("write", task2_compute_end, task2_write_end),
         ("read", task2_write_end, task3_read_end), ("write", task3_compute_end, task3_write_end)]

plot.plot_mem_log(mm.get_log(), task_time, "input = %d MB \nmem_rb = %d MBps\nmem_wb = %d MBps \n"
                                           "disk_rb = %d MBps\ndisk_wb = %d MBps"
                  % (input_size, mm.read_bw, mm.write_bw,
                     storage.read_bw, storage.write_bw),
                  xmin=0, xmax=200, ymin=-10000, ymax=280000)

export_mem(mm.get_log(), "py_log/ex1/new/100gb_sim_mem.csv")
export_time(tasks, "py_log/ex1/new/100gb_sim_time.csv")
