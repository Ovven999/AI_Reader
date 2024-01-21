import sys
sys.path.append('../')
from pydub import AudioSegment

import uukanshu.uukanshu_scrapper as uu_scrapper
from api_test import slice_gen_audio


chapter_number = 55
book_url = 'https://www.uukanshu.net/b/167729/#gsc.tab=0'

links = uu_scrapper.process_book(book_url)
print(links)
chapter_text = uu_scrapper.extract_chapter_text(chapter_number, links)

total_audio = AudioSegment.empty()
total_duration_in_seconds = 0
current_audio_end = '[00:00.00]'
previous_audio_end = '[00:00.00]'

with open('chapter_text.txt', 'w', encoding='utf-8') as file:
    for sentence in chapter_text:
        result = slice_gen_audio(sentence)
        audio_file_path = result[1]

        # Load the audio file
        audio = AudioSegment.from_file(audio_file_path)
        total_audio += audio

        # Get the duration in milliseconds
        duration_in_milliseconds = len(audio)

        # Convert the duration to seconds
        duration_in_seconds = duration_in_milliseconds / 1000

        # Accumulate the duration
        total_duration_in_seconds += duration_in_seconds

        # Convert the total duration to minutes and seconds
        total_minutes = int(total_duration_in_seconds / 60)
        total_seconds = int(total_duration_in_seconds % 60)

        # Format the seconds with two decimal places
        total_seconds_formatted = '{:.2f}'.format(total_seconds)

        current_audio_end = f'[{total_minutes:02}:{total_seconds_formatted}]'

        # Create a line in the desired format
        line = previous_audio_end + sentence
        print(line)

        file.write(line + '\n')

        previous_audio_end = current_audio_end

total_audio.export("chapter_audio.mp3", format="mp3")
