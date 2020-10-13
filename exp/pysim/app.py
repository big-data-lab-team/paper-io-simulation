# i/o simulator in python
import plot_sim
import csv
import time
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


mm = MemoryManager(268600, 268600, read_bw=6860, write_bw=2765)
storage = Storage(450000, read_bw=510, write_bw=420)
kernel = IOManager(mm, storage, dirty_ratio=0.4)

input_size = 100000
compute_time = 155

file1 = File("file1", input_size, input_size)
file2 = File("file2", input_size, input_size)
file3 = File("file3", input_size, input_size)
file4 = File("file4", input_size, input_size)

start = time.time()

start_time = 0

task1_read_end = kernel.read_file_by_chunk(file1, 50, start_time)
task1_compute_end = kernel.compute(task1_read_end, compute_time)
task1_write_end = kernel.write_file_in_chunk(file2, 50, task1_compute_end)
kernel.release(file2)

task2_read_end = kernel.read_file_by_chunk(file2, 50, task1_write_end)
task2_compute_end = kernel.compute(task2_read_end, compute_time)
task2_write_end = kernel.write_file_in_chunk(file3, 50, task2_compute_end)
kernel.release(file3)

task3_read_end = kernel.read_file_by_chunk(file3, 50, task2_write_end)
task3_compute_end = kernel.compute(task3_read_end, compute_time)
task3_write_end = kernel.write_file_in_chunk(file4, 50, task3_compute_end)
kernel.release(file4)

end = time.time()

print("Sim time: %.8f" % (end - start))

task_time = {
    "read_start": [start_time, task1_write_end, task2_write_end],
    "read_end": [task1_read_end, task2_read_end, task3_read_end],
    "write_start": [task1_compute_end, task2_compute_end, task3_compute_end],
    "write_end": [task1_write_end, task2_write_end, task3_write_end],

}

tasks = [("read", start_time, task1_read_end), ("write", task1_compute_end, task1_write_end),
         ("read", task1_write_end, task2_read_end), ("write", task2_compute_end, task2_write_end),
         ("read", task2_write_end, task3_read_end), ("write", task3_compute_end, task3_write_end)]

plot_sim.plot_pysim_log(mm.get_log(), task_time, "input = %d MB \nmem_rb = %d MBps\nmem_wb = %d MBps \n"
                                           "disk_rb = %d MBps\ndisk_wb = %d MBps"
                      % (input_size, mm.read_bw, mm.write_bw,
                     storage.read_bw, storage.write_bw),
                      xmin=0, xmax=800, ymin=-10000, ymax=280000)

export_mem(mm.get_log(), "export/%dgb_sim_mem.csv" % (input_size / 1000))
export_time(tasks, "export/%dgb_sim_time.csv" % (input_size / 1000))
