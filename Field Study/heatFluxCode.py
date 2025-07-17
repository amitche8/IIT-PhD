import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

platform = "MAC" # options MAC or Windows

# File paths

if platform == "MAC":
    data_set_1 = "data/All heatflux data-Pi 5.csv"
    data_set_2 = "data/All temperature data-Pi 5.csv"
else:
    data_set_1 = "data\All heatflux data-Pi 5.csv"
    data_set_2 = "data\All temperature data-Pi 5.csv"

# Load data
heatflux_df = pd.read_csv(data_set_1, parse_dates=['Time'])
temperature_df = pd.read_csv(data_set_2, parse_dates=['Time'])

# Filter date range
start_date = pd.to_datetime("2025-03-17")
end_date = pd.to_datetime("2025-03-21")
heatflux_df = heatflux_df[(heatflux_df['Time'] >= start_date) & (heatflux_df['Time'] <= end_date)]
temperature_df = temperature_df[(temperature_df['Time'] >= start_date) & (temperature_df['Time'] <= end_date)]

print(heatflux_df.columns.tolist())

# Define channels, labels, and styles
hf_cols = [
    "Heatflux - Pi 1 - Channel 1", "Heatflux - Pi 1 - Channel 2",
    "Heatflux - Pi 1 - Channel 3",     
    "Heatflux - Pi 2 - Channel 1", "Heatflux - Pi 2 - Channel 2",
    "Heatflux - Pi 5 - Channel 1", "Heatflux - Pi 5 - Channel 2",
    "Heatflux - Pi 5 - Channel 3", "Heatflux - Pi 5 - Channel 4"
]

temp_cols = [
    "Temperature - Pi 1 - Channel 1", "Temperature - Pi 1 - Channel 2",
    "Temperature - Pi 1 - Channel 3",     
    "Temperature - Pi 2 - Channel 1", "Temperature - Pi 2 - Channel 2",
    "Temperature - Pi 5 - Channel 1", "Temperature - Pi 5 - Channel 2",
    "Temperature - Pi 5 - Channel 3", "Temperature - Pi 5 - Channel 4"
]



labels = [
    "House R - Below wall", "House R - Slab", "House R - Window", "House R - Above wall",
    "House T - Slab", "House T - Below Grade Wall",
    "House A - Below Grade Wall", "House A - Slab", "House A - Window", "House A - Above wall"
]

markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '*']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 
          'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
marker_interval = 300  # spacing for marker visibility
smooth_window = 10  # rolling window in number of points (~10 min for 1-min data)

# Smooth the data
heatflux_df[hf_cols] = heatflux_df[hf_cols].rolling(window=smooth_window, min_periods=1).mean()
temperature_df[temp_cols] = temperature_df[temp_cols].rolling(window=smooth_window, min_periods=1).mean()

# Font settings
plt.rcParams.update({'font.size': 14})

# -----------------------------
# House A - Pi 1
# -----------------------------
# Get indices of House A (Pi 1)
houseA_indices = [i for i, col in enumerate(hf_cols) if "Pi 1" in col]

# Heat Flux Plot
plt.figure(figsize=(12, 5))
for j, i in enumerate(houseA_indices):
    col = hf_cols[i]
    plt.plot(
        heatflux_df['Time'], heatflux_df[col], label=labels[i],
        color=colors[j], marker=markers[j], markevery=marker_interval,
        markersize=5, linewidth=1.5
    )
plt.xlabel('Time')
plt.ylabel('Heat Flux [W/m²]')
plt.title('Heat Flux vs. Time (House A)')
plt.ylim(-50, 50)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Temperature Plot
houseA_temp_indices = [i for i, col in enumerate(temp_cols) if "Pi 1" in col]
plt.figure(figsize=(12, 5))
for j, i in enumerate(houseA_temp_indices):
    col = temp_cols[i]
    plt.plot(
        temperature_df['Time'], temperature_df[col], label=labels[i],
        color=colors[j], marker=markers[j], markevery=marker_interval,
        markersize=5, linewidth=1.5
    )
plt.xlabel('Time')
plt.ylabel('Temperature [°C]')
plt.title('Temperature vs. Time (House A)')
plt.ylim(18, 28)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()



# -----------------------------
# House T - Pi 2
# -----------------------------
# Get indices of House T (Pi 2)
houseT_indices = [i for i, col in enumerate(hf_cols) if "Pi 2" in col]

# Heat Flux Plot
plt.figure(figsize=(12, 5))
for j, i in enumerate(houseT_indices):
    col = hf_cols[i]
    plt.plot(
        heatflux_df['Time'], heatflux_df[col], label=labels[i],
        color=colors[j], marker=markers[j], markevery=marker_interval,
        markersize=5, linewidth=1.5
    )
plt.xlabel('Time')
plt.ylabel('Heat Flux [W/m²]')
plt.title('Heat Flux vs. Time (House T)')
plt.ylim(-50, 50)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Temperature Plot
houseT_temp_indices = [i for i, col in enumerate(temp_cols) if "Pi 2" in col]
plt.figure(figsize=(12, 5))
for j, i in enumerate(houseT_temp_indices):
    col = temp_cols[i]
    plt.plot(
        temperature_df['Time'], temperature_df[col], label=labels[i],
        color=colors[j], marker=markers[j], markevery=marker_interval,
        markersize=5, linewidth=1.5
    )
plt.xlabel('Time')
plt.ylabel('Temperature [°C]')
plt.title('Temperature vs. Time (House T)')
plt.ylim(18, 28)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()


# -----------------------------
# House R - Pi 5
# -----------------------------
# Get indices of House R (Pi 5)
houseR_indices = [i for i, col in enumerate(hf_cols) if "Pi 5" in col]

# Heat Flux Plot
plt.figure(figsize=(12, 5))
for j, i in enumerate(houseR_indices):
    col = hf_cols[i]
    plt.plot(
        heatflux_df['Time'], heatflux_df[col], label=labels[i],
        color=colors[j], marker=markers[j], markevery=marker_interval,
        markersize=5, linewidth=1.5
    )
plt.xlabel('Time')
plt.ylabel('Heat Flux [W/m²]')
plt.title('Heat Flux vs. Time (House R)')
plt.ylim(-50, 50)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Temperature Plot
houseR_temp_indices = [i for i, col in enumerate(temp_cols) if "Pi 5" in col]
plt.figure(figsize=(12, 5))
for j, i in enumerate(houseR_temp_indices):
    col = temp_cols[i]
    plt.plot(
        temperature_df['Time'], temperature_df[col], label=labels[i],
        color=colors[j], marker=markers[j], markevery=marker_interval,
        markersize=5, linewidth=1.5
    )
plt.xlabel('Time')
plt.ylabel('Temperature [°C]')
plt.title('Temperature vs. Time (House R)')
plt.ylim(18, 28)
plt.gca().xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 6, 12, 18]))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
plt.xticks(rotation=45)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
