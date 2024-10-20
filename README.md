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

## How It Works
1. **Data Stream**: The `data_stream()` function generates real-time data incorporating:
   - A seasonal pattern (modeled as a sine wave),
   - A linear trend, and
   - Random noise with a chance of introducing anomalies (spikes).

2. **Anomaly Detection**: The `anomaly_detection()` function uses the EWMA of the data and its standard deviation to detect anomalies. If the current data point deviates from the expected value by more than a set threshold, it is flagged as an anomaly.

3. **Real-Time Visualization**: 
   - The data stream is visualized in an animated plot using `matplotlib.animation`. 
   - Anomalies are highlighted with red scatter points on the plot, updating in real-time as the data stream progresses.
  
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


