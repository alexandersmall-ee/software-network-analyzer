import pyvisa

# Explicitly use PyVISA-Py backend
rm = pyvisa.ResourceManager('@py')

# List available instruments
resources = rm.list_resources()
print("Available Instruments:", resources)

# Check if an oscilloscope is detected
if resources:
    oscilloscope = rm.open_resource(resources[0])  # Automatically connect to first device
    oscilloscope.timeout = 5000  # Set timeout to 5 seconds
    print("Connected to:", oscilloscope.query("*IDN?"))
else:
    print("No instruments detected.")
