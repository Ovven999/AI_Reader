import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_html(url, output_path, driver):
    # Initialize WebDriver and open the page
    driver.get(url)

    # Get the HTML of the page
    html = driver.page_source

    # Close the browser
    driver.quit()

    # Write the HTML to the file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html)

    print(f"HTML saved to {output_path}")

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

def init_webdriver():
    # Path to your ChromeDriver executable
    driver_path = r"E:\other\chromedriver-win64\chromedriver.exe"
    service = Service(driver_path)
    return webdriver.Chrome(service=service)

def scrape_and_extract(url, html_path, text_path):
    driver = init_webdriver()
    get_html(url, html_path, driver)
    extract_text(html_path, text_path)
    driver.quit()

if __name__ == "__main__":
    html_file_path = 'cd_scraped_page.html'
    html_file_path = os.path.join(current_dir, html_file_path)
    extract_text_file_path = 'cd_extracted_text.txt'
    extract_text_file_path = os.path.join(current_dir, extract_text_file_path)

    url = 'https://www.qidian.com/chapter/1010426071/390356888/'

    scrape_and_extract(url, html_file_path, extract_text_file_path)
