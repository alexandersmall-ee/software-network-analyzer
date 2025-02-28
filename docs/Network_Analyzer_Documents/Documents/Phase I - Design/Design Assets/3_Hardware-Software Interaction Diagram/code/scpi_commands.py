import pyvisa

try:
    # Connect to the oscilloscope
    rm = pyvisa.ResourceManager('@py')
    oscilloscope = rm.open_resource('USB0::1689::867::C064444::0::INSTR')
    oscilloscope.timeout = 10000  # Set timeout to 10 seconds

    # Identify the oscilloscope
    print("Oscilloscope ID:", oscilloscope.query("*IDN?"))

    # Query the horizontal scale (timebase)
    print("Current Timebase:", oscilloscope.query("HORizontal:MAIn:SCAle?"))

    # Query the vertical scale for Channel 1
    print("Current CH1 Voltage Scale:", oscilloscope.query("CH1:SCAle?"))

    # Set timebase to 5ms/div
    oscilloscope.write("HORizontal:MAIn:SCAle 5E-3")

    # Set CH1 voltage scale to 1V/div
    oscilloscope.write("CH1:SCAle 1")

    # Confirm changes
    print("Updated Timebase:", oscilloscope.query("HORizontal:MAIn:SCAle?"))
    print("Updated CH1 Voltage Scale:", oscilloscope.query("CH1:SCAle?"))

except Exception as e:
    print("Error:", e)

finally:
    # Ensure the oscilloscope connection is closed properly
    oscilloscope.close()
    print("Connection closed.")
