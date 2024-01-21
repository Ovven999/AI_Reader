from gradio_client import Client
import simpleaudio as sa
import time
import tkinter as tk
from tkinter import messagebox

client = Client("http://127.0.0.1:7860/")
# client = Client("http://10.0.0.131:7860/")

SDP_Ratio = 0.6
Noise = 0.4
Noise_W = 0.8
Length = 1
sentence_pause = 0.4
paragraph_pause = 1

def gen_audio(text):
    result = client.predict(
            text,	# str  in '输入文本内容' Textbox component
            "芙宁娜",	# str (Option from: [('芙宁娜', '芙宁娜')]) in 'Speaker' Dropdown component
            SDP_Ratio,	# int | float (numeric value between 0 and 1) in 'SDP Ratio' Slider component
            Noise,	# int | float (numeric value between 0.1 and 2) in 'Noise' Slider component
            Noise_W,	# int | float (numeric value between 0.1 and 2) in 'Noise_W' Slider component
            Length,	# int | float (numeric value between 0.1 and 2) in 'Length' Slider component
            "ZH,ZH",	# str (Option from: [('ZH', 'ZH'), ('JP', 'JP'), ('EN', 'EN'), ('mix', 'mix'), ('auto', 'auto')]) in 'Language' Dropdown component
            "",	# str (filepath on your computer (or URL) of file) in 'Audio prompt' Audio component
            "",	# str  in 'Text prompt' Textbox component
            "Text prompt",	# str  in 'Prompt Mode' Radio component
            "",	# str  in '辅助文本' Textbox component
            0,	# int | float (numeric value between 0 and 1) in 'Weight' Slider component
            fn_index=0
    )
    return result

def slice_gen_audio(text):
    result = client.predict(
            text,	# str  in '输入文本内容' Textbox component
            "芙宁娜",	# str (Option from: [('芙宁娜', '芙宁娜')]) in 'Speaker' Dropdown component
            SDP_Ratio,	# int | float (numeric value between 0 and 1) in 'SDP Ratio' Slider component
            Noise,	# int | float (numeric value between 0.1 and 2) in 'Noise' Slider component
            Noise_W,	# int | float (numeric value between 0.1 and 2) in 'Noise_W' Slider component
            Length,	# int | float (numeric value between 0.1 and 2) in 'Length' Slider component
            "ZH,ZH",	# str (Option from: [('ZH', 'ZH'), ('JP', 'JP'), ('EN', 'EN'), ('mix', 'mix'), ('auto', 'auto')]) in 'Language' Dropdown component
            True,	# bool  in '按句切分    在按段落切分的基础上再按句子切分文本' Checkbox component
            paragraph_pause,	# int | float (numeric value between 0 and 10) in '段间停顿(秒)，需要大于句间停顿才有效' Slider component
            sentence_pause,	# int | float (numeric value between 0 and 5) in '句间停顿(秒)，勾选按句切分才生效' Slider component
            "",	# str (filepath on your computer (or URL) of file) in 'Audio prompt' Audio component
            "",	# str  in 'Text prompt' Textbox component
            "",	# str  in '辅助文本' Textbox component
            0,	# int | float (numeric value between 0 and 1) in 'Weight' Slider component
            fn_index=1
    )
    return result

def generate_audio(file_path):
    import pygame
    # Initialize pygame mixer
    pygame.mixer.init()

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    print(text)
    result = slice_gen_audio(text)
    print(result)

    # Load and play the audio file
    pygame.mixer.music.load(result[1])
    pygame.mixer.music.play()

    # Flag to control playback status
    playback_active = True

    # Control loop
    while playback_active:
        command = input("Enter 'pause', 'resume', 'stop', or 'exit': ").strip().lower()

        if command == "pause":
            pygame.mixer.music.pause()
        elif command == "resume":
            pygame.mixer.music.unpause()
        elif command == "stop":
            pygame.mixer.music.stop()
            playback_active = False  # Stop the loop
        elif command == "exit":
            playback_active = False  # Exit the loop without stopping music
        else:
            print("Invalid command. Please enter 'pause', 'resume', 'stop', or 'exit'.")

        time.sleep(0.1)  # Short delay to prevent CPU overuse

    # Optional: Stop the music if exiting the loop
    pygame.mixer.music.stop()

# file_path = 'chapter_55.txt'
# generate_audio(file_path)