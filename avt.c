#include <reg51.h>
#include <string.h> 

// --- LCD Control Pin Definitions (P3) ---
sbit rs = P3^2; // Register Select
sbit en = P3^3; // Enable
// LCD Data Bus is P2 (Standard 8-bit mode)

// --- Keypad I/O Pin Definitions (P1) ---
// Rows (Output) are P1.0 - P1.3
sbit r1 = P1^0;
sbit r2 = P1^1;
sbit r3 = P1^2;
sbit r4 = P1^3;
// Columns (Input) are P1.4 - P1.6
sbit c1 = P1^4;
sbit c2 = P1^5;
sbit c3 = P1^6;

// --- Function Prototypes ---
void delay();
void cmd (int);
void data1 (char);
void lcd_init(); // Renamed from lcd() for clarity
void display(char *s);
int key();
void disp(int);
void uart_init();
void uart_tx(char);
void uart_tx_string(char *s); // New function

int k; // Global variable to store the key value

// ====================================================================
// --- UTILITY FUNCTIONS ---
// ====================================================================

void delay() {
    int i,j;
    // Delay loop (approx. 1ms at 12MHz, though precise timing is less critical here)
    for(i=0;i<10;i++) 
        for(j=0;j<1200;j++);
}

// ====================================================================
// --- LCD DRIVER FUNCTIONS (8-bit Mode, P2 Data) ---
// ====================================================================

void cmd(int a) {
    P2 = a; // Send command byte to P2
    rs = 0; // Command Mode
    en = 1;
    delay();
    en = 0;
}

void data1(char j) {
    P2 = j; // Send data byte to P2
    rs = 1; // Data Mode
    en = 1;
    delay();
    en = 0;
}

void lcd_init() {
    delay(); // Initial power-on delay
    cmd(0x38); // 8-bit mode, 2 lines, 5x7 font
    cmd(0x0C); // Display ON, Cursor OFF, Blink OFF (Original was 0x0E: Cursor ON)
    cmd(0x01); // Clear Display
    cmd(0x06); // Entry Mode Set (Increment cursor)
    cmd(0x80); // Set cursor to start of line 1
}

void display(char *s){
    while(*s!='\0'){
        data1(*s);
        s++;
    }
}

// ====================================================================
// --- UART FUNCTIONS ---
// ====================================================================

void uart_init() {
    // TMOD: Timer 1, Mode 2 (8-bit auto-reload)
    TMOD = 0x20; 
    // TH1: 0xFD for 9600 Baud @ 11.0592MHz crystal
    TH1 = 0xFD; 
    // SCON: Mode 1 (8-bit UART), REN=0 (Transmit only)
    SCON = 0x50; 
    // TR1: Start Timer 1
    TR1 = 1; 
}

void uart_tx(char c) {
    SBUF = c;
    while(TI == 0); // Wait for transmission to complete
    TI = 0;         // Clear the flag for the next byte
}

void uart_tx_string(char *s) {
    while (*s != '\0') {
        uart_tx(*s);
        s++;
    }
}

// ====================================================================
// --- KEYPAD SCAN FUNCTION ---
// Maps key presses to integers: 1-9, 0, 10 (*), 11 (#)
// ====================================================================

int key() {
    int x = 12; // Default: No key pressed (return value 12)

    // Row 1 (r1=0)
    P1 = 0xFF; // Set all P1 HIGH
    r1 = 0;
    if(c1==0){ x=1; while(c1==0); return x; } // Key '1'
    if(c2==0){ x=2; while(c2==0); return x; } // Key '2'
    if(c3==0){ x=3; while(c3==0); return x; } // Key '3'

    // Row 2 (r2=0)
    P1 = 0xFF; 
    r2 = 0;
    if(c1==0){ x=4; while(c1==0); return x; } // Key '4'
    if(c2==0){ x=5; while(c2==0); return x; } // Key '5'
    if(c3==0){ x=6; while(c3==0); return x; } // Key '6'

    // Row 3 (r3=0)
    P1 = 0xFF; 
    r3 = 0;
    if(c1==0){ x=7; while(c1==0); return x; } // Key '7'
    if(c2==0){ x=8; while(c2==0); return x; } // Key '8'
    if(c3==0){ x=9; while(c3==0); return x; } // Key '9'

    // Row 4 (r4=0)
    P1 = 0xFF; 
    r4 = 0;
    if(c1==0){ x=10; while(c1==0); return x; } // Key '*'
    if(c2==0){ x=0;  while(c2==0); return x; } // Key '0'
    if(c3==0){ x=11; while(c3==0); return x; } // Key '#'

    return x; // Returns 12 if no key is pressed
}

// ====================================================================
// --- KEY ACTION/DISPLAY FUNCTION ---
// ====================================================================

void disp(int x) {
    cmd(0x01); // Clear screen
    cmd(0x80); // Line 1
    
    switch(x){
        case 1: 
            display("CATARACT TEST");
            cmd(0xC0); display("Loading...");
            uart_tx_string("CMD:CATARACT\n");
            break;
        case 2: 
            display("GLARE TEST");
            cmd(0xC0); display("Loading...");
            uart_tx_string("CMD:GLARE\n");
            break;
        case 3: 
            display("LOW CONTRAST");
            cmd(0xC0); display("Loading...");
            uart_tx_string("CMD:LOWCONTRAST\n");
            break;
        case 10: // Key '*'
            display("MENU SELECTED");
            cmd(0xC0); display("Press 1, 2, or 3");
            uart_tx_string("CMD:MENU\n");
            break;
        case 11: // Key '#' - Used as Exit/Back
            display("EXIT/RESTART");
            cmd(0xC0); display("KIOSK WELCOMES");
            uart_tx_string("CMD:RESTART\n");
            break;
        default:
            display("Input: "); // Default feedback for 0, 4-9
            // Convert integer to ASCII char before display/transmission
            data1(x + '0'); 
            cmd(0xC0); 
            display("Error/Debug key.");
            // Send the raw key value for debugging
            uart_tx_string("DBG:");
            uart_tx(x + '0');
            uart_tx('\n');
    }
}

// ====================================================================
// --- MAIN PROGRAM ---
// ====================================================================

void main() {
    
    lcd_init();
    uart_init();

    display("KIOSK WELCOMES");
    cmd(0xC0);
    display("TEST YOUR EYE");

    while(1){
        int new_key = 12; // 12 means no key pressed
        
        // ?? BLOCKING LOOP: Waits for a key press (new_key != 12) ??
        do {
            new_key = key(); 
        } while(new_key == 12); 
        
        // Key found! Execute the action once.
        disp(new_key);
    }
}