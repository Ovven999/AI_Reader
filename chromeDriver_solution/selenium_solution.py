import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # Corrected import here
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

# this uses selenium to simulate clicks and text input


def extract_text(html_input_path, txt_output_path):
    # Read the HTML file
    with open(html_input_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract title
    title_element = soup.find('h1', class_='title')
    if title_element:
        # Remove any unwanted child elements, such as <span> with data-count
        for child in title_element.find_all():
            child.decompose()
        title = title_element.get_text().strip()
    else:
        title = ""

    # Find all elements with class 'content-text' and extract text
    extracted_text = [element.get_text().strip() for element in soup.find_all('span', class_='content-text')]

    # Prepend the title to the extracted text
    extracted_text.insert(0, title)

    # Join the extracted text
    joined_text = '\n'.join(extracted_text)

    # Write the extracted text to a file
    with open(txt_output_path, 'w', encoding='utf-8') as file:
        file.write(joined_text)

    print(f"Extracted text saved to {txt_output_path}")

current_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = 'cd_scraped_page.html'
html_file_path = os.path.join(current_dir, html_file_path)
extract_text_file_path = 'cd_extracted_text.txt'
extract_text_file_path = os.path.join(current_dir, extract_text_file_path)

# Specify the remote debugging port
debugging_port = "9222"

# Chrome options
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", f"localhost:{debugging_port}")

# Path to chromedriver
driver_path = r"E:\other\chromedriver-win64\chromedriver.exe"

# Set the service
service = Service(executable_path=driver_path)

# Connect to the existing Chrome session
driver = webdriver.Chrome(service=service, options=chrome_options)

# # Now you can control the existing Chrome browser
driver.get('https://www.qidian.com/book/1010426071/')

# Store the ID of the original window
original_window = driver.current_window_handle

time.sleep(2)
chapter_link = driver.find_element(By.LINK_TEXT, "第两百零九章 天选觉醒药剂")
actions = ActionChains(driver)
actions.move_to_element(chapter_link)
actions.click()
actions.perform()

# Wait for the new tab to open
time.sleep(2)

# Switch to the new window/tab
new_window = [window for window in driver.window_handles if window != original_window][0]
driver.switch_to.window(new_window)

time.sleep(2)
html_source = driver.page_source
# Write the HTML to the file
with open(html_file_path, 'w', encoding='utf-8') as file:
    file.write(html_source)
extract_text(html_file_path, extract_text_file_path)

initial_url = driver.current_url
scroll_increment = 50000  # Number of pixels to scroll each time
max_scroll_attempts = 50  # Maximum number of scroll attempts

for _ in range(50):  # Scroll down 20 times (adjust the number as needed)
    pyautogui.scroll(-1000, x=0, y=0)  # Scroll down, specifying x and y coordinates
    # Wait for the page to load content
    time.sleep(1)

    # Check if the URL has changed
    current_url = driver.current_url
    if current_url != initial_url:
        pyautogui.press('f5')
        print(f"URL changed to: {current_url}")
        initial_url = current_url

# You can continue automating actions on the browser...
