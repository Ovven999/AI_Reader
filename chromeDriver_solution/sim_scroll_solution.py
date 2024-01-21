import pyautogui

# Simulate scrolling down by moving the mouse wheel quickly
for _ in range(1):  # Scroll down 20 times (adjust the number as needed)
    pyautogui.scroll(-50000, x=0, y=0)  # Scroll down, specifying x and y coordinates


from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service

# Path to chromedriver
driver_path = r"E:\other\chromedriver-win64\chromedriver.exe"
# Path to your ChromeDriver executable
driver_path = r"E:\other\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://www.qidian.com/chapter/1010426071/392456058/")  # Replace with the actual URL

initial_url = driver.current_url
scroll_increment = 100  # Number of pixels to scroll each time
max_scroll_attempts = 50  # Maximum number of scroll attempts

for _ in range(max_scroll_attempts):
    # pyautogui.scroll(-5000, x=0, y=0)  # Scroll down, specifying x and y coordinates
    # Scroll the page
    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
    
    # Wait for the page to load content
    time.sleep(1)

    # Check if the URL has changed
    current_url = driver.current_url
    if current_url != initial_url:
        print(f"URL changed to: {current_url}")
        break

# Perform your actions here

# Close the driver
driver.quit()