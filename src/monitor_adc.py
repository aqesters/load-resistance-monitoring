import time
import csv
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        raise Exception("Provide output filename by running \"python monitor_adc.py [filename]\"")
        
    # Inputs
    curr_sense_resistance = 0.1  # Ohms

    # Initialize I2C bus and ADC
    i2c = board.I2C()
    ads = ADS1115(i2c)

    # Select the channel (e.g., channel 0)
    source_channel = AnalogIn(ads, ads1x15.Pin.A1)
    load_channel = AnalogIn(ads, ads1x15.Pin.A0)
    curr_sense_channel = AnalogIn(ads, ads1x15.Pin.A0, ads1x15.Pin.A1)

    # Calibration factors (determined empirically)
    gain = 1.44 / 1.427
    offset = -1 * (10/1000 * curr_sense_resistance) / gain   # 10 mA offset * current sense resistance

    # Time interval between readings (in seconds)
    time_interval = 0.2

    # Open CSV file and write header
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Source voltage (V)", "Load voltage (V)", "Curr sense voltage (V)", "Current (mA)"])

        # Record the start time
        start_time = time.time()

        # Main loop
        try:
            while True:
                # Read voltage from the selected channel
                source_voltage = (source_channel.voltage - offset) * gain
                load_voltage = (load_channel.voltage - offset) * gain
                curr_sense_voltage = -1 * (curr_sense_channel.voltage - offset) * gain
                current = curr_sense_voltage / curr_sense_resistance * 1000

                # Calculate the elapsed time since the start
                elapsed_time = time.time() - start_time

                # Write the data to the CSV file
                writer.writerow([elapsed_time, source_voltage, load_voltage, curr_sense_voltage, current])
                print(f"{elapsed_time:>.2f} s\tLoad voltage: {load_voltage:>.3f} V\tCurrent: {current:>.1f} mA")

                # Wait for the specified time interval
                time.sleep(time_interval)
                
        except KeyboardInterrupt:
            print("Monitoring stopped.")
