import pandas as pd
import matplotlib.pyplot as plt

columns = ["read1", "write1", "read2", "write2", "read3", "write3"]
files = ["file1", "file2", "file3", "file4"]
df_real = pd.read_csv("fincore/real.csv", index_col="task")
df_sim = pd.read_csv("fincore/sim.csv", index_col="task")

# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=[10,5])

df_real[files].plot.bar(stacked=True, rot=0, title="Real pipeline")
# df_sim[files].plot.bar(stacked=True, rot=0, title="WRENCH simulator")

plt.subplots_adjust(left=0.12, bottom=0.15, right=0.92, top=0.9)

plt.xlabel("")
plt.ylabel("amount (GB)")
plt.savefig("figures/fincore_real.svg", format="svg")
plt.savefig("figures/fincore_real.pdf", format="pdf")

plt.show()
