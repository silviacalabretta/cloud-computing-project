import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# 1. LOAD DATA
df_cpu = pd.read_csv('cpu_summary.csv', sep=';')

df_mem = pd.read_csv('mem_summary.csv', sep=';')

df_net = pd.read_csv('net_summary.csv', sep=';')

df_disk = pd.read_csv('disk_summary.csv', sep=';')


# 2. DATA PREPARATION & PARSING

def parse_labels(df, is_network=False):
    """
    Parses 'label' column to extract Infrastructure (VM/Container)
    and Role/Path info.
    """
    infra_list = []
    role_list = []
    
    for label in df['label']:
        # Detect Infrastructure
        if label.startswith('vm'):
            infra = 'VM'
        elif label.startswith('c'):
            infra = 'Container'
        else:
            infra = 'Unknown'
        
        # Detect Role/Path
        if is_network:
            # e.g., vm_n04_m -> "Node -> Master"
            parts = label.split('_')
            # Heuristic: join the parts after the first one to form the path
            role = f"{parts[1]} to {parts[2]}" if len(parts) > 2 else "Unknown"
        else:
            # e.g., vm_m -> "Master", vm_n04 -> "Node"
            if '_m' in label:
                role = 'Master'
            else:
                role = 'Node'
                
        infra_list.append(infra)
        role_list.append(role)
        
    df['Infrastructure'] = infra_list
    df['Role'] = role_list
    return df

# Apply parsing
df_cpu = parse_labels(df_cpu)
df_mem = parse_labels(df_mem)
df_disk = parse_labels(df_disk)
df_net = parse_labels(df_net, is_network=True)

# 3. PLOTTING

sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 11})
colors = {"VM": "#4c72b0", "Container": "#dd8452"}

# Change layout to 3 Rows x 2 Columns to accommodate Disk
fig, axes = plt.subplots(3, 2, figsize=(16, 18))
plt.subplots_adjust(hspace=0.4, wspace=0.3)

# --- ROW 1: CPU & MEMORY ---

# Plot 1: CPU
sns.barplot(data=df_cpu, x="Role", y="events_per_sec", hue="Infrastructure", 
            ax=axes[0, 0], palette=colors, errorbar=None)
axes[0, 0].set_title("CPU Performance (Sysbench)")
axes[0, 0].set_ylabel("Events per Second (Higher is Better)")
axes[0, 0].legend(loc='lower center')

# Plot 2: Memory
sns.barplot(data=df_mem, x="Role", y="operation_per_sec", hue="Infrastructure", 
            ax=axes[0, 1], palette=colors, errorbar=None)
axes[0, 1].set_title("Memory Performance (Sysbench)")
axes[0, 1].set_ylabel("Operations per Second (Higher is Better)")

# --- ROW 2: NETWORK ---

# Plot 3: Network Throughput
sns.barplot(data=df_net, x="Role", y="Bitrate_up(Gbits/sec)", hue="Infrastructure", 
            ax=axes[1, 0], palette=colors)
axes[1, 0].set_title("Network Throughput (Higher is Better)")
axes[1, 0].set_ylabel("Bitrate (Gbps)")
axes[1, 0].set_xlabel("Connection Path")

# Plot 4: Network Latency
sns.barplot(data=df_net, x="Role", y="rtt_avg(ms)", hue="Infrastructure", 
            ax=axes[1, 1], palette=colors)
axes[1, 1].set_title("Network Latency (Lower is Better)")
axes[1, 1].set_ylabel("Avg RTT (ms)")
axes[1, 1].set_xlabel("Connection Path")

# --- ROW 3: DISK (Integrated) ---

# Filter Data for Local vs NFS
df_disk_local = df_disk[df_disk['filesystem'] == 'local']
df_disk_nfs = df_disk[df_disk['filesystem'] == 'NFS']

# Plot 5: Disk Write (Local)
sns.barplot(data=df_disk_local, x="Role", y="write", hue="Infrastructure", 
            ax=axes[2, 0], palette=colors, errorbar=None)
axes[2, 0].set_title("Disk Seq. Write - Local Storage")
axes[2, 0].set_ylabel("Throughput (kB/s)")
axes[2, 0].set_xlabel("Node Role")

# Plot 6: Disk Write (NFS)
sns.barplot(data=df_disk_nfs, x="Role", y="write", hue="Infrastructure", 
            ax=axes[2, 1], palette=colors, errorbar=None)
axes[2, 1].set_title("Disk Seq. Write - NFS Storage")
axes[2, 1].set_ylabel("Throughput (kB/s)")
axes[2, 1].set_xlabel("Node Role")

# Add overall title
fig.suptitle('Benchmark Comparison: VMs vs Containers (Master vs Nodes)', fontsize=16, y=0.92)

plt.show()