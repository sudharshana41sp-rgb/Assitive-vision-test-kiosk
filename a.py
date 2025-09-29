import serial
import time
import sys
import pygame
import random

# --- CONFIGURATION ---
# IMPORTANT: Use the port paired with the one Proteus is using (e.g., COM21 if Proteus uses COM20)
SERIAL_PORT = 'COM21'
BAUD_RATE = 9600

# --- PYGAME CONSTANTS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_LOW_CONTRAST = (200, 200, 200) # For Low Contrast Test (about 20% contrast)
GLARE_COLOR = (255, 255, 250)      # Slightly off-white for Glare Test background

# --- TEST UTILITY FUNCTIONS ---

def draw_optotype(screen, color, text_size, direction):
    """Draws the optotype ('E') at the center in the specified size and direction."""
    
    # 1. Rotate the 'E' based on direction
    # Directions: 0-Right, 90-Up, 180-Left, 270-Down (Standard Pygame rotation)
    
    # Text rendering (Pygame standard)
    font = pygame.font.Font(None, int(text_size))
    text_surface = font.render("E", True, color)
    
    if direction == 'UP':
        angle = 90
    elif direction == 'DOWN':
        angle = 270
    elif direction == 'LEFT':
        angle = 180
    else: # Default or 'RIGHT'
        angle = 0
        
    rotated_surface = pygame.transform.rotate(text_surface, angle)

    # 2. Position the optotype in the center
    rect = rotated_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.blit(rotated_surface, rect)

    # ... (after draw_optotype and run_test_loop functions) ...

def get_acuity_remark(score_line):
    """Provides a user-friendly remark based on the Snellen denominator."""
    try:
        # Extract the denominator (e.g., 40 from "20/40")
        denominator = int(score_line.split('/')[1])
    except:
        # Handle cases like "Test Not Completed"
        return "Test was incomplete or results were inconclusive."
    
    if denominator <= 20:
        return "Vision is Excellent! Your acuity is better than average."
    elif denominator <= 30:
        return "Vision is Good. Your acuity is within the normal range."
    elif denominator <= 50:
        return "Vision is Fair. You may need a professional consultation."
    else: # denominator > 50 (e.g., 20/60, 20/100)
        return "Vision is Poor. Immediate consultation with an eye care specialist is recommended."

# ... (before the Visual Test Functions) ...


def run_test_loop(screen, test_type, optotype_color, background_color):
    """Generic loop for all acuity-based tests (Cataract, Low Contrast)."""
    
    test_running = True
    current_size = 250
    score_line = "20/200"
    
    DIRECTIONS = ['RIGHT', 'LEFT', 'UP', 'DOWN']
    current_direction = random.choice(DIRECTIONS)
    
    # Text font for test instructions
    instruction_font = pygame.font.Font(None, 30)

    while test_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                test_running = False
            
            if event.type == pygame.KEYDOWN:
                key_pressed = None
                
                # Check directional input (User's answer)
                if event.key == pygame.K_RIGHT: key_pressed = 'RIGHT'
                elif event.key == pygame.K_LEFT: key_pressed = 'LEFT'
                elif event.key == pygame.K_UP: key_pressed = 'UP'
                elif event.key == pygame.K_DOWN: key_pressed = 'DOWN'
                
                # Stop/End Key
                elif event.key == pygame.K_ESCAPE:
                    test_running = False
                    
                
                if key_pressed:
                    if key_pressed == current_direction:
                        # Correct Answer: Decrease size, update score, new direction
                        current_size *= 0.8
                        score_line = f"20/{int(200 * (current_size / 250) * 4)}" # Simple score approximation
                        print(f"Correct! New Size: {int(current_size)}. Score: {score_line}")
                        current_direction = random.choice(DIRECTIONS)
                    else:
                        # Incorrect Answer: End test
                        print(f"Incorrect. Final Score: {score_line}")
                        test_running = False

                
        # --- DRAWING ---
        screen.fill(background_color)
        
        # Draw Instructions
        instructions = instruction_font.render(f"Direction: {current_direction}. Press ESC to quit.", True, BLACK)
        screen.blit(instructions, (10, 10))

        # Draw Optotype
        draw_optotype(screen, optotype_color, current_size, current_direction)
        
        pygame.display.flip()
        
    # 1. Get the final remark
    final_remark = get_acuity_remark(score_line)
    
    # 2. Print the final score and the remark for the Kiosk attendant/log
    print(f"TEST SCORE: {score_line}")
    print(f"TEST REMARK: {final_remark}")

    # 3. Return the score
    return score_line


# ====================================================================
# --- VISUAL TEST FUNCTIONS (Called by Serial Listener) ---
# ====================================================================

def load_cataract_test():
    """Triggers the Cataract Test UI (Standard black on white, acuity change)."""
    print("\n✅ COMMAND EXECUTED: Launching CATARACT Test UI...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CATARACT TEST (Standard Acuity)")
    
    final_score = run_test_loop(screen, "CATARACT", BLACK, WHITE)
    
    pygame.quit()
    print(f"CATARACT TEST COMPLETE. Final Score Logged: {final_score}")

def load_glare_test():
    """Triggers the Glare Test UI (Standard optotype on high-brightness/glare background)."""
    print("\n✅ COMMAND EXECUTED: Launching GLARE Test UI...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GLARE TEST (High Contrast / Glare)")
    
    # Glare test uses the same acuity logic but with a slightly off-white, high-intensity background
    final_score = run_test_loop(screen, "GLARE", BLACK, GLARE_COLOR) 
    
    pygame.quit()
    print(f"GLARE TEST COMPLETE. Final Score Logged: {final_score}")

def load_low_contrast_test():
    """Triggers the Low Contrast Visual Acuity Test UI (Low contrast optotype)."""
    print("\n✅ COMMAND EXECUTED: Launching LOW CONTRAST Test UI...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("LOW CONTRAST VISUAL TEST")
    
    # Low contrast uses a light gray optotype on a white background
    final_score = run_test_loop(screen, "LOW CONTRAST", GRAY_LOW_CONTRAST, WHITE)
    
    pygame.quit()
    print(f"LOW CONTRAST TEST COMPLETE. Final Score Logged: {final_score}")

def default_action(command):
    """Handles unexpected or non-critical commands."""
    if command:
        print(f"INFO: Menu/Debug command received: {command}")


# ====================================================================
# --- SERIAL COMMUNICATION HANDLER (UNCHANGED) ---
# ====================================================================

def serial_listener():
    """Initializes the serial connection and listens for commands in a loop."""
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
            # Check for incoming commands from the 8051
            if ser.in_waiting > 0:
                command = ser.readline().decode('utf-8').strip()
                
                # Command Parsing Logic
                if command == "CMD:CATARACT":
                    load_cataract_test()
                    
                elif command == "CMD:GLARE":
                    load_glare_test()
                    
                elif command == "CMD:LOWCONTRAST":
                    load_low_contrast_test()
                
                elif command:
                    default_action(command)
            
            time.sleep(0.01) # Small sleep to reduce CPU usage
            
    except serial.SerialException as e:
        print(f"\n❌ FATAL ERROR: Could not open port {SERIAL_PORT}.")
        print(f"   Details: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nListener stopped by user (KeyboardInterrupt).")
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(f"Connection on {SERIAL_PORT} closed.")

if __name__ == "__main__":
    # Ensure Pygame is NOT initialized here, only inside the test functions
    serial_listener()
