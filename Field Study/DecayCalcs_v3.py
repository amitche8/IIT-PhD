import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# File paths
house_files = {
    "A": "0_A_Complete Data.xlsx",
    "R": "0_R_Complete Data.xlsx",
    "T": "0_T_Complete Data.xlsx"
}
sensors = {
    "A": ["A_1_N_T  [°C]", "A_2_N_T  [°C]", "A_3_N_T  [°C]"],
    "R": ["R_1_W_T  [°C]", "R_2_W_T  [°C]", "R_3_W_T  [°C]"],
    "T": ["T_1_W_T  [°C]", "T_2_W_T  [°C]", "T_3_W_T  [°C]"]
}

# Constants
timestamp_col = "Date-Time (CDT)"
r2_threshold = 0.7
outdoor_temp_stability_threshold = 2.0
start_time = pd.to_datetime("2025-03-21 18:00:00") # outage start
end_time = pd.to_datetime("2025-03-22 18:11:00") # the first 24 hours
output_dir = "Decay_Plots"
os.makedirs(output_dir, exist_ok=True)

# Time constant equation
def exp_decay(t, Tf, delta_T, tau):
    return Tf + delta_T * np.exp(-t / tau)

# data frame for the calculated values
records = []

for house, file_path in house_files.items():
    df = pd.read_excel(file_path)
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df = df.set_index(timestamp_col).sort_index()
    df_window = df.loc[start_time:end_time]

    # Include original temperature sensors and detected MRT columns
    all_columns = df_window.columns
    mrt_cols = [col for col in all_columns if "MRT" in col and col.startswith(house)]
    sensor_list = sensors[house] + mrt_cols

    for sensor_col in sensor_list:
        O_col = f"{house}_O_T [°C]"
        if sensor_col not in df_window or O_col not in df_window:
            continue

        temp_data = df_window[[sensor_col, O_col]].dropna()
        if temp_data.empty:
            continue

        times = (temp_data.index - temp_data.index[0]).total_seconds() / 3600
        indoor_T = temp_data[sensor_col].values
        outdoor_T = temp_data[O_col].values

        T_out_start = outdoor_T[0]
        mask = outdoor_T <= T_out_start + outdoor_temp_stability_threshold
        stable_data = temp_data[mask]

        if len(stable_data) < 10:
            continue

        t_hours = (stable_data.index - stable_data.index[0]).total_seconds() / 3600
        indoor_stable = stable_data[sensor_col].values
        outdoor_stable = stable_data[O_col].values

        try:
            popt, _ = curve_fit(exp_decay, t_hours, indoor_stable,
                                p0=(indoor_stable[-1], indoor_stable[0] - indoor_stable[-1], 1),
                                maxfev=10000)
            Tf, delta_T, tau_hr = popt
            fit_vals = exp_decay(t_hours, *popt)
            T_tau = exp_decay(tau_hr, *popt)

            ss_res = np.sum((indoor_stable - fit_vals) ** 2)
            ss_tot = np.sum((indoor_stable - np.mean(indoor_stable)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            Ti = indoor_stable[0]
            delta_Ti = abs(Ti - Tf)

            # Filter conditions
            if (r_squared < r2_threshold or tau_hr > 100 or Tf < 0 or delta_Ti < 0.2):
                continue

            # Plot
            t_ext = np.linspace(0, 5 * tau_hr, 300)
            ext_vals = exp_decay(t_ext, *popt)

            plt.figure(figsize=(8, 4))
            plt.plot(t_hours, indoor_stable, 'o', label='Measured')
            plt.plot(t_hours, fit_vals, '-', label='Fit')
            plt.plot(t_ext, ext_vals, '--', label='Extrapolated', color='gray')
            plt.axhline(Tf, linestyle=':', color='black', label=f'Tf = {Tf:.2f}°C')
            plt.plot(tau_hr, T_tau, 'ro', label=f'T(τ) = {T_tau:.2f}°C')
            plt.title(f"{house} - {sensor_col} | R²={r_squared:.2f}, τ={tau_hr:.2f} hr")
            plt.xlim([0, 50])
            plt.xlabel("Time (hr)")
            plt.ylim([12, 24])
            plt.ylabel("Temperature (°C)")
            plt.legend()
            plt.grid(True, linestyle=':')
            plt.tight_layout()

            safe_name = sensor_col.replace(" ", "").replace("[°C]", "").replace("[%", "").replace("/", "_")
            fig_name = f"{house}_{safe_name}_decay.png"
            plt.savefig(os.path.join(output_dir, fig_name))
            plt.close()

            # Interpolate outdoor temperature at tau
            outdoor_series = pd.Series(outdoor_stable, index=t_hours)
            outdoor_interp = outdoor_series.interpolate(method='linear')
            T_out_tau = np.interp(tau_hr, outdoor_interp.index, outdoor_interp.values) if tau_hr <= t_hours.max() else np.nan
            

            records.append({
                "House": house,
                "Sensor": sensor_col,
                "Start Time": stable_data.index[0],
                "End Time": stable_data.index[-1],
                "Tau (hr)": tau_hr,
                "Ti (°C)": Ti,
                "Tf (°C)": Tf,
                "T(τ) (°C)": T_tau,
                "Outdoor Start (°C)": outdoor_stable[0],
                "Outdoor End (°C)": outdoor_stable[-1],
                "Outdoor at τ (°C)": T_out_tau,
                "R²": r_squared,
                "Plot File": fig_name
            })
        except:
            continue

# Save final results
df_final = pd.DataFrame(records)

# === Generate summary statistics by house ===
if len(records) > 0:
    records_df = pd.DataFrame(records)
    records_df.to_csv('Decay_Results_With_MRT.csv', index=False)

    summary_stats = records_df.groupby("House")["Tau (hr)"].agg(
        Average="mean",
        StdDev="std",
        Max="max",
        Min="min",
        Median="median"
    ).reset_index()
    summary_stats.to_csv("Decay_Stats_Summary_By_House.csv", index=False)
    print("✅ Summary statistics saved to 'Decay_Stats_Summary_By_House.csv'")
else:
    print("⚠️ No decay results to summarize.")


# === Generate summary statistics by house and floor ===
if len(records) > 0:
    records_df = pd.DataFrame(records)

    # Extract floor number from sensor names (e.g., R_1_E_T → Floor = 1)
    records_df["Floor"] = records_df["Sensor"].str.extract(r"_(\d+)_")[0]

    floor_stats = records_df.groupby(["House", "Floor"])["Tau (hr)"].agg(
        Average="mean",
        StdDev="std",
        Max="max",
        Min="min",
        Median="median"
    ).reset_index()

    floor_stats.to_csv("Decay_Stats_By_House_And_Floor.csv", index=False)
    print("✅ Floor-level summary saved to 'Decay_Stats_By_House_And_Floor.csv'")
