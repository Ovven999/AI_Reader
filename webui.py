import gradio as gr
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from api_test import slice_gen_audio  # Assuming this is your audio generation function
import scrapper_solution.scrapper as scrapper
import uukanshu.uukanshu_scrapper as uu_scrapper


# Function to extract chapter text from the URL
def extract_chapter_text(book_url, chapter_number):
    # Fetch HTML and extract links
    chapter_text = None
    domain_name = domain_name = urlparse(book_url).netloc
    if (domain_name == 'www.qidian.com'): 
        html = scrapper.fetch_html(book_url)
        links = scrapper.extract_links(html)
        chapter_url = links[chapter_number - 1]

        chapter_text = scrapper.read_specific_chapter_text(chapter_url)

    elif (domain_name == 'www.uukanshu.net'):
        links = uu_scrapper.process_book(book_url)
        chapter_text = uu_scrapper.extract_chapter_text(chapter_number, links)
    return chapter_text

# Function to generate audio from text
def generate_audio(text):
    audio_file = None
    try:
        result = slice_gen_audio(text)
        audio_file = result[1]
    except Exception as e:
        print(e)
    return audio_file

# Create Gradio interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### Book Chapter to Audio Converter")
        
        with gr.Row():
            book_url_input = gr.Textbox(label="Enter book URL")
            chapter_number_input = gr.Number(label="Enter chapter number", step=1)
            submit_button = gr.Button("Generate Audio")

        audio_output = gr.Audio(label="Generated Audio", type="filepath")
        chapter_text_output = gr.Textbox(label="Chapter Text", interactive=False)

        # When button is clicked
        def generate(book_url, chapter_number):
            chapter_text = extract_chapter_text(book_url, int(chapter_number))
            audio_file = generate_audio(chapter_text)
            return audio_file, chapter_text

        submit_button.click(generate, inputs=[book_url_input, chapter_number_input], outputs=[audio_output, chapter_text_output])

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(server_port=7866, enable_queue=False, share=False)
