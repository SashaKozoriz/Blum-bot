import os
import sys
import cv2
import numpy as np
import time
from mss import mss
import pyautogui
import pygetwindow as gw
import keyboard
from math import sqrt
from concurrent.futures import ThreadPoolExecutor, as_completed

pyautogui.PAUSE = 0

def get_window_region(window):
    """Returns the region of the entire window."""
    return {
        "top": window.top,
        "left": window.left,
        "width": window.width,
        "height": window.height
    }

def distance(p1, p2):
    """Calculates the Euclidean distance between two points."""
    if not isinstance(p1, tuple) or not isinstance(p2, tuple):
        return float('inf')
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def find_objects(frame, template, threshold=0.8):
    """Finds objects in the frame matching the template."""
    result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return list(zip(*locations[::-1]))

def find_object_task(frame, template, name):
    """Wrapper function to find objects and return their names."""
    objects = find_objects(frame, template)
    return name, objects

def get_base_path():
    """Returns the base path for the script or executable."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def main():
    """Main function to control the automation script."""
    while True:
        try:
            target_window = gw.getWindowsWithTitle('TelegramDesktop')[0]
            monitor = get_window_region(target_window)

            base_path = get_base_path()

            # Load templates outside of the main loop
            templates = {
                'play_button': cv2.imread(os.path.join(base_path, 'play_button.png'), 0),
                'close_button': cv2.imread(os.path.join(base_path, 'close_button.png'), 0),
                'ice_cube': cv2.imread(os.path.join(base_path, 'ice_cube.png'), 0),
                'green_object': cv2.imread(os.path.join(base_path, 'green_object.png'), 0)
            }

            if any(template is None for template in templates.values()):
                print("Failed to load templates. Please ensure all template files exist.")
                return

            print("Script is running. Press 'q' to stop.")
            
            last_click = None
            button_timers = {'play_button': 0, 'close_button': 0}
            button_found_time = {'play_button': 0, 'close_button': 0}
            object_positions = {}
            
            with mss() as sct:
                with ThreadPoolExecutor(max_workers=4) as executor:
                    while not keyboard.is_pressed('q'):
                        screenshot = np.array(sct.grab(monitor))
                        frame = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2BGR)
                        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        
                        futures = [executor.submit(find_object_task, gray_frame, template, name) for name, template in templates.items()]
                        
                        for future in as_completed(futures):
                            name, objects = future.result()
                            if objects:
                                object_positions[name] = objects
                        
                        current_time = time.time()
                        
                        for button in ['play_button', 'close_button']:
                            if button in object_positions:
                                if button_found_time[button] == 0:
                                    button_found_time[button] = current_time
                                    print(f"{button.capitalize()} found. Waiting 5 seconds before clicking.")
                                elif current_time - button_found_time[button] >= 5:
                                    obj = object_positions[button][0]
                                    click_position(button, obj, monitor["left"], monitor["top"], templates)
                                    button_timers[button] = current_time
                                    button_found_time[button] = 0
                                    del object_positions[button]
                            else:
                                button_found_time[button] = 0
                        
                        handle_special_cases(object_positions, last_click, monitor["left"], monitor["top"], templates)
                        
                        time.sleep(0.01)
            
            print("Script stopped.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        user_input = input("Press 'r' to restart the script, or any other key to exit: ")
        if user_input.lower() != 'r':
            break

def click_position(button, obj, left, top, templates):
    """Handles the calculation and execution of clicks based on button type."""
    click_x = left + obj[0] + templates[button].shape[1] // 2
    click_y = top + obj[1] + templates[button].shape[0] // 2
    pyautogui.click(click_x, click_y)
    print(f"Clicked {button} at: ({click_x}, {click_y})")

def handle_special_cases(object_positions, last_click, left, top, templates):
    """Handles special cases like ice cube and green object interactions."""
    if 'ice_cube' in object_positions:
        obj = object_positions['ice_cube'][0]
        click_position('ice_cube', obj, left, top, templates)
        last_click = obj
        del object_positions['ice_cube']
    
    if 'green_object' in object_positions:
        green_objects = object_positions['green_object']
        if last_click and green_objects:
            obj = min(green_objects, key=lambda o: distance(o, last_click))
        elif green_objects:
            obj = green_objects[0]
        else:
            return
        
        click_position('green_object', obj, left, top, templates)
        last_click = obj
        del object_positions['green_object']

if __name__ == "__main__":
    main()