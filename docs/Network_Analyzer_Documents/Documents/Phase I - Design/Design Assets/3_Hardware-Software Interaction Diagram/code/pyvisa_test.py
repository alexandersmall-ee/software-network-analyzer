import pyvisa

def test_pyvisa_connection():
    try:
        print("Checking PyVISA installation and listing available instruments...")

        # Initialize the resource manager
        rm = pyvisa.ResourceManager('@py')

        # List all connected VISA-compatible instruments
        instruments = rm.list_resources()

        if not instruments:
            print("No VISA-compatible instruments found.")
            return

        print(f"Found instruments: {instruments}")

        # Attempt to connect to the oscilloscope
        oscilloscope_address = None
        for instrument in instruments:
            if "USB" in instrument:  # Looking for a USB-connected oscilloscope
                oscilloscope_address = instrument
                break

        if not oscilloscope_address:
            print("No USB oscilloscope found. Ensure the device is connected.")
            return

        print(f"Connecting to oscilloscope at {oscilloscope_address}...")

        # Open connection to oscilloscope
        oscilloscope = rm.open_resource(oscilloscope_address)
        oscilloscope.timeout = 5000  # 5-second timeout to prevent hanging

        # Send an SCPI command to confirm communication
        print("Sending *IDN? command to identify the oscilloscope...")
        oscilloscope_id = oscilloscope.query("*IDN?").strip()

        print(f"Connected to: {oscilloscope_id}")

        # Close the connection
        oscilloscope.close()
        print("Connection closed successfully.")

    except Exception as e:
        print(f"PyVISA Test Failed: {e}")

if __name__ == "__main__":
    test_pyvisa_connection()
