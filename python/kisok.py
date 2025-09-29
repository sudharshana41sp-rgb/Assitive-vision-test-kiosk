import serial
import time
import sys

# --- CONFIGURATION ---
# IMPORTANT: This port MUST be the paired port not used by Proteus (e.g., COM11 if Proteus uses COM10)
SERIAL_PORT = 'COM11'
BAUD_RATE = 9600

# --- VISUAL TEST FUNCTIONS (PLACEHOLDERS) ---
# Replace the print statements with your actual GUI/Pygame code
def load_cataract_test():
    """Triggers the Cataract Test UI."""
    print("✅ COMMAND EXECUTED: Launching CATARACT Test UI...")
    time.sleep(0.1) 

def load_glare_test():
    """Triggers the Glare Test UI."""
    print("✅ COMMAND EXECUTED: Launching GLARE Test UI...")
    time.sleep(0.1) 

def load_low_contrast_test():
    """Triggers the Low Contrast Visual Acuity Test UI."""
    print("✅ COMMAND EXECUTED: Launching LOW CONTRAST Test UI...")
    time.sleep(0.1) 

# --- SERIAL COMMUNICATION HANDLER ---
def serial_listener():
    """Initializes the serial connection and listens for commands."""
    try:
        # Open the virtual serial port
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=1
        )
        print(f"--- Python Listener Active on {SERIAL_PORT} @ {BAUD_RATE} bps ---")
        print("Waiting for commands from 8051 Kiosk (Press Ctrl+C to stop)...\n")
        
        while True:
            # Check if there is data available in the buffer
            if ser.in_waiting > 0:
                # Read data until newline (\n), decode from bytes, and strip whitespace
                command_bytes = ser.readline()
                command = command_bytes.decode('utf-8').strip()
                
                # Command Parsing Logic (Matches strings sent by the 8051 C code)
                if command == "CMD:CATARACT":
                    load_cataract_test()
                    
                elif command == "CMD:GLARE":
                    load_glare_test()
                    
                elif command == "CMD:LOWCONTRAST":
                    load_low_contrast_test()
                
                # Handle other commands for user feedback
                elif command == "CMD:MENU":
                    print("SYSTEM: Kiosk initialized, main menu displayed.")
                elif command == "CMD:SHUTDOWN":
                    print("SYSTEM: Kiosk shutting down. End communication.")
                    # Optionally break the loop here
                elif command:
                    print(f"INFO: Debug message received: {command}")
            
            time.sleep(0.01) # Small delay to reduce CPU usage
            
    except serial.SerialException as e:
        print(f"\n❌ FATAL ERROR: Could not open port {SERIAL_PORT}.")
        print("   Ensure VSPE is running, COM10 is used by Proteus, and COM11 is the correct port.")
        print(f"   Details: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nListener stopped by user (KeyboardInterrupt).")
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"Connection on {SERIAL_PORT} closed.")

if __name__ == "__main__":
    serial_listener()
