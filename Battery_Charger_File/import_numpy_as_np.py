import numpy as np
import matplotlib.pyplot as plt
import time

# -------------------------------
# Battery Charging Parameters
# -------------------------------
battery_capacity_mAh = 3000          # Battery capacity in mAh
initial_voltage = 3.0                # Starting voltage in volts
max_voltage = 4.2                    # Cutoff voltage in volts (Li-ion)
charge_current = 1.5                 # Charging current in Amps (constant current phase)
internal_resistance = 0.05           # Ohm - internal resistance of the battery
time_step = 1                        # in seconds
total_time = 7200                    # 2 hours max charging simulation
cv_threshold_voltage = 4.0           # Switch to CV mode at this voltage
cutoff_current = 0.1                 # Stop charging when current drops below this in CV phase

# -------------------------------
# Initialize data lists
# -------------------------------
time_series = []
voltage_series = []
current_series = []
power_series = []

# -------------------------------
# Simulate CC-CV Charging
# -------------------------------
def simulate_cc_cv_charging():
    voltage = initial_voltage
    capacity_charged = 0.0
    mode = "CC"  # Start in Constant Current mode

    for t in range(0, total_time, time_step):
        if mode == "CC":
            current = charge_current
            voltage_rise = (charge_current * internal_resistance) + 0.001  # tiny voltage increment
            voltage += voltage_rise * time_step / 100
            if voltage >= cv_threshold_voltage:
                mode = "CV"
                print(f"[INFO] Switching to CV mode at t = {t}s, V = {voltage:.2f}V")

        elif mode == "CV":
            voltage = max_voltage
            current = max((max_voltage - voltage) / internal_resistance, cutoff_current)
            if current <= cutoff_current:
                print(f"[INFO] Charging complete at t = {t}s")
                break

        energy = voltage * current
        capacity_charged += (current * time_step / 3600)  # Convert to mAh

        # Store data
        time_series.append(t)
        voltage_series.append(voltage)
        current_series.append(current)
        power_series.append(voltage * current)

        # Simulate processing time (comment this line out for faster execution)
        # time.sleep(0.001)

        # Stop if capacity is full
        if capacity_charged >= battery_capacity_mAh:
            print(f"[INFO] Battery reached full capacity at t = {t}s")
            break

    return capacity_charged

# -------------------------------
# Plot results
# -------------------------------
def plot_results():
    plt.figure(figsize=(15, 8))

    plt.subplot(3, 1, 1)
    plt.plot(time_series, voltage_series, label="Voltage (V)", color="blue")
    plt.ylabel("Voltage (V)")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time_series, current_series, label="Current (A)", color="green")
    plt.ylabel("Current (A)")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time_series, power_series, label="Power (W)", color="red")
    plt.xlabel("Time (s)")
    plt.ylabel("Power (W)")
    plt.grid(True)
    plt.legend()

    plt.suptitle("Battery Charging Simulation - CC/CV Method", fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

# -------------------------------
# Report Summary
# -------------------------------
def report_summary(capacity):
    total_energy = np.trapz(power_series, time_series) / 3600  # in Watt-hours
    print("\n======== Charging Summary ========")
    print(f"Total Charging Time   : {time_series[-1]} seconds ({time_series[-1]/60:.2f} minutes)")
    print(f"Capacity Charged      : {capacity:.2f} mAh")
    print(f"Estimated Energy Used : {total_energy:.2f} Wh")
    print("==================================\n")

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    print("[START] Battery Charging Simulation\n")
    charged_capacity = simulate_cc_cv_charging()
    report_summary(charged_capacity)
    plot_results()
