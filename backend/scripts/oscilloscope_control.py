import sys
import json
import os
import pyvisa
from datetime import datetime, timezone

# file path for local measurement logs
LOG_FILE = "backend/data/measurements.json"

# initialize PyVISA resource manager
rm = pyvisa.ResourceManager()

try:
    # using usb id, open communication with the oscilloscope
    oscilloscope = rm.open_resource("USB0::0x0699::0x0368::C000000::INSTR")
    oscilloscope.timeout = 5000  # set timeout to avoid hanging requests

except Exception as e:
    # connection error and 
    print(json.dumps({"error": "Could not connect to oscilloscope", "details": str(e)}))
    sys.exit(1)

def save_measurement_log(data):
    """Saves oscilloscope measurement data to a JSON log file."""
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        # Read existing logs if file exists
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        # Append new measurement entry
        logs.append(data)

        # Write updated logs back to file
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    except Exception as e:
        print(json.dumps({"error": "Failed to log measurement", "details": str(e)}))

def send_test_signal(frequency, waveform):
    """
    Function that sends a test signal command to the oscilloscope.
    - Uses SCPI commands to configure the signal generator.
    - Accepts frequency and waveform type as parameters for flexibility.
    - Outputs a JSON confirmation message.    
    """
    try:
        oscilloscope.write(f"APPL:{waveform} {frequency}Hz, 3VPP")
        return {"status": "success", "message": f"Test signal {waveform} at {frequency}Hz sent."}
    except Exception as e:
        return {"error": "Failed to send test signal", "details": str(e)}

def get_measurements():
    """Retrieves amplitude and phase measurements from the oscilloscope."""
    try:
        amplitude = oscilloscope.query("MEASure:VPP?")
        phase = oscilloscope.query("MEASure:PHASe?")

        # Create structured measurement data
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "frequency": sys.argv[2] if len(sys.argv) > 2 else "N/A",
            "amplitude": float(amplitude),
            "phase": float(phase)
        }

        save_measurement_log(data)  # Persist measurement

        return data
    except Exception as e:
        return {"error": "Failed to retrieve measurements", "details": str(e)}

# handle command-line arguments from API
if len(sys.argv) > 1:
    command = sys.argv[1]

    if command == "test-signal" and len(sys.argv) >= 4:
        frequency = sys.argv[2]
        waveform = sys.argv[3]
        result = send_test_signal(frequency, waveform)
        print(json.dumps(result))

    elif command == "get-measurements":
        result = get_measurements()
        print(json.dumps(result))

    else:
        print(json.dumps({"error": "Invalid arguments"}))

sys.exit(0)
