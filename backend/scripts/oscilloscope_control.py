import sys
import json
import pyvisa

# Initialize PyVISA resource manager
rm = pyvisa.ResourceManager()

try:
    # Open communication with the oscilloscope
    oscilloscope = rm.open_resource("USB0::0x0699::0x0368::C000000::INSTR")
    oscilloscope.timeout = 5000  # Set timeout to avoid hanging requests

except Exception as e:
    print(json.dumps({"error": "Could not connect to oscilloscope", "details": str(e)}))
    sys.exit(1)

def send_test_signal(frequency, waveform):
    """Sends a test signal command to the oscilloscope."""
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
        return {
            "timestamp": sys.argv[2] if len(sys.argv) > 2 else "N/A",
            "amplitude": float(amplitude.strip()),
            "phase": float(phase.strip())
        }
    except Exception as e:
        return {"error": "Failed to retrieve measurements", "details": str(e)}

# Handle command-line arguments from Node.js
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
