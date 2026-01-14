import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D  # Required for custom legends

# --- Configuration ---
groups = {
    "vm-master": ["vm_m"],
    "vm-node": ["vm_n04", "vm_n05"],
    "c-master": ["c_m"],
    "c-node": ["c_n01", "c_n02"]
}

# --- Helper Functions ---

def get_aggregated_df(raw_df, col_throughput, col_latency):
    """Aggregates raw data into a structured DataFrame."""
    agg_list = []
    for k, labels in groups.items():
        type_code, role_code = k.split("-")
        
        deployment_type = "VM" if type_code == "vm" else "Container"
        role = role_code.capitalize() # "Master" or "Node"
        
        tmp = raw_df[raw_df["label"].isin(labels)]
        
        agg_list.append({
            "Role": role,
            "Type": deployment_type,
            "throughput": tmp[col_throughput].mean(),
            "latency": tmp[col_latency].mean()
        })
        
    return pd.DataFrame(agg_list)

def plot_bar_metric(df, metric_col, ylabel, title, filename):
    """Generates the grouped bar charts."""
    plt.figure()
    
    pivot_df = df.pivot(index="Role", columns="Type", values=metric_col)
    pivot_df = pivot_df.reindex(columns=["VM", "Container"])
    
    ax = pivot_df.plot(kind="bar", color=["xkcd:blue blue", "darkorange"], rot=0, zorder=3)
    
    # Grid styling
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='-', alpha=0.7)
    
    ax.set_ylabel(ylabel)
    ax.set_xlabel("") 
    ax.set_title(title)
    ax.legend(title=None)
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_scatter(df, xlabel, title, filename):
    """Generates the Latency vs Throughput scatterplot."""
    plt.figure()
    ax = plt.gca()

    # Iterate rows to plot each point with specific Color/Marker
    for _, row in df.iterrows():
        
        # Color by Type
        color = "xkcd:blue blue" if row["Type"] == "VM" else "darkorange"
        
        # Marker by Role
        # 'o' for Master, '^' for Node
        marker = "o" if row["Role"] == "Master" else "^"
        
        plt.scatter(row["throughput"], row["latency"],
                    color=color, marker=marker, s=120, zorder=3)

    # Grid styling
    ax.set_axisbelow(True)
    ax.grid(True, linestyle='-', alpha=0.7)

    # Manual Legend Construction
    legend_elements = [
        # Shapes for Roles
        Line2D([0], [0], marker='o', color='w', label='Master',
               markerfacecolor='gray', markersize=10),
        Line2D([0], [0], marker='^', color='w', label='Node',
               markerfacecolor='gray', markersize=10),
        # Colors for Types
        Line2D([0], [0], marker='s', color='w', label='VM',
               markerfacecolor='xkcd:blue blue', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='Container',
               markerfacecolor='darkorange', markersize=10)
    ]

    plt.legend(handles=legend_elements, loc='best')
    
    plt.xlabel(xlabel)
    plt.ylabel("Latency (ms)")
    plt.title(title)
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# --- Main Execution ---

# 1. Process CPU Data
print("Processing CPU data...")
cpu = pd.read_csv("../cpu_summary.csv", sep=";")
cpu_agg = get_aggregated_df(cpu, "events_per_sec", "lat_avg_ms")

plot_bar_metric(cpu_agg, "throughput", "Events/sec", "CPU Throughput", "cpu_throughput.png")
plot_bar_metric(cpu_agg, "latency", "Latency (ms)", "CPU Latency", "cpu_latency.png")
plot_scatter(cpu_agg, "Throughput (events/s)", "CPU: Latency vs Throughput", "cpu_scatter.png")

# 2. Process Memory Data
print("Processing Memory data...")
mem = pd.read_csv("../mem_summary.csv", sep=";")
mem_agg = get_aggregated_df(mem, "operation_per_sec", "avg_lat(ms)")

plot_bar_metric(mem_agg, "throughput", "Ops/sec", "Memory Throughput", "mem_throughput.png")
plot_bar_metric(mem_agg, "latency", "Latency (ms)", "Memory Latency", "mem_latency.png")
plot_scatter(mem_agg, "Throughput (ops/s)", "Memory: Latency vs Throughput", "mem_scatter.png")

print("All plots generated successfully.")