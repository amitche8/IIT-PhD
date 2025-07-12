import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# File paths
# data_set_1 = "data/All heatflux data-Pi 5.csv"
# data_set_2 = "data/All temperature data-Pi 5.csv"

data_set_1 = 'D:/GitHub/IIT-PhD/.git/Field Study/data/All heatflux data-Pi 5.csv'
data_set_2 = 'D:/GitHub/IIT-PhD/.git/Field Study/data/All temperature data-Pi 5.csv'

# Load data
heatflux_df = pd.read_csv(data_set_1, parse_dates=['Time'])
temperature_df = pd.read_csv(data_set_2, parse_dates=['Time'])

# Filter date range
start_date = pd.to_datetime("2025-03-17")
end_date = pd.to_datetime("2025-03-21")
heatflux_df = heatflux_df[(heatflux_df['Time'] >= start_date) & (heatflux_df['Time'] <= end_date)]
temperature_df = temperature_df[(temperature_df['Time'] >= start_date) & (temperature_df['Time'] <= end_date)]

# Define channels, labels, and styles
hf_cols = [f"Heatflux - Pi 5 - Channel {i}" for i in range(1, 5)]
temp_cols = [f"Temperature - Pi 5 - Channel {i}" for i in range(1, 5)]
labels = ["Below wall", "Slab", "Window", "Above wall"]
markers = ['o', 's', '^', 'D']
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
marker_interval = 300  # spacing for marker visibility
smooth_window = 10  # rolling window in number of points (~10 min for 1-min data)

# Smooth the data
heatflux_df[hf_cols] = heatflux_df[hf_cols].rolling(window=smooth_window, min_periods=1).mean()
temperature_df[temp_cols] = temperature_df[temp_cols].rolling(window=smooth_window, min_periods=1).mean()

# Font settings
plt.rcParams.update({'font.size': 14})

# Plot Heat Flux
plt.figure(figsize=(12, 5))
for col, label, marker, color in zip(hf_cols, labels, markers, colors):
    plt.plot(
        heatflux_df['Time'], heatflux_df[col], label=label, color=color,
        marker=marker, markevery=marker_interval, markersize=5, linewidth=1.5
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

# Plot Temperature
plt.figure(figsize=(12, 5))
for col, label, marker, color in zip(temp_cols, labels, markers, colors):
    plt.plot(
        temperature_df['Time'], temperature_df[col], label=label, color=color,
        marker=marker, markevery=marker_interval, markersize=5, linewidth=1.5
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
