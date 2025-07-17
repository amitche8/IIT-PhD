import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

platform = "MAC"  # options MAC or Windows

# File paths
if platform == "MAC":
    data_set_1 = "data/All heatflux data-Pi 5.csv"
    data_set_2 = "data/All temperature data-Pi 5.csv"
else:
    data_set_1 = "data\\All heatflux data-Pi 5.csv"
    data_set_2 = "data\\All temperature data-Pi 5.csv"

# Load data and convert 'Time' to datetime explicitly

heatflux_df = pd.read_csv(data_set_1, parse_dates=['Time'])
temperature_df = pd.read_csv(data_set_2, parse_dates=['Time'])


heatflux_df['Time'] = pd.to_datetime(heatflux_df['Time'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
temperature_df['Time'] = pd.to_datetime(temperature_df['Time'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

# Filter date range
start_date = pd.to_datetime("2025-03-17")
end_date = pd.to_datetime("2025-03-21")
heatflux_df = heatflux_df[(heatflux_df['Time'] >= start_date) & (heatflux_df['Time'] <= end_date)]
temperature_df = temperature_df[(temperature_df['Time'] >= start_date) & (temperature_df['Time'] <= end_date)]

print(heatflux_df.columns.tolist())

# Define channels, labels, and styles
hf_cols = [
    "Heatflux - Pi 1 - Channel 1", "Heatflux - Pi 1 - Channel 2",
    "Heatflux - Pi 1 - Channel 3", "Heatflux - Pi 1 - Channel 4",
    "Heatflux - Pi 2 - Channel 1", "Heatflux - Pi 2 - Channel 2",
    "Heatflux - Pi 5 - Channel 1", "Heatflux - Pi 5 - Channel 2",
    "Heatflux - Pi 5 - Channel 3", "Heatflux - Pi 5 - Channel 4"
]

temp_cols = [
    "Temperature - Pi 1 - Channel 1", "Temperature - Pi 1 - Channel 2",
    "Temperature - Pi 1 - Channel 3", "Temperature - Pi 1 - Channel 4",
    "Temperature - Pi 2 - Channel 1", "Temperature - Pi 2 - Channel 2",
    "Temperature - Pi 5 - Channel 1", "Temperature - Pi 5 - Channel 2",
    "Temperature - Pi 5 - Channel 3", "Temperature - Pi 5 - Channel 4"
]

labels = [
    "House A - Below Grade Wall", "House A - Slab", "House A - Window", "House A - Above wall",
    "House T - Slab", "House T - Below Grade Wall",
    "House R - Below wall", "House R - Slab", "House R - Window", "House R - Above wall"
]

markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '*']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red',
          'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

marker_interval = 300
smooth_window = 10

# Smooth the data
heatflux_df[hf_cols] = heatflux_df[hf_cols].rolling(window=smooth_window, min_periods=1).mean()
temperature_df[temp_cols] = temperature_df[temp_cols].rolling(window=smooth_window, min_periods=1).mean()

# Font settings
plt.rcParams.update({'font.size': 14})

# Helper function for plotting
def plot_signals(df, cols, indices, title, ylabel, ylimits):
    plt.figure(figsize=(12, 5))
    for j, i in enumerate(indices):
        x = df['Time'].to_numpy()
        y = pd.to_numeric(df[cols[i]], errors='coerce').to_numpy()
        mask = ~pd.isna(y)
        plt.plot(
            x[mask], y[mask],
            label=labels[i], color=colors[j], marker=markers[j],
            markevery=marker_interval, markersize=5, linewidth=1.5
        )
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.ylim(*ylimits)
    if "Heat Flux" in ylabel:
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))

    # ✅ Use AutoDateLocator to prevent MAXTICKS error
    locator = mdates.AutoDateLocator(minticks=4, maxticks=12)
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))

    plt.xticks(rotation=45)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# -----------------------------
# House R - Pi 5
# -----------------------------
houseR_indices = [i for i, col in enumerate(hf_cols) if "Pi 5" in col]
plot_signals(heatflux_df, hf_cols, houseR_indices, "Heat Flux vs. Time (House R)", "Heat Flux [W/m²]", (-50, 50))
plot_signals(temperature_df, temp_cols, houseR_indices, "Temperature vs. Time (House R)", "Temperature [°C]", (18, 28))

# -----------------------------
# House T - Pi 2
# -----------------------------
houseT_indices = [i for i, col in enumerate(hf_cols) if "Pi 2" in col]
plot_signals(heatflux_df, hf_cols, houseT_indices, "Heat Flux vs. Time (House T)", "Heat Flux [W/m²]", (-50, 50))
plot_signals(temperature_df, temp_cols, houseT_indices, "Temperature vs. Time (House T)", "Temperature [°C]", (18, 28))

# -----------------------------
# House A - Pi 1
# -----------------------------
houseA_indices = [i for i, col in enumerate(hf_cols) if "Pi 1" in col]
plot_signals(heatflux_df, hf_cols, houseA_indices, "Heat Flux vs. Time (House A)", "Heat Flux [W/m²]", (-50, 50))
plot_signals(temperature_df, temp_cols, houseA_indices, "Temperature vs. Time (House A)", "Temperature [°C]", (18, 28))

plt.figure(figsize=(10, 4))

plt.plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 1 - Channel 3"].to_numpy(), label="House A - Slab", marker='o', markevery=100)
plt.plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 2 - Channel 1"].to_numpy(), label="House T - Slab", marker='s', markevery=100)
plt.plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 5 - Channel 2"].to_numpy(), label="House R - Slab", marker='^', markevery=100)

plt.title("Heat Flux - Slab (All Houses)")
plt.xlabel("Time")
plt.ylabel("Heat Flux [W/m²]")
plt.ylim(-10, 30)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))

plt.plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 1 - Channel 3"].to_numpy(), label="House A - Slab", marker='o', markevery=100)
plt.plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 2 - Channel 1"].to_numpy(), label="House T - Slab", marker='s', markevery=100)
plt.plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 5 - Channel 2"].to_numpy(), label="House R - Slab", marker='^', markevery=100)


plt.title("Temperature - Slab (All Houses)")
plt.xlabel("Time")
plt.ylabel("Temperature [°C]")
plt.ylim(16, 24)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Load simulation data with fixed format
sim_df = pd.read_csv("data/Simulation.csv")

# Clean and prepend year to Time string
sim_df['Time'] = '2025/' + sim_df['Time'].str.strip()  # becomes e.g. "2025/03/17 07:00:00"

# Parse datetime explicitly
sim_df['Time'] = pd.to_datetime(sim_df['Time'], format='%Y/%m/%d %H:%M:%S', errors='coerce')



# Align time range to House T
common_start = max(heatflux_df['Time'].min(), sim_df['Time'].min())
common_end = min(heatflux_df['Time'].max(), sim_df['Time'].max())

print(sim_df[['Slab Column 1', 'Slab Column 2']].describe())


# Plot House T slab (Channel 1 on Pi 2) + Simulation columns

# Determine overlapping time window
common_start = max(heatflux_df['Time'].min(), sim_df['Time'].min())
common_end = min(heatflux_df['Time'].max(), sim_df['Time'].max())

print("Heatflux Time Range:", heatflux_df['Time'].min(), "to", heatflux_df['Time'].max())
print("Simulation Time Range:", sim_df['Time'].min(), "to", sim_df['Time'].max())
print(sim_df['Time'].isna().sum())


# Plot House T slab (Channel 1 on Pi 2) + Simulation columns
plt.figure(figsize=(10, 5))

plt.plot(
    heatflux_df['Time'].to_numpy(),
    heatflux_df['Heatflux - Pi 2 - Channel 1'].to_numpy(),
    label="House T - Slab",
    marker='o', markevery=300, linewidth=1
)

plt.plot(
    sim_df['Time'].to_numpy(),
    sim_df['Slab Column 1'].to_numpy(),
    label="Simulation - Slab Column 1",
    linestyle='--', marker='s', markevery=5, linewidth=2
)

plt.plot(
    sim_df['Time'].to_numpy(),
    sim_df['Slab Column 2'].to_numpy(),
    label="Simulation - Slab Column 2",
    linestyle='-.', marker='^', markevery=5, linewidth=2
)

# Apply time range limit to x-axis
plt.xlim([common_start, common_end])

plt.grid(True, which='both', linestyle=':', linewidth=0.7)
plt.legend(fontsize=10)
plt.xlabel("Time")
plt.ylabel("Heat Flux [W/m²]")
plt.title("House T Slab vs. Simulated Columns")
plt.ylim(-10, 10)
plt.tight_layout()
plt.show()
