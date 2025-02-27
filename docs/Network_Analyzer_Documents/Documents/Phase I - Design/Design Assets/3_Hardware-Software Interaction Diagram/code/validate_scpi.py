import pyvisa
import csv
import time

# Define SCPI commands from Tektronix TDS 1002B Programmer Manual
scpi_commands = {
    "Identify Device": "*IDN?",
    "Query Horizontal Scale": "HORizontal:MAIn:SCAle?",
    "Query Vertical Scale CH1": "CH1:SCAle?",
    "Query Vertical Scale CH2": "CH2:SCAle?",
    "Query Acquisition Mode": "ACQuire:MODe?",
    "Query Waveform Data Format": "DATa:ENCdg?",
    "Query Waveform Data Source": "DATa:SOUrce?",
    "Query Waveform Data Start": "DATa:STARt?",
    "Query Waveform Data Stop": "DATa:STOP?",
}

# SCPI commands that require `.write()`
write_commands = {
    "Set Horizontal Scale": "HORizontal:MAIn:SCAle 5E-3",
    "Set CH1 Voltage Scale": "CH1:SCAle 1",
    "Set CH2 Voltage Scale": "CH2:SCAle 1",
    "Set Trigger Source": "TRIGger:A:SOUrce CH1",
    "Set Measurement Source": "MEASUrement:IMMed:SOUrce CH1"
}

# Measurement SCPI commands (assumed to work when signal is present in a later phase)
measurement_commands = {
    "Set Frequency Measurement": "MEASUrement:IMMed:TYPe FREQ",
    "Query Frequency Measurement": "MEASUrement:IMMed:VALue?",
    "Set Period Measurement": "MEASUrement:IMMed:TYPe PERIOD",
    "Query Period Measurement": "MEASUrement:IMMed:VALue?",
    "Set Peak-to-Peak Measurement": "MEASUrement:IMMed:TYPe PK2PK",
    "Query Peak-to-Peak Voltage": "MEASUrement:IMMed:VALue?",
    "Set RMS Measurement": "MEASUrement:IMMed:TYPe CRMS",
    "Query RMS Voltage": "MEASUrement:IMMed:VALue?"
}

# Connect to the oscilloscope
try:
    rm = pyvisa.ResourceManager('@py')
    oscilloscope = rm.open_resource('USB0::1689::867::C064444::0::INSTR')
    oscilloscope.timeout = 10000  # Set timeout to prevent hanging

    results = []

    print("Starting SCPI Command Validation...\n")

    # Test query-based SCPI commands
    for command_name, command in scpi_commands.items():
        try:
            print(f"Testing: {command_name} -> {command}")
            response = oscilloscope.query(command)
            results.append([command_name, command, "Success", response.strip()])
        except Exception as e:
            results.append([command_name, command, "Failed", str(e)])
            print(f"⚠️ Failed: {command} -> {e}")

        time.sleep(0.5)  # Small delay to avoid buffer overload

    # Test write-based SCPI commands
    for command_name, command in write_commands.items():
        try:
            print(f"Setting: {command_name} -> {command}")
            oscilloscope.write(command)
            results.append([command_name, command, "Success", "Write Command Executed"])
        except Exception as e:
            results.append([command_name, command, "Failed", str(e)])
            print(f"⚠️ Failed: {command} -> {e}")

        time.sleep(0.5)  # Small delay

    # ✅ Measurement Commands - Skipped for Now
    for command_name, command in measurement_commands.items():
        results.append([command_name, command, "Skipped", "Measurement testing will be done in a future phase."])
        print(f"Skipped: {command_name} -> Measurement testing will be done in a future phase.")

    # Save results to CSV
    with open("validated_scpi_commands.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Command Name", "SCPI Command", "Status", "Response/Error"])
        writer.writerows(results)

    print("\nSCPI Command Validation Completed. Results saved in 'validated_scpi_commands.csv'.")

except Exception as e:
    print(f"Connection Error: {e}")

finally:
    # Ensure the oscilloscope connection is closed properly
    oscilloscope.close()
    print("Connection closed.")
