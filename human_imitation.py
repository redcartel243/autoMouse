import pyautogui
import threading
import time
import keyboard
import tkinter as tk
import random
import ctypes
import win32con
import win32gui
import atexit
import win32api

# Flag to control the mouse movement loop
running = False
start_time = None
mouse_thread = None
keyboard_thread = None

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Prevent Windows from sleeping
def prevent_sleep():
    win32api.SetThreadExecutionState(
        win32con.ES_CONTINUOUS | win32con.ES_SYSTEM_REQUIRED
    )

# Save the system cursor before changing it
def save_current_cursor():
    cursor = win32gui.LoadImage(0, 32512, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_SHARED)
    save_system_cursor = ctypes.windll.user32.CopyImage(cursor, win32con.IMAGE_CURSOR, 0, 0, win32con.LR_COPYFROMRESOURCE)
    return save_system_cursor

saved_cursor = save_current_cursor()

def restore_cursor():
    # Restore the old cursor
    print("Restoring cursor")
    ctypes.windll.user32.SetSystemCursor(saved_cursor, 32512)
    ctypes.windll.user32.DestroyCursor(saved_cursor)

# Make sure cursor is restored at the end
atexit.register(restore_cursor)

# Load a custom cursor
def load_custom_cursor():
    custom_cursor = win32gui.LoadImage(0, "mouse.cur", win32con.IMAGE_CURSOR, 0, 0, win32con.LR_LOADFROMFILE)
    if custom_cursor:
        ctypes.windll.user32.SetSystemCursor(custom_cursor, 32512)
    else:
        print("Failed to load custom cursor")

# Reset to the default cursor
def reset_cursor():
    restore_cursor()

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
    global running, mouse_thread, keyboard_thread, start_time
    if not running:
        running = True
        start_time = time.time()
        mouse_thread = threading.Thread(target=simulate_mouse_movement)
        keyboard_thread = threading.Thread(target=simulate_keyboard_activity)
        mouse_thread.start()
        keyboard_thread.start()
        update_elapsed_time()
        #prevent_sleep()
        load_custom_cursor()

def stop_program():
    global running, mouse_thread, keyboard_thread
    running = False
    if mouse_thread and mouse_thread.is_alive():
        mouse_thread.join()
    if keyboard_thread and keyboard_thread.is_alive():
        keyboard_thread.join()
    reset_cursor()

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
