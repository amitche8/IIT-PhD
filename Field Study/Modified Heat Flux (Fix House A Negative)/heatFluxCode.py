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


# Plot slab and below grade which are common for all homes in one figure with subplots or separately 
subplot_slab = "Yes" # options Yes or No 

if subplot_slab == "Yes":

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Subplot 1: Slab Heat Flux
    axs[0].plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 1 - Channel 3"].to_numpy(), label="House A - Slab", marker='D', markersize=8, markevery=100)
    axs[0].plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 2 - Channel 1"].to_numpy(), label="House T - Slab", marker='s', markersize=8, markevery=100)
    axs[0].plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 5 - Channel 2"].to_numpy(), label="House R - Slab", marker='x', markersize=8, markevery=100)
    axs[0].set_title("(a): Slab Heat Flux for the Three Houses")
    axs[0].set_ylabel("Heat Flux [W/m²]")
    axs[0].set_ylim(-15, 35)
    axs[0].legend()
    axs[0].grid(True)

    # Subplot 2: Below Grade Wall Heat Flux
    axs[1].plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 1 - Channel 2"].to_numpy(), label="House A - Below Grade Wall", marker='D', markersize=8, markevery=100)
    axs[1].plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 2 - Channel 2"].to_numpy(), label="House T - Below Grade Wall", marker='s', markersize=8, markevery=100)
    axs[1].plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 5 - Channel 1"].to_numpy(), label="House R - Below Grade Wall", marker='x', markersize=8, markevery=100)
    axs[1].set_title("(b): Below Grade Wall Heat Flux for the Three Houses)")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Heat Flux [W/m²]")
    axs[1].set_ylim(-15, 35)
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Subplot 1: Slab Temperature
    axs[0].plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 1 - Channel 3"].to_numpy(), label="House A - Slab", marker='o', markevery=100)
    axs[0].plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 2 - Channel 1"].to_numpy(), label="House T - Slab", marker='s', markevery=100)
    axs[0].plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 5 - Channel 2"].to_numpy(), label="House R - Slab", marker='^', markevery=100)
    axs[0].set_title("Temperature - Slab (All Houses)")
    axs[0].set_ylabel("Temperature [°C]")
    axs[0].set_ylim(16, 24)
    axs[0].legend()
    axs[0].grid(True)

    # Subplot 2: Below Grade Wall Temperature
    axs[1].plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 1 - Channel 2"].to_numpy(), label="House A - Below Grade Wall", marker='o', markevery=100)
    axs[1].plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 2 - Channel 2"].to_numpy(), label="House T - Below Grade Wall", marker='s', markevery=100)
    axs[1].plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 5 - Channel 1"].to_numpy(), label="House R - Below Grade Wall", marker='^', markevery=100)
    axs[1].set_title("Temperature - Below Grade Wall (All Houses)")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Temperature [°C]")
    axs[1].set_ylim(16, 24)
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

else:
    #
    # Slab readings for all houses
    #

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

    #
    # Wall below grade readings for all houses
    #


    plt.figure(figsize=(10, 4))

    plt.plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 1 - Channel 2"].to_numpy(), label="House A - Below Grade Wall", marker='o', markevery=100)
    plt.plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 2 - Channel 2"].to_numpy(), label="House T - Below Grade Wall", marker='s', markevery=100)
    plt.plot(heatflux_df['Time'].to_numpy(), heatflux_df["Heatflux - Pi 5 - Channel 1"].to_numpy(), label="House R - Below Grade Wall", marker='^', markevery=100)

    plt.title("Heat Flux - Below Grade Wall (All Houses)")
    plt.xlabel("Time")
    plt.ylabel("Heat Flux [W/m²]")
    plt.ylim(-10, 30)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 4))

    plt.plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 1 - Channel 2"].to_numpy(), label="House A - Below Grade Wall", marker='o', markevery=100)
    plt.plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 2 - Channel 2"].to_numpy(), label="House T - Below Grade Wall", marker='s', markevery=100)
    plt.plot(temperature_df['Time'].to_numpy(), temperature_df["Temperature - Pi 5 - Channel 1"].to_numpy(), label="House R - Below Grade Wall", marker='^', markevery=100)


    plt.title("Temperature - Below Grade Wall (All Houses)")
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




# Plot Simulation Results

# Load simulation data with fixed format
sim_df2 = pd.read_csv("data/SimulationSlab.csv")

# Clean and prepend year to Time string
sim_df2['Time'] = '2025/' + sim_df2['Time'].str.strip()  # becomes e.g. "2025/03/17 07:00:00"

# Parse datetime explicitly
sim_df2['Time'] = pd.to_datetime(sim_df2['Time'], format='%Y/%m/%d %H:%M:%S', errors='coerce')

# Determine overlapping time window
common_start = pd.to_datetime("2025-01-01 01:00:00")
common_end = pd.to_datetime("2025-03-31 01:00:00")


plt.figure(figsize=(10, 5))

plt.plot(
    sim_df2['Time'].to_numpy(),
    sim_df2['Slab Unins'].to_numpy(),
    label="Uninsulated Basement Conductive Heat Flux",
    linestyle='--', marker='s', markevery=5, linewidth=2
)

plt.plot(
    sim_df2['Time'].to_numpy(),
    sim_df2['Slab Insulated'].to_numpy(),
    label="Insulated Basement Conductive Heat Flux",
    linestyle='-.', marker='^', markevery=5, linewidth=2
)

# Apply time range limit to x-axis
plt.xlim([common_start, common_end])

plt.grid(True, which='both', linestyle=':', linewidth=0.7)
plt.legend(fontsize=10)
plt.xlim([common_start, common_end])

# Set ticks explicitly to include start and end
xticks = pd.date_range(start=common_start, end=common_end, periods=6)  # or use freq='MS' for monthly ticks
plt.xticks(xticks, [dt.strftime('%Y-%m-%d') for dt in xticks])

plt.xlabel("Date", fontsize=14)
plt.ylabel("Heat Flux [W/m²]", fontsize=14)
plt.title("Simulated Basement Conductive Heat Flux for House T")
plt.ylim(-30, 30)
plt.yticks(range(-30, 31, 10))  # from -25 to 25, step 5
plt.tight_layout()
plt.legend(fontsize=14)
plt.show()
