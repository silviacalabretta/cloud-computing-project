import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


# CPU 
cpu = pd.read_csv("../cpu_summary.csv", sep=";")

groups = {
    "vm-master": ["vm_m"],
    "vm-node": ["vm_n04", "vm_n05"],
    "c-master": ["c_m"],
    "c-node": ["c_n01", "c_n02"]
}

cpu_agg = []
for k, labels in groups.items():
    tmp = cpu[cpu["label"].isin(labels)]
    cpu_agg.append([k, tmp["events_per_sec"].mean(), tmp["lat_avg_ms"].mean()])

cpu_agg = pd.DataFrame(cpu_agg, columns=["group", "throughput", "latency"])

colors = ["tab:blue", "tab:blue", "tab:orange", "tab:orange"]

# Throughput
plt.figure()
plt.bar(cpu_agg["group"], cpu_agg["throughput"], color=colors)
plt.ylabel("Events/sec")
plt.title("CPU Throughput")
plt.savefig("cpu_throughput.png")
plt.close()

# Latency
plt.figure()
plt.bar(cpu_agg["group"], cpu_agg["latency"], color=colors)
plt.ylabel("Latency (ms)")
plt.title("CPU Latency")
plt.savefig("cpu_latency.png")
plt.close()


# MEMORY

mem = pd.read_csv("../mem_summary.csv", sep=";")

mem_agg = []
for k, labels in groups.items():
    tmp = mem[mem["label"].isin(labels)]
    mem_agg.append([k, tmp["operation_per_sec"].mean(), tmp["avg_lat(ms)"].mean()])

mem_agg = pd.DataFrame(mem_agg, columns=["group", "throughput", "latency"])

plt.figure()
plt.bar(mem_agg["group"], mem_agg["throughput"], color=colors)
plt.ylabel("Ops/sec")
plt.title("Memory Throughput")
plt.savefig("mem_throughput.png")
plt.close()

plt.figure()
plt.bar(mem_agg["group"], mem_agg["latency"], color=colors)
plt.ylabel("Latency (ms)")
plt.title("Memory Latency")
plt.savefig("mem_latency.png")
plt.close()

# LATENCY VS THROUGHPUT

plt.figure()

for i, row in cpu_agg.iterrows():
    group = row["group"]

    # Technology color
    if group.startswith("vm"):
        color = "tab:blue"
    else:
        color = "tab:orange"

    # Role marker
    if group.endswith("r"):
        marker = "o"      # master
    else:
        marker = "^"      # node

    plt.scatter(row["throughput"], row["latency"],
                color=color, marker=marker, s=120)


# Build legend manually
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Master',
           markerfacecolor='tab:grey', markersize=8),
    Line2D([0], [0], marker='^', color='w', label='Node',
           markerfacecolor='tab:grey', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='VM',
           markerfacecolor='tab:blue', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Container',
           markerfacecolor='tab:orange', markersize=8)
]

plt.legend(handles=legend_elements)

plt.xlabel("Throughput (events/s)")
plt.ylabel("Latency (ms)")
plt.title("CPU: Latency vs Throughput")
plt.savefig("cpu_scatter.png")
plt.close()


plt.figure()

for i, row in mem_agg.iterrows():
    group = row["group"]

    # Technology color
    if group.startswith("vm"):
        color = "tab:blue"
    else:
        color = "tab:orange"

    # Role marker
    if group.endswith("r"):
        marker = "o"      # master
    else:
        marker = "^"      # node

    plt.scatter(row["throughput"], row["latency"],
                color=color, marker=marker, s=120)


# Build legend manually
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Master',
           markerfacecolor='tab:grey', markersize=8),
    Line2D([0], [0], marker='^', color='w', label='Node',
           markerfacecolor='tab:grey', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='VM',
           markerfacecolor='tab:blue', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Container',
           markerfacecolor='tab:orange', markersize=8)
]

plt.legend(handles=legend_elements)
plt.xlabel("Throughput (ops/s)")
plt.ylabel("Latency (ms)")
plt.title("Memory: Latency vs Throughput")
plt.savefig("mem_scatter.png")
plt.close()



# DISK

disk = pd.read_csv("../disk_summary.csv", sep=";")

seq_ops = ["write", "rewrite", "read", "reread"]
rand_ops = ["random_read", "random_write", "bkwd_read", "stride_read", "record_rewrite"]
file_ops = ["fwrite", "frewrite", "fread", "freread"]

def plot_disk(op_list, name):
    plt.figure()

    style = {
        "vm-master":  {"color": "tab:blue",   "linestyle": "-",  "marker": "o"},
        "vm-node":  {"color": "cornflowerblue", "linestyle": "-", "marker": "^"},
        "c-master":   {"color": "tab:orange", "linestyle": "-",  "marker": "o"},
        "c-node":   {"color": "lightsalmon",    "linestyle": "-", "marker": "^"},
    }

    for g, labels in groups.items():
        tmp = disk[disk["label"].isin(labels)]
        y = tmp[op_list].mean()

        plt.plot(op_list, y,
                 label=g,
                 color=style[g]["color"],
                 linestyle=style[g]["linestyle"],
                 marker=style[g]["marker"],
                 linewidth=2,
                 markersize=8)

    plt.ylabel("KB/sec")
    plt.title(name)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{name}.png")
    plt.close()

plot_disk(seq_ops, "disk_sequential")
plot_disk(rand_ops, "disk_random")
plot_disk(file_ops, "disk_file")

#local vs nf
plt.figure()

labels = disk["label"].unique()
x = range(len(labels))
width = 0.35

local_vals = []
nfs_vals = []
local_colors = []
nfs_colors = []

for lab in labels:
    row_local = disk[(disk["label"] == lab) & (disk["filesystem"] == "local")]
    row_nfs   = disk[(disk["label"] == lab) & (disk["filesystem"] == "NFS")]

    local_vals.append(row_local["read"].values[0])
    nfs_vals.append(row_nfs["read"].values[0])

    if lab.startswith("vm"):
        local_colors.append("tab:blue")
        nfs_colors.append("slateblue")
    else:
        local_colors.append("tab:orange")
        nfs_colors.append("orangered")

x = np.arange(len(labels))

label_map = {
    "vm_m": "vm-master",
    "vm_n04": "vm-node04",
    "vm_n05": "vm-node05",
    "c_m": "c-master",
    "c_n01": "c-node01",
    "c_n02": "c-node02"
}

correct_labels = [label_map[l] for l in labels]

plt.bar(x - width/2, local_vals, width, label="Local", color=local_colors)
plt.bar(x + width/2, nfs_vals, width, label="NFS", color=nfs_colors)

plt.xticks(x, correct_labels, rotation=20)
plt.ylabel("Read KB/sec")
plt.title("Disk Performance: Local vs NFS (Read)")
plt.legend()

plt.tight_layout()
plt.savefig("disk_local_vs_nfs.png")
plt.close()



# plt.figure()
# for fs in ["local", "NFS"]:
#     tmp = disk[disk["filesystem"] == fs]
#     plt.bar(tmp["label"], tmp["read"], label=fs)
# plt.legend()
# plt.ylabel("Read KB/sec")
# plt.title("Disk Local vs NFS (Read)")
# plt.savefig("disk_local_vs_nfs.png")
# plt.close()

#NETWORK
net = pd.read_csv("../net_summary.csv", sep=";")

label_map = {
    "vm_n04_m": "vm-master-node",
    "vm_n05_n04": "vm-node-node",
    "c_n01_m": "c-master-node",
    "c_n02_n01": "c-node-node"
}
x = np.arange(len(net))

clean_labels = [label_map[l] for l in net["label"]]

plt.figure()
plt.bar(x, net["rtt_avg(ms)"], color=colors)
plt.xticks(x, clean_labels, rotation=20)
plt.ylabel("RTT (ms)")
plt.title("Network RTT")
plt.tight_layout()
plt.savefig("net_rtt.png")
plt.close()

# plt.figure()
# plt.bar(net["label"], net["rtt_avg(ms)"], color=colors)
# plt.ylabel("RTT (ms)")
# plt.title("Network RTT")
# plt.savefig("net_rtt.png")
# plt.close()

labels = net["label"].tolist()
# x = np.arange(len(labels))
width = 0.35

# Define colors:
# VMs = blue tones, Containers = orange/red tones
colors_up = []
colors_down = []

for name in labels:
    if name.startswith("vm"):
        colors_up.append("tab:blue")
        colors_down.append("slateblue")   # lighter / purplish blue
    else:
        colors_up.append("tab:orange")
        colors_down.append("orangered")   # stronger red/orange

plt.figure()

plt.bar(x - width/2, net["Bitrate_up(Gbits/sec)"], width,
        label="Upload", color=colors_up)

plt.bar(x + width/2, net["Bitrate_down(Gbits/sec)"], width,
        label="Download", color=colors_down)

plt.ylabel("Gbit/sec")
plt.title("Network Throughput: Upload vs Download")
plt.xticks(x, clean_labels, rotation=20)
plt.legend()

plt.tight_layout()
plt.savefig("net_upload_download.png")
plt.close()

# VM VS CONTAINERS SUMMARY
summary = pd.DataFrame({
    "CPU": [cpu_agg.loc[cpu_agg.group=="c-master","throughput"].values[0] /
            cpu_agg.loc[cpu_agg.group=="vm-master","throughput"].values[0]],
    "MEM": [mem_agg.loc[mem_agg.group=="c-master","throughput"].values[0] /
            mem_agg.loc[mem_agg.group=="vm-master","throughput"].values[0]]
})

plt.figure()
plt.bar(summary.columns, summary.iloc[0])
plt.ylabel("Container / VM")
plt.title("Container Advantage Summary")
plt.savefig("vm_vs_container.png")
plt.close()


