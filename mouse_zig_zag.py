import pyautogui
import threading
import time
import keyboard
import tkinter as tk

# Flag to control the mouse movement loop
running = False
start_time = None

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False


def mouse_movement_thread():
    global running, start_time
    start_time = time.time()
    for y in range(1000):
        for x in range(1000):
            if not running:
                break

            pyautogui.moveTo(x, y)
            print("X: {0}, Y: {1}\n".format(x, y))


def start_program():
    global running, mouse_thread
    if not running:
        running = True
        mouse_thread = threading.Thread(target=mouse_movement_thread)
        mouse_thread.start()
        update_elapsed_time()


def stop_program():
    global running, mouse_thread
    running = False
    if mouse_thread and mouse_thread.is_alive():
        mouse_thread.join()


def update_elapsed_time():
    global start_time, running
    if running:
        elapsed_time = time.time() - start_time
        time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        time_label.config(text=f"Elapsed Time: {time_str}")
        root.after(1000, update_elapsed_time)  # Update time label every second


def on_key_press(event):
    global running
    if str(event.name).lower() == 'q':
        print("Detected 'q' key press. Stopping mouse movement...")
        stop_program()


# Setup tkinter GUI
root = tk.Tk()
root.title("Mouse Movement Program")

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
