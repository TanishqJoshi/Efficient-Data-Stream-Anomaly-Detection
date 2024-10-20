# Efficient Data Stream Anomaly Detection

## Overview
This project implements a real-time data stream simulator combined with an anomaly detection mechanism using the Exponentially Weighted Moving Average (EWMA). The system detects unusual behavior or anomalies in the data stream and visualizes the results in real time through an animated plot.

## Features
- **Data Stream Simulation**: Generates a continuous stream of data incorporating seasonal trends, noise, and occasional anomalies.
- **Anomaly Detection**: Uses EWMA to detect anomalies based on deviations from expected behavior.
- **Real-time Visualization**: Displays the data stream and highlights detected anomalies in an animated plot.
- **Customization**: Allows users to adjust parameters like the smoothing factor `beta` and the anomaly threshold multiplier.

## Files
- `main.py`: Contains the code for data simulation, anomaly detection, and visualization.
- `requirements.txt`: Specifies the dependencies required to run the project.

## Anomaly Detection Algorithm:

1. **Data Stream Simulation**:
   - A real-time data stream is simulated using a combination of **seasonal** (sine wave), **trend** (linear increase), and **noise** (random variations) components.
   - Periodically, anomalies (large positive or negative spikes) are introduced with a 5% probability to mimic real-world unexpected events.

2. **EWMA Calculation**:
   - The anomaly detection uses EWMA to compute a smoothed value (`ewma`) that represents the expected behavior of the data, updating based on the previous values.
   - The algorithm also calculates the **EWMA standard deviation** (`ewma_std`) to track variability in the data over time.

3. **Anomaly Detection Logic**:
   - The current data value is compared to the smoothed value and its expected variability (EWMA standard deviation).
   - If the value deviates from the expected range (determined by the `ewma` and a multiple of the standard deviation, controlled by `threshold_multiplier`), it is flagged as an anomaly.
   - The detection sensitivity is controlled by `beta`, which determines how much weight is given to recent data versus historical data in the EWMA calculation.

4. **Parameter Validation**:
   - The algorithm includes checks to ensure the input parameters for anomaly detection (e.g., `beta`, `threshold_multiplier`, `ewma_std`) are valid.

### Effectiveness:
- **EWMA** is effective for detecting subtle and sudden shifts in data streams while being responsive to changes over time. It is widely used in scenarios where the data exhibits time-dependent patterns with occasional anomalies.
- By using both the smoothed value and variability (EWMA standard deviation), the algorithm adapts to normal variations in the data, reducing false positives while effectively catching true anomalies.
- The algorithm's **flexibility** (via parameters like `beta` and `threshold_multiplier`) allows it to be tuned for different data patterns and sensitivities.

  
## Customization
- **Smoothing Factor (`beta`)**: Adjusts the sensitivity of the EWMA to new data. A value closer to `1` makes it more responsive to changes, while a value closer to `0` makes it more stable.
- **Threshold Multiplier**: Adjusts the sensitivity of anomaly detection. Increasing this value will make the system less sensitive to smaller anomalies.

## Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project
Run the `main.py` script to start the simulation and anomaly detection process:
```bash
python main.py
```
This will open a window displaying the real-time data stream and highlight any detected anomalies.


