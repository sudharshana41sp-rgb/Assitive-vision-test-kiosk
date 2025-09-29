# Assitive-vision-test-kiosk
Assistive Keystroke Vision Test (8051 + Python + PyGame)

This project demonstrates how embedded systems can be used in healthcare applications, specifically for vision testing. It integrates an 8051 microcontroller simulation with Python applications to provide virtual eye tests like cataract, glare, and low-contrast vision checks.

🔄 Working Principle

User Interaction

A 4x3 Keypad is connected to the 8051.

Pressing keys:

1 → Cataract Test

2 → Glare Test

3 → Low Contrast Test

LCD Feedback

The 16x2 LCD shows a “loading” message while the test is being prepared.

Serial Communication

The 8051 is connected to a virtual COM port in Proteus.

Using UART (TX/RX), the microcontroller sends the test selection to the PC.

Python Application (PySerial + PyGame)

PySerial listens to the COM port.

Based on the key pressed, PyGame displays the correct vision test chart.

Result Output

After test completion, the system evaluates performance.

Displays Snellen ratio + remark about vision quality.

🛠️ Components & Tools

AT89C51 Microcontroller (8051)

4x3 Matrix Keypad

16x2 LCD Display

Proteus (simulation + virtual COM port)

Embedded C for 8051

Python (PySerial, PyGame)

✨ Features

Embedded system integration with software application

Fully simulated in Proteus (no physical hardware required)

Real-time communication via virtual COM port

Healthcare application for vision testing

Outputs test results in standard Snellen format

🚀 Skills Gained

Microcontroller programming (8051, Embedded C)

Peripheral interfacing (Keypad, LCD)

Serial communication (UART)

Python programming with PySerial and PyGame

System-level integration (Hardware + Software)

Healthcare-focused embedded application design

✨ With this project, I showcased how embedded systems + Python applications can be used in real-world medical assistive technology.
