import requests
import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Set up directory paths
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
current_dir = os.path.dirname(os.path.abspath(__file__))

headers = {
    'Cookie': '_csrfToken=mCWibSdWoqCzoADJ8nQwPGDtL5a93AeQ6eBAUDEh; newstatisticUUID=1700282693_609696040; supportwebp=true; fu=262768675; qdrs=8%7C10%7C2%7C1%7C3; supportWebp=true; ywguid=120006878504; ywkey=ywGLqTEXjtb0; ywopenid=0900C55E14F861F672F3D2C541B60B23; _gid=GA1.2.801835264.1705300486; traffic_utm_referer=; Hm_lvt_f00f67093ce2f38f215010b699629083=1705300487; trkf=1; qdrsnew=8%7C5%7C2%7C1%7C3; _yep_uuid=3a3c236c-07ea-74d8-c574-9834bc89a64b; e1=%7B%22pid%22%3A%22qd_P_my_bookshelf%22%2C%22eid%22%3A%22qd_M198%22%2C%22l3%22%3A2%2C%22l2%22%3A3%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_P_my_bookshelf%22%2C%22eid%22%3A%22%22%2C%22l3%22%3A2%2C%22l2%22%3A3%2C%22l1%22%3A3%7D; _ga_FZMMH98S83=GS1.1.1705362706.10.1.1705362796.0.0.0; _ga=GA1.1.1237100431.1700282908; _ga_PFYW0QLV3P=GS1.1.1705362706.10.1.1705362796.0.0.0; Hm_lpvt_f00f67093ce2f38f215010b699629083=1705362797',
    'Host': 'www.qidian.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

headers = {
    'Cookie': '_csrfToken=mCWibSdWoqCzoADJ8nQwPGDtL5a93AeQ6eBAUDEh; newstatisticUUID=1700282693_609696040; supportwebp=true; fu=262768675; qdrs=8%7C10%7C2%7C1%7C3; supportWebp=true; ywguid=120006878504; ywkey=ywGLqTEXjtb0; ywopenid=0900C55E14F861F672F3D2C541B60B23; _gid=GA1.2.801835264.1705300486; traffic_utm_referer=; Hm_lvt_f00f67093ce2f38f215010b699629083=1705300487; trkf=1; qdrsnew=8%7C5%7C2%7C1%7C3; _yep_uuid=3a3c236c-07ea-74d8-c574-9834bc89a64b; e1=%7B%22pid%22%3A%22qd_P_my_bookshelf%22%2C%22eid%22%3A%22qd_M198%22%2C%22l3%22%3A2%2C%22l2%22%3A3%2C%22l1%22%3A3%7D; e2=%7B%22pid%22%3A%22qd_P_my_bookshelf%22%2C%22eid%22%3A%22%22%2C%22l3%22%3A2%2C%22l2%22%3A3%2C%22l1%22%3A3%7D; _ga=GA1.1.1237100431.1700282908; _ga_PFYW0QLV3P=GS1.1.1705377999.13.1.1705379403.0.0.0; _ga_FZMMH98S83=GS1.1.1705377999.13.1.1705379403.0.0.0; Hm_lpvt_f00f67093ce2f38f215010b699629083=1705379404',
    'Referer': 'https://www.qidian.com/book/1010426071/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_html(url):
    """Fetch HTML content from a given URL."""
    response = requests.get(url, headers=headers)
    return response.text

def extract_links(html):
    """Extract chapter links from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')
    return [li.a.get('href') for li in soup.find_all('li', class_='chapter-item') if li.a]

def process_chapter(link, save_dir):
    """Process a chapter link: fetch content, extract title and main text, and save to a file."""
    chapter_url = "https:" + link
    html = fetch_html(chapter_url)

    soup = BeautifulSoup(html, 'html.parser')

    # Extract title
    title_content = soup.find('title').get_text(separator='\n', strip=True).split('_')[0].strip() 
    text_content = title_content + '\n'

    # Find and extract main content
    main_content = soup.find('main')
    if main_content:
        text_content += main_content.get_text(separator='\n', strip=True)

    # Save to a file
    save_text_to_file(title_content, text_content, save_dir)

def save_text_to_file(title, text, save_dir):
    """Save the given text to a file in the specified directory."""
    # Ensure the save directory exists, create it if it doesn't
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Construct the file path
    extract_text_file_path = os.path.join(save_dir, title + '.txt')

    # Write the text to the file
    with open(extract_text_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def start_from_chapter(book_url, chapter_number, save_dir):
    """Main function to orchestrate the web scraping process."""
    html = fetch_html(book_url)

    links = extract_links(html)

    for link in links[chapter_number-1:]:
        process_chapter(link, save_dir)

def read_specific_chapter_and_save(book_url, chapter_number, save_dir):
    """Read a specific chapter from the book."""
    html = fetch_html(book_url)

    links = extract_links(html)
    if chapter_number <= len(links):
        process_chapter(links[chapter_number - 1], save_dir)
    else:
        print("Chapter number out of range.")

def read_specific_chapter_text(link):
    """Process a chapter link: fetch content, extract title and main text, and return a string."""
    chapter_url = "https:" + link
    html = fetch_html(chapter_url)

    soup = BeautifulSoup(html, 'html.parser')

    # Extract title
    title_content = soup.find('title').get_text(separator='\n', strip=True).split('_')[0].strip() 
    text_content = title_content + '\n'

    # Find and extract main content
    main_content = soup.find('main')
    if main_content:
        text_content += main_content.get_text(separator='\n', strip=True)

    return text_content

if __name__ == "__main__":
    book_url = 'https://www.qidian.com/book/1027606717/#Catalog'
    save_directory = os.path.join(current_dir, r'../book_chapters/')
    start_from_chapter(book_url, 1, save_directory)