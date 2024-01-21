import os
from scrapper_solution import scrapper  # Assuming scrapper is a module in scrapper_solution

current_dir = os.path.dirname(os.path.abspath(__file__))
book_url = 'https://www.qidian.com/book/1010426071/'
chapter_links_file = os.path.join(current_dir, 'chapter_links.txt')

def save_links_to_file(links, filename):
    """Save the links to a text file."""
    with open(filename, 'w', encoding='utf-8') as file:
        for link in links:
            file.write(link + '\n')

def load_links_from_file(filename):
    """Load the links from a text file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

def read_specific_chapter(chapter_number, save_dir):
    """Read a specific chapter from the book."""
    if chapter_number <= len(links):
        scrapper.process_chapter(links[chapter_number - 1], save_dir)
    else:
        print("Chapter number out of range.")

# scrap the whole book
# scrapper.start_from_chapter(book_url, 1, current_dir)

# Check if chapter_links.txt exists
# if os.path.exists(chapter_links_file):
#     # Load links from the file
#     links = load_links_from_file(chapter_links_file)
# else:
#     # Fetch HTML and extract links
#     html = scrapper.fetch_html(book_url)
#     links = scrapper.extract_links(html)
#     # Save the extracted links to a file
#     save_links_to_file(links, chapter_links_file)
        
html = scrapper.fetch_html(book_url)
links = scrapper.extract_links(html)
# Save the extracted links to a file
save_links_to_file(links, chapter_links_file)

chapter_number = 176
chapter_url = links[chapter_number - 1]
chapter_content = scrapper.read_specific_chapter_text(chapter_url)

print(chapter_content)