import mss
import mss.tools
import time
import pygetwindow as gw
import pyautogui
from PIL import Image
import pytesseract
import os
import glob
import sys
from pathlib import Path

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from api_test import generate_audio

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_images(image_paths, language_code='chi_sim'):  # Use 'chi_tra' for Traditional Chinese
    full_text = ""
    for img_path in image_paths:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img, lang=language_code)
        full_text += "\n" + text  # Add a newline to separate text from different images
    return full_text

def take_screenshot(window_title, output_file='window_screenshot.png'):
    # Find the window
    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        # Restore and activate the window
        window.restore()
        window.activate()

        with mss.mss() as sct:
            decrease_top = 150  # Pixels to decrease from the top
            decrease_sides = 150  # Pixels to decrease from each side (left and right)

            # The screen part to capture
            monitor = {
                "top": window.top + decrease_top,
                "left": window.left + decrease_sides,
                "width": window.width - 2 * decrease_sides,  # Decrease from both left and right
                "height": window.height - decrease_top  # Height is adjusted only for the top decrease
            }
            sct_img = sct.grab(monitor)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_file)
            print("Screenshot taken and saved as window_screenshot.png")
    else:
        print(f"No window with title '{window_title}' found.")

def scroll_window(window_title):
    window = gw.getWindowsWithTitle(window_title)[0]

    if window:
        window.activate()  # Focus the window
        # time.sleep(1)  # Wait a bit for the window to be focused
        # pyautogui.scroll(-100)  # Scroll down
        pyautogui.press('pagedown') # Scroll down
    else:
        print(f"Window titled '{window_title}' not found.")

def get_text():
    pass


count = 0
window_title = "第7章 我信你个鬼 _《我绑架了时间线》小说在线阅读 - 起点中文网 - Google Chrome" 
while gw.getWindowsWithTitle(window_title):
    output_file = f'screenshots\window_screenshot_{count}.png'
    output_file = os.path.join(current_dir, output_file)
    take_screenshot(window_title, output_file=output_file)
    scroll_window(window_title)
    time.sleep(1)
    count += 1


##############extract text from image#################
    
# Path to your screenshots directory
screenshot_directory = os.path.join(current_dir, 'screenshots')

# Construct the search pattern for .png files
search_pattern = os.path.join(screenshot_directory, '*.png')

# Use glob.glob to get all .png files in the directory
image_files = glob.glob(search_pattern)[:-1]

# Extract text and print it
extracted_text = extract_text_from_images(image_files)
print(extracted_text)

# Save the extracted text to a file
output_path = 'ss_extracted_text.txt';
output_path = os.path.join(current_dir, output_path)
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(extracted_text)

# generate_audio(output_path)