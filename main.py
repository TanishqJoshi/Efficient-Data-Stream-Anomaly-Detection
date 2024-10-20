import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import time

# Function to simulate a real-time data stream
def data_stream():
    """Simulate a continuous data stream with seasonal, trend, and noise components."""
    t = 0  # Time index
    while True:
        try:
            # Simulate seasonal pattern (sine wave), trend (linear increase), and noise (random variation)
            seasonal = 10 * np.sin(2 * np.pi * t / 50)
            trend = 0.05 * t
            noise = np.random.normal(0, 1)
            value = seasonal + trend + noise

            # Occasionally introduce anomalies with a 5% chance
            if random.random() < 0.05:
                value += random.choice([20, -20])  # Large positive or negative spike

            yield value  # Output the generated value
            t += 1
            time.sleep(0.1)  # Simulate real-time by pausing for 0.1 seconds between data points
        except Exception as e:
            print(f"Error in data generation: {e}")
            break

# Function to validate input parameters for anomaly detection
def validate_params(value, ewma, ewma_std, beta, threshold_multiplier):
    """Ensure parameters are within acceptable ranges for anomaly detection."""
    if not isinstance(value, (int, float)) or np.isnan(value) or np.isinf(value):
        raise ValueError(f"Invalid data value: {value}")
    if not (0 < beta < 1):
        raise ValueError(f"Invalid beta value: {beta}, must be between 0 and 1")
    if threshold_multiplier <= 0:
        raise ValueError(f"Threshold multiplier must be positive. Got {threshold_multiplier}.")
    if ewma_std < 0:
        raise ValueError(f"Invalid EWMA standard deviation: {ewma_std}, must be non-negative.")

# Function to detect anomalies in a data stream using Exponentially Weighted Moving Average (EWMA)
def anomaly_detection(value, ewma, ewma_std, beta=0.3, threshold_multiplier=2):
    """
    Detect anomalies in the data stream based on EWMA and its standard deviation.
    
    Parameters:
    value - Current data value
    ewma - Current EWMA of the data stream
    ewma_std - Current standard deviation of the EWMA
    beta - Smoothing factor for EWMA
    threshold_multiplier - Multiplier to determine the threshold for anomaly detection
    
    Returns:
    ewma_new - Updated EWMA
    ewma_std_new - Updated EWMA standard deviation
    is_anomaly - Boolean flag indicating whether an anomaly is detected
    """
    try:
        # Validate the parameters
        validate_params(value, ewma, ewma_std, beta, threshold_multiplier)

        # Update EWMA and EWMA standard deviation using exponential weighting
        ewma_new = beta * value + (1 - beta) * ewma
        variance_new = beta * (value - ewma_new) ** 2 + (1 - beta) * ewma_std ** 2
        ewma_std_new = np.sqrt(variance_new)

        # Calculate the anomaly detection threshold
        threshold = threshold_multiplier * ewma_std_new
        is_anomaly = abs(value - ewma_new) > threshold  # Flag if the deviation exceeds the threshold

        if is_anomaly:
            print(f"Anomaly detected at Time {time.time()}: Value = {value}, EWMA = {ewma_new}, Threshold = {threshold}")

        return ewma_new, ewma_std_new, is_anomaly
    except Exception as e:
        print(f"Error in anomaly detection: {e}")
        return ewma, ewma_std, False

# Main function to visualize real-time data with anomaly detection
def main():
    """
    Main function to simulate a real-time data stream and perform anomaly detection,
    visualizing the results in an animated plot.
    """
    data_gen = data_stream()  # Initialize the data stream generator
    ewma, ewma_std = 0, 1  # Initial values for EWMA and standard deviation
    times, values, anomalies = [], [], []  # Lists to store time, values, and anomalies

    fig, ax = plt.subplots()  # Create a matplotlib figure and axis for plotting
    line, = ax.plot([], [], lw=2, label='Data Stream')  # Line plot for data stream
    scat = ax.scatter([], [], color='red', label='Anomaly')  # Scatter plot for anomalies
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('Real-Time Data Stream with Anomaly Detection')
    ax.legend()
    plt.tight_layout()

    # Initialization function for the animation (sets up the plot limits)
    def init():
        ax.set_xlim(0, 100)
        ax.set_ylim(-30, 50)
        line.set_data(times, values)
        scat.set_offsets(np.empty((0, 2)))  # Empty scatter plot for anomalies
        return line, scat

    # Update function for the animation (called repeatedly during the animation)
    def update(frame):
        nonlocal ewma, ewma_std  # Use nonlocal to modify ewma and ewma_std in the main scope
        try:
            value = next(data_gen)  # Get the next value from the data stream
        except StopIteration:
            print("Data stream ended.")
            return line, scat
        except Exception as e:
            print(f"Error in fetching next data point: {e}")
            return line, scat

        # Perform anomaly detection on the new data point
        ewma, ewma_std, is_anomaly = anomaly_detection(value, ewma, ewma_std, beta=0.3, threshold_multiplier=1.5)

        # Update the time and value lists for the plot
        times.append(frame)
        values.append(value)
        if len(times) > 100:  # Keep only the last 100 data points in the plot
            times.pop(0)
            values.pop(0)
        line.set_data(times, values)

        # If an anomaly is detected, add it to the anomaly list and update the scatter plot
        if is_anomaly:
            anomalies.append((frame, value))
            if len(anomalies) > 100:
                anomalies.pop(0)
        if anomalies:
            x, y = zip(*anomalies)  # Unzip anomaly coordinates into x and y
            scat.set_offsets(np.c_[x, y])  # Update scatter plot with anomalies
        else:
            scat.set_offsets(np.empty((0, 2)))  # Clear the scatter plot if no anomalies

        # Adjust plot limits based on the latest data
        ax.set_xlim(max(0, frame - 100), frame + 10)
        ymin = min(values + [v for (_, v) in anomalies])
        ymax = max(values + [v for (_, v) in anomalies])
        ax.set_ylim(ymin - 5, ymax + 5)
        return line, scat

    # Create the animation using the update function
    ani = animation.FuncAnimation(fig, update, init_func=init, interval=100, cache_frame_data=False)

    # Display the plot
    try:
        plt.show()
    except KeyboardInterrupt:
        print("Plotting interrupted by user.")
    except Exception as e:
        print(f"Unexpected error during plotting: {e}")

# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()
