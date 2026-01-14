import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# --- Configuration ---
groups = {
    "vm-master": ["vm_m"],
    "vm-node":   ["vm_n04", "vm_n05"],
    "c-master":  ["c_m"],
    "c-node":    ["c_n01", "c_n02"]
}

# 1. Order: Local clustered together, Shared clustered together
bar_categories = [
    ("vm-master", "local", "VM Master (Local)"),
    ("vm-node",   "local", "VM Node (Local)"),
    ("vm-master", "NFS",   "VM Master (Shared)"),
    ("vm-node",   "NFS",   "VM Node (Shared)"),
    ("c-master",  "local", "Cont Master (Local)"),
    ("c-node",    "local", "Cont Node (Local)"),
    ("c-master",  "NFS",   "Cont Master (Shared)"),
    ("c-node",    "NFS",   "Cont Node (Shared)")
]

# 2. Colors for Main Plots (8 colors)
colors = [
    "xkcd:blue",        # VM Master (Local)
    "cornflowerblue",   # VM Node (Local)
    "darkslateblue",    # VM Master (Shared)
    "slateblue",        # VM Node (Shared)
    "orangered",        # Cont Master (Local)
    "tomato",           # Cont Node (Local)
    "darkorange",       # Cont Master (Shared)
    "sandybrown"        # Cont Node (Shared)
]

# 3. Simple Colors for Read Plot (4 colors)
simple_colors = {
    "vm_local":    "xkcd:blue",
    "vm_shared":   "slateblue",
    "cont_local":  "orangered",
    "cont_shared": "darkorange"
}

# Operations Lists
seq_ops = ["write", "rewrite", "read", "reread"]
rand_ops = ["random_read", "random_write", "bkwd_read", "stride_read", "record_rewrite"]
file_ops = ["fwrite", "frewrite", "fread", "freread"]
all_ops = seq_ops + rand_ops + file_ops

# --- Helper Functions ---

def get_op_data(df, ops_list):
    """Constructs a DataFrame for the main grouped plots."""
    rows = []
    for op in ops_list:
        row_data = {"Operation": op}
        for group_key, fs, display_name in bar_categories:
            labels = groups[group_key]
            mask = (df["label"].isin(labels)) & (df["filesystem"] == fs)
            tmp = df[mask]
            row_data[display_name] = tmp[op].mean() if not tmp.empty else 0
        rows.append(row_data)
    return pd.DataFrame(rows).set_index("Operation")

def plot_disk_ops(df, title, filename, figure_size=(14, 7), rot=0):
    fig, ax = plt.subplots(figsize=figure_size)
    df.plot(kind="bar", color=colors, width=0.85, rot=rot, zorder=3, ax=ax)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='-', alpha=0.7)
    ax.set_ylabel("Throughput (KB/sec)")
    ax.set_xlabel("Operation")
    ax.set_title(title)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def plot_single_op_compare(df, op_name, filename):
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    
    # 1. Define Groups for X-axis
    x_groups = [
        ("vm-master", "VM Master"),
        ("vm-node",   "VM Node"),
        ("c-master",  "Cont Master"),
        ("c-node",    "Cont Node")
    ]
    
    # 2. Extract Data & Colors
    local_vals = []
    shared_vals = []
    c_local = [] 
    c_shared = []
    
    for key, name in x_groups:
        labels = groups[key]
        
        # Determine base type (vm or c)
        base_type = "vm" if "vm" in key else "cont"
        
        # Get Local Value & Color
        tmp_loc = df[(df["label"].isin(labels)) & (df["filesystem"] == "local")]
        val_loc = tmp_loc[op_name].mean() if not tmp_loc.empty else 0
        local_vals.append(val_loc)
        c_local.append(simple_colors[f"{base_type}_local"])
        
        # Get Shared Value & Color
        tmp_shr = df[(df["label"].isin(labels)) & (df["filesystem"] == "NFS")]
        val_shr = tmp_shr[op_name].mean() if not tmp_shr.empty else 0
        shared_vals.append(val_shr)
        c_shared.append(simple_colors[f"{base_type}_shared"])

    # 3. Plotting
    x = np.arange(len(x_groups))
    width = 0.35
    
    # Local Bars (Left)
    ax.bar(x - width/2, local_vals, width, label="Local", color=c_local, zorder=3)
    
    # Shared Bars (Right)
    ax.bar(x + width/2, shared_vals, width, label="Shared", color=c_shared, zorder=3)
    
    # 4. Styling
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='-', alpha=0.7)
    
    ax.set_xticks(x)
    ax.set_xticklabels([name for _, name in x_groups])
    ax.set_ylabel(f"{op_name.capitalize()} Throughput (KB/sec)")
    ax.set_title(f"Disk Performance Comparison: {op_name.capitalize()}")
    
    # Custom Legend (4 colors only)
    legend_elements = [
        mpatches.Patch(color=simple_colors["vm_local"],    label='VM (Local)'),
        mpatches.Patch(color=simple_colors["vm_shared"],   label='VM (Shared)'),
        mpatches.Patch(color=simple_colors["cont_local"],  label='Container (Local)'),
        mpatches.Patch(color=simple_colors["cont_shared"], label='Container (Shared)'),
    ]
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.02, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

# --- Main Execution ---

print("Loading Disk data...")
disk = pd.read_csv("../data/disk_summary.csv", sep=";")

# 1. Standard Plots
print("Generating Standard Plots...")
plot_disk_ops(get_op_data(disk, seq_ops), "Disk: Sequential Operations", "disk_sequential.png")
plot_disk_ops(get_op_data(disk, rand_ops), "Disk: Random Operations", "disk_random.png")
plot_disk_ops(get_op_data(disk, file_ops), "Disk: File Operations", "disk_file.png")
plot_disk_ops(get_op_data(disk, all_ops), "Disk: All Operations Combined", "disk_all_combined.png", figure_size=(24, 8))

# 2. NEW: Single Operation Comparison (4 Colors)
print("Generating Read Comparison Plot...")
plot_single_op_compare(disk, "read", "disk_read_compare.png")

print("All disk plots generated successfully.")