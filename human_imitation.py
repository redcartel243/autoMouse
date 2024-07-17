import pyautogui
import threading
import time
import keyboard
import tkinter as tk
import random
import ctypes

# Flag to control the mouse movement loop
running = False
start_time = None
mouse_thread = None

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Prevent Windows from sleeping
def prevent_sleep():
    ctypes.windll.kernel32.SetThreadExecutionState(
        ctypes.windll.kernel32.ES_CONTINUOUS | ctypes.windll.kernel32.ES_SYSTEM_REQUIRED
    )

def simulate_mouse_movement():
    width, height = pyautogui.size()
    while running:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.3))
        time.sleep(random.uniform(0.5, 2))
        print(f"Moved to X: {x}, Y: {y}")

def simulate_keyboard_activity():
    while running:
        pyautogui.press(random.choice(['shift', 'ctrl', 'alt']))
        time.sleep(random.uniform(10, 30))

def start_program():
    global running, mouse_thread, keyboard_thread
    if not running:
        running = True
        mouse_thread = threading.Thread(target=simulate_mouse_movement)
        keyboard_thread = threading.Thread(target=simulate_keyboard_activity)
        mouse_thread.start()
        keyboard_thread.start()
        update_elapsed_time()
        prevent_sleep()

def stop_program():
    global running, mouse_thread, keyboard_thread
    running = False
    if mouse_thread and mouse_thread.is_alive():
        mouse_thread.join()
    if keyboard_thread and keyboard_thread.is_alive():
        keyboard_thread.join()

def update_elapsed_time():
    global start_time, running
    if running:
        elapsed_time = time.time() - start_time
        time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        time_label.config(text=f"Elapsed Time: {time_str}")
        root.after(1000, update_elapsed_time)  # Update time label every second

def on_key_press(event):
    if str(event.name).lower() == 'q':
        print("Detected 'q' key press. Stopping mouse movement...")
        stop_program()

# Setup tkinter GUI
root = tk.Tk()
root.title("Mouse")

start_button = tk.Button(root, text="Start", fg="green", command=start_program)
start_button.pack(pady=10)

stop_button = tk.Label(root, text="Press Q to stop", fg="red")
stop_button.pack(pady=10)

time_label = tk.Label(root, text="Elapsed Time: 00:00:00")
time_label.pack(pady=10)

# Register the 'q' key press event listener
keyboard.on_press_key('q', on_key_press)

# Main loop for tkinter application
root.mainloop()

# Clean up on exit
stop_program()
print("Program exited.")
