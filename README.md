# load-resistance-monitoring
Monitor load health based on calculated resistance 

## Driving the load
The load is driven at different levels, and the load resistance is measured and compared to nominal values as an indicator of load health. 
To drive the load, either a current source or voltage source can be used. 

In the provided example, a DC power supply is operated in constant-current mode. Since the power supply does not have a programming interface, the current is adjusted manually, and the voltage drops across the current sense resistor and load resistor are measured using a Raspberry Pi 4 and an ADS1115 16-bit ADC. 

## Calculating electrical current
Current is calculated by Ohm's Law using the measured voltage drop across the current sense resistor and the nominal resistance of that resistor. Unlike the load resistor, the current sense resistor is being operated at well below its max power rating (2W), so it is much more reliable for measuring current.

## Data collection
Using the script `src/monitor_adc.py` on the Raspberry Pi 4, the current sense voltage and load voltage are measured continuously while the current drive is manually increased on the DC power supply. The results are saved to a CSV file. In this example, this experiment is repeated for multiple 10-Ohm resistors.

I2C must be enabled on the Raspberry Pi in order for this script to work. 

## Post-processing
Once voltage and current are measured for multiple resistors, a separate script `src/plot_resistor_data.ipynb` is used to post-process and plot the data from multiple CSV files. Post-processing includes the following steps:

- Read all CSV files into separate DataFrame objects.
- Remove all rows after the first negative current value, which is an erroneous value that shows up when the ADC input voltage exceeds the max level supported by the ADC.
- Calculate nominal load voltage, load resistance, and power dissipation at the load. Add these as new columns to the DataFrame.

The same script supports plotting the data with non-normalized or normalized axes.

![Non-normalized plot](images/unnormalized_plot.png)

![Normalized plot](images/normalized_plot.png)

## Next steps
- Add figures to show hardware setup
