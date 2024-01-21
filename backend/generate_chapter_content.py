import sys
sys.path.append('../')
from pydub import AudioSegment

import uukanshu.uukanshu_scrapper as uu_scrapper
from api_test import slice_gen_audio


def generate_chapter_content(chapter_url):
    chapter_text = uu_scrapper.extract_chapter_text_urlOnly(chapter_url)

    total_audio = AudioSegment.empty()
    total_duration_in_seconds = 0
    current_audio_end = '[00:00.00]'
    previous_audio_end = '[00:00.00]'

    text_file_path = './data/chapter_text.txt'
    audio_file_path = './data/chapter_audio.mp3'

    with open(text_file_path, 'w', encoding='utf-8') as file:
        for sentence in chapter_text:
            result = slice_gen_audio(sentence)
            audio_path = result[1]

            # Load the audio file
            audio = AudioSegment.from_file(audio_path)
            total_audio += audio

            # Process duration and write to file
            duration_in_seconds = len(audio) / 1000
            total_duration_in_seconds += duration_in_seconds
            total_minutes, total_seconds = divmod(total_duration_in_seconds, 60)
            current_audio_end = f'[{int(total_minutes):02}:{int(total_seconds):02}.{int(total_seconds % 1 * 100):02}]'
            line = previous_audio_end + sentence
            file.write(line + '\n')
            previous_audio_end = current_audio_end

    total_audio.export(audio_file_path, format="mp3")
    return text_file_path, audio_file_path
