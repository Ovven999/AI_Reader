import requests
from bs4 import BeautifulSoup
import sys
import subprocess
import sys
import os

# Add the parent directory to the PYTHONPATH
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from AudioQueue.audio_queue import AudioQueue

headers = {
    "Cookie": "_ga=GA1.1.1918879035.1705345428; _ga_Q66QG7P69Z=GS1.1.1705345428.1.1.1705345437.0.0.0; fcip=111; __gsas=ID=569d81bd092c242b:T=1705463878:RT=1705463878:S=ALNI_MYoOByRAkG2Dk35kAhUxyXf_04Opw; lastread=167729%3D0%3D; ASP.NET_SessionId=nunxe2vqkgpdimyimyea0ctf; _ga_28VWNSC5P8=GS1.1.1705620154.12.1.1705621850.0.0.0",
    "Referer": "https://www.uukanshu.net/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

def get_headers():
    return headers

def get_html_content(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None


def save_to_file(content, file_path):
    with open(file_path, "wb") as file:
        file.write(content)

def save_links_to_file(links, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for link in links:
            file.write(f"name: {link['name']}, url: {link['url']}\n")

def scrape_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    ul_element = soup.find("ul", id="chapterList")
    link_elements = ul_element.find_all("a")
    links = []

    for link_element in link_elements:
        href = link_element["href"]
        title = link_element["title"]
        links.append({"name": title, "url": href})

    links.reverse()
    return links

def scrape_chapter(html_content, chapter_number):
    soup = BeautifulSoup(html_content, "html.parser")
    title_element = soup.find("h1", id="timu")
    title_text = title_element.get_text().strip()
    contentbox = soup.find("div", id="contentbox")
    extracted_content = contentbox.get_text(separator="\n").strip()
    lines = [line.strip() for line in extracted_content.splitlines()]
    extracted_content = "\n".join(lines)
    combined_content = title_text + "\n" + extracted_content.strip()
    output_file_path = f"chapter_{chapter_number}.txt"

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(combined_content)
    return combined_content

def scrape_chapter_as_list(html_content, chapter_number):
    soup = BeautifulSoup(html_content, "html.parser")
    title_element = soup.find("h1", id="timu")
    title_text = title_element.get_text().strip()
    contentbox = soup.find("div", id="contentbox")
    extracted_content = contentbox.get_text(separator="\n").strip()
    lines = [line.strip() for line in extracted_content.splitlines()]
    lines.insert(0, title_text)
    return lines


def process_book(book_url):
    # Specify the URL and scrape book HTML content
    html_content = get_html_content(book_url)

    if html_content:
        save_to_file(html_content, "./web_html.html")

        # Scrape links and save to file
        links = scrape_links(html_content)
        save_links_to_file(links, "links.txt")
    return links


def extract_chapter_text_urlOnly(chapter_url):
    text = None
    chapter_url = headers["Referer"] + chapter_url

    # Scrape chapter content and save to file
    chapter_html_content = get_html_content(chapter_url)
    if chapter_html_content:
        save_to_file(chapter_html_content, "./chapter_html.html")
        text = scrape_chapter_as_list(chapter_html_content, 0)
    return text

def extract_chapter_text(chapter_number, links):
    text = None
    if chapter_number < len(links):
        chapter_url = headers["Referer"] + links[chapter_number]["url"][1:]

        # Scrape chapter content and save to file
        chapter_html_content = get_html_content(chapter_url)
        if chapter_html_content:
            save_to_file(chapter_html_content, "./chapter_html.html")
            text = scrape_chapter_as_list(chapter_html_content, chapter_number)
            # print(
            #     f"Chapter {chapter_number} content saved to chapter_{chapter_number}.txt"
            # )
        else:
            print(f"Chapter {chapter_number} does not exist.")
    return text

def update_postion(queue, text_list, position):
    queue.empty_queue()
    for i in range(position, position+3):
        queue.enqueue(text_list[i])
    

def main():
    # chapter_number = 2000
    if len(sys.argv) != 2:
        print("Usage: python uukanshu_scrapper.py <chapter_number>")
        sys.exit(1)

    chapter_number = int(sys.argv[1])
    book_url = "https://www.uukanshu.net/b/68138/#gsc.tab=0"
    links = process_book(book_url)
    text_list = extract_chapter_text(chapter_number, links)
    
    # queue = AudioQueue(3)
    # list_length = len(text_list)
    # count = 3
    # for i in range(count):
    #     queue.enqueue(text_list[i])
    # while count <= list_length:
    #     print(queue)
    #     update_to_line = input("skip to line: ")
    #     if (update_to_line != ''):
    #         update_to_line = int(update_to_line) - 1
    #         update_postion(queue, text_list, update_to_line)
    #     else:
    #         print("deequeeueed: " + queue.dequeue())
            
    #         queue.enqueue(text_list[count])
    #         count += 1

if __name__ == "__main__":
    main()
