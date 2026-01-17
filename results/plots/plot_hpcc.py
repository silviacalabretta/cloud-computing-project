import pandas as pd
import matplotlib.pyplot as plt
import io

# --- 1. Load the Data ---
# Assuming the file is named 'hpcc_summary.csv' and is in the same directory.
# We use sep=";" because your data is semi-colon separated.
filename = "hpcc_summary.csv"

# Creating the dummy file for demonstration purposes so you can run this script directly.
# You can remove this block if your file already exists.
csv_content = """N;NB;Time(s);Gflops/s
6144;64;12.5;1.24E+01
6144;128;13.74;1.13E+01
6144;192;19.01;8.14E+00
6144;256;23.15;6.68E+00
1024;192;0.11;6.80E+00
2048;192;0.53;1.08E+01
4096;192;4.14;1.11E+01
6144;192;20.61;7.51E+00
8192;192;58.94;6.22E+00
"""
# Use io.StringIO to read the string as if it were a file
df = pd.read_csv(io.StringIO(csv_content), sep=";")
# If reading from actual file, uncomment the line below and comment the one above:
# df = pd.read_csv(filename, sep=";")

# --- 2. Separate the Data ---

# Group 1: First 4 rows (N=6144 fixed, NB varies)
# Indices 0 to 3
df_nb = df.iloc[:4].copy()

# Group 2: Remaining rows (NB=192 fixed, N varies)
# Indices 4 to end
df_n = df.iloc[4:].copy()

# --- 3. Plotting ---
# Create a figure with 2 subplots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Subplot 1: Varying N (Problem Size) ---
ax1.plot(df_n["N"], df_n["Gflops/s"], marker='o', color='tab:orange', linewidth=2, markersize=8)
ax1.set_title("Performance vs Problem Size (N)\n(Fixed NB=192)")
ax1.set_xlabel("N", fontsize=12)
ax1.set_ylabel("Gflops/s", fontsize=12)
ax1.grid(True, linestyle='-', alpha=0.7)
ax1.tick_params(axis='both', which='major', labelsize=12)
# Force integer ticks for N if needed
ax1.set_xticks(df_n["N"])

# --- Subplot 2: Varying NB (Block Size) ---
ax2.plot(df_nb["NB"], df_nb["Gflops/s"], marker='o', color='orangered', linewidth=2, markersize=8)
ax2.set_title("Performance vs Block Size (NB)\n(Fixed N=6144)")
ax2.set_xlabel("NB", fontsize=12)
ax2.set_ylabel("Gflops/s", fontsize=12)
ax2.grid(True, linestyle='-', alpha=0.7)
ax2.tick_params(axis='both', which='major', labelsize=12)
# Force integer ticks for NB if needed
ax2.set_xticks(df_nb["NB"])



# --- 4. Final Layout and Save ---
plt.tight_layout()
plt.savefig("hpcc_performance.png")
print("Plot generated successfully: hpcc_performance.png")
plt.show()