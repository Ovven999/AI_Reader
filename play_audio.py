import tkinter as tk
from tkinter import messagebox, font
import pygame
from api_test import slice_gen_audio
import scrapper_solution.scrapper as scrapper
import uukanshu.uukanshu_scrapper as uu_scrapper
from urllib.parse import urlparse

# Initialize pygame mixer
pygame.mixer.init()

# Function to extract chapter text from the URL
def extract_chapter_text(book_url, chapter_number):
    # Fetch HTML and extract links
    chapter_text = None
    domain_name = urlparse(book_url).netloc
    if domain_name == 'www.qidian.com':
        html = scrapper.fetch_html(book_url)
        links = scrapper.extract_links(html)
        chapter_url = links[chapter_number - 1]
        chapter_text = scrapper.read_specific_chapter_text(chapter_url)
    elif domain_name == 'www.uukanshu.net':
        links = uu_scrapper.process_book(book_url)
        chapter_text = uu_scrapper.extract_chapter_text(chapter_number, links)
    return chapter_text

# Function to generate and play audio from text
def play_audio_from_url():
    book_url = url_entry.get()
    chapter_number = int(chapter_entry.get())
    try:
        text = extract_chapter_text(book_url, chapter_number)
        result = slice_gen_audio(text)
        pygame.mixer.music.load(result[1])
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def pause_audio():
    pygame.mixer.music.pause()

def resume_audio():
    pygame.mixer.music.unpause()

def stop_audio():
    pygame.mixer.music.stop()

# Tkinter GUI setup
root = tk.Tk()
root.title("Audio Playback")
root.geometry("400x500")  # Width x Height

# Customizing font and button style
button_font = font.Font(family='Helvetica', size=12, weight='bold')
button_style = {'font': button_font, 'bg': '#4CAF50', 'fg': 'white', 'height': 2, 'width': 15}

# URL entry
tk.Label(root, text="Book URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Chapter number entry
tk.Label(root, text="Chapter Number:").pack()
chapter_entry = tk.Entry(root, width=20)
chapter_entry.pack()

# Play button
play_button = tk.Button(root, text="Play", command=play_audio_from_url, **button_style)
play_button.pack(pady=10)

# Pause button
pause_button = tk.Button(root, text="Pause", command=pause_audio, **button_style)
pause_button.pack(pady=10)

# Resume button
resume_button = tk.Button(root, text="Resume", command=resume_audio, **button_style)
resume_button.pack(pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_audio, **button_style)
stop_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
