from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import sys
sys.path.append('../')
import zipfile
import io

from uukanshu.uukanshu_scrapper import process_book
from generate_chapter_content import generate_chapter_content



app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/get-chapters', methods=['GET'])
def get_chapters():
    book_url = request.args.get('url')
    print(book_url)
    # Logic to fetch and process chapters based on book_url
    # For now, let's assume we return a static response

    chapterLinks = process_book(book_url)
    # print(chapterLinks)

    return jsonify({'chapterLinks': chapterLinks})

@app.route('/get-chapter-content', methods=['GET'])
def get_chapter_content():
    chapter_url = request.args.get('url')
    
    # Logic to fetch/generate the text and MP3 files for the given chapter_url
    # Let's assume the files are stored in 'text.txt' and 'audio.mp3'
    text_file_path, audio_file_path = generate_chapter_content(chapter_url)

    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.write(text_file_path, 'chapter_text.txt')
        zip_file.write(audio_file_path, 'chapter_audio.mp3')
    
    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='chapter-content.zip'  # Correct argument for specifying the download file name
    )

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='10.0.0.131', port=5000)
