import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# --- Configuration ---
# Map raw labels to (Type, Role)
# We break this down so we can pivot the data
label_mapping_data = {
    "vm_n04_m":   {"Type": "VM",        "Role": "Master-Node"},
    "vm_n05_n04": {"Type": "VM",        "Role": "Node-Node"},
    "c_n01_m":    {"Type": "Container", "Role": "Master-Node"},
    "c_n02_n01":  {"Type": "Container", "Role": "Node-Node"}
}

# Throughput specific label map (still used for the second plot)
throughput_label_map = {
    "vm_n04_m":   "VM Master-Node",
    "vm_n05_n04": "VM Node-Node",
    "c_n01_m":    "Cont Master-Node",
    "c_n02_n01":  "Cont Node-Node"
}

# Throughput Colors
color_up_vm   = "xkcd:blue"
color_down_vm = "slateblue"
color_up_cont   = "tab:orange"
color_down_cont = "orangered"

# --- Helper Functions ---

def plot_rtt_grouped(df, filename):
    plt.figure(figsize=(10, 6))
    
    # 1. Prepare Data
    plot_data = []
    for raw_label, info in label_mapping_data.items():
        # Find the row in the dataframe
        row = df[df["label"] == raw_label]
        if not row.empty:
            val = row["rtt_avg(ms)"].values[0]
            plot_data.append({
                "Role": info["Role"],
                "Type": info["Type"],
                "RTT": val
            })
            
    df_agg = pd.DataFrame(plot_data)
    
    # 2. Pivot: Index=Role, Columns=Type
    pivot_df = df_agg.pivot(index="Role", columns="Type", values="RTT")
    
    # 3. Force Order: 
    # Columns: VM first, Container second
    pivot_df = pivot_df.reindex(columns=["VM", "Container"])
    # Index: Master-Node first, Node-Node second (optional, but good for consistency)
    pivot_df = pivot_df.reindex(["Master-Node", "Node-Node"])
    
    # 4. Plot
    ax = pivot_df.plot(kind="bar", 
                       color=["xkcd:blue", "tab:orange"], 
                       rot=0, 
                       zorder=3)
    
    # 5. Styling
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='-', alpha=0.7)
    
    ax.set_ylabel("RTT (ms)")
    ax.set_xlabel("") 
    ax.set_title("Network Latency (RTT)")
    ax.legend(title=None)
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_throughput(df, filename):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Order for the throughput plot (keeping 4 groups distinct as requested previously)
    ordered_keys = ["vm_n04_m", "vm_n05_n04", "c_n01_m", "c_n02_n01"]
    df = df.set_index("label").reindex(ordered_keys).reset_index()
    
    x = np.arange(len(ordered_keys))
    width = 0.35
    clean_labels = [throughput_label_map[k] for k in ordered_keys]
    
    # Prepare color lists
    c_up = []
    c_down = []
    
    for label in ordered_keys:
        if label.startswith("vm"):
            c_up.append(color_up_vm)
            c_down.append(color_down_vm)
        else:
            c_up.append(color_up_cont)
            c_down.append(color_down_cont)
    
    # Plot Upload bars (Left)
    ax.bar(x - width/2, df["Bitrate_up(Gbits/sec)"], width, 
           color=c_up, label="Upload", zorder=3)
    
    # Plot Download bars (Right)
    ax.bar(x + width/2, df["Bitrate_down(Gbits/sec)"], width, 
           color=c_down, label="Download", zorder=3)
    
    # Styling
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='-', alpha=0.7)
    
    ax.set_xticks(x)
    ax.set_xticklabels(clean_labels, rotation=0)
    ax.set_ylabel("Throughput (Gbits/sec)")
    ax.set_title("Network Throughput: Upload vs Download")
    
    # Custom Legend
    legend_handles = [
        mpatches.Patch(color=color_up_vm, label="VM Upload"),
        mpatches.Patch(color=color_down_vm, label="VM Download"),
        mpatches.Patch(color=color_up_cont, label="Cont Upload"),
        mpatches.Patch(color=color_down_cont, label="Cont Download"),
    ]
    
    # Legend outside right
    ax.legend(handles=legend_handles, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

# --- Main Execution ---

print("Loading Network data...")
net = pd.read_csv("../net_summary.csv", sep=";")

print("Generating Network RTT plot...")
plot_rtt_grouped(net, "net_rtt.png")

print("Generating Network Throughput plot...")
plot_throughput(net, "net_upload_download.png")

print("All network plots generated successfully.")