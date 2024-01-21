import win32api
import win32con
import win32gui
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QLineEdit, QHBoxLayout, QScrollArea
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTime, QTimer
import threading
from api_test import slice_gen_audio
import scrapper_solution.scrapper as scrapper
import uukanshu.uukanshu_scrapper as uu_scrapper
from urllib.parse import urlparse
from AudioQueue.audio_queue import AudioQueue

import pythoncom

class MediaKeyListener:
    def __init__(self, on_play_pause):
        self.on_play_pause = on_play_pause

    def listen(self):
        pythoncom.PumpWaitingMessages()
        while True:
            msg = win32gui.GetMessage(None, 0, 0)
            if msg[1][1] == win32con.WM_APPCOMMAND:
                if msg[1][2] == win32con.APPCOMMAND_MEDIA_PLAY_PAUSE:
                    self.on_play_pause()
            win32api.TranslateMessage(msg)
            win32api.DispatchMessage(msg)

class AudioPlayer(QWidget):

    queue = None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.queue = AudioQueue(3)
        self.current_chapter = 1
        self.total_chapters = 0
        self.book_url = None
        self.current_index = 0
        self.chapter_text = None
        self.isFullConnected = False
        self.isLBLConnected = False

        # Set up media key listener
        self.media_key_listener = MediaKeyListener(self.toggle_play_pause)
        listener_thread = threading.Thread(target=self.media_key_listener.listen, daemon=True)
        listener_thread.start()

    def initUI(self):
        self.player = QMediaPlayer()

        # URL Entry
        self.urlLabel = QLabel('Book URL:')
        self.urlEntry = QLineEdit(self)

        # Chapter Number Entry
        self.chapterLabel = QLabel('Chapter Number:')
        self.chapterEntry = QLineEdit(self)

         # Change the Play button to Generate and Play
        self.playButton_lbl= QPushButton('Generate line by line')
        self.playButton_lbl.clicked.connect(self.generateAndPlayAudio_lbl)

        # Change the Play button to Generate and Play
        self.playButton_full = QPushButton('Generate all at once')
        self.playButton_full.clicked.connect(self.generateAndPlayAudio_full)

        # Add a Resume button
        self.resumeButton = QPushButton('play')
        self.resumeButton.clicked.connect(self.resumeAudio)

        # Pause Button
        self.pauseButton = QPushButton('Pause')
        self.pauseButton.clicked.connect(self.pauseAudio)

        # Slider for seeking
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.setAudioPosition)

        # Time labels
        self.currentTimeLabel = QLabel('00:00')
        self.totalTimeLabel = QLabel('00:00')

        # Slider layout
        sliderLayout = QHBoxLayout()
        sliderLayout.addWidget(self.currentTimeLabel)
        sliderLayout.addWidget(self.slider)
        sliderLayout.addWidget(self.totalTimeLabel)

        # Status label
        self.statusLabel = QLabel('Status: Ready')

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.urlLabel)
        layout.addWidget(self.urlEntry)
        layout.addWidget(self.chapterLabel)
        layout.addWidget(self.chapterEntry)
        layout.addWidget(self.playButton_lbl)
        layout.addWidget(self.playButton_full)
        layout.addWidget(self.resumeButton)
        layout.addWidget(self.pauseButton)
        layout.addLayout(sliderLayout)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)
        self.setWindowTitle('Audio Player')
        self.setGeometry(300, 300, 300, 200)

        # Connect signals for updating slider and labels
        self.player.positionChanged.connect(self.updateSliderPosition)
        self.player.durationChanged.connect(self.setSliderRange)

        # Connect signals for updating slider and labels
        self.player.positionChanged.connect(self.updateSliderPosition)
        self.player.durationChanged.connect(self.setSliderRange)

    ##############################play full chapster at once#############################################
    def generateAndPlayAudio_full(self):
        self.current_chapter = 1
        self.total_chapters = 0
        self.book_url = None
        self.current_index = 0

        self.queue = AudioQueue(1)
        if self.isFullConnected == False:
            self.player.mediaStatusChanged.connect(self.onMediaStatusChanged)
            self.isFullConnected = True
        if self.isLBLConnected:
            self.player.mediaStatusChanged.disconnect(self.onMediaStatusChanged_lbl)
            self.isLBLConnected = False
        book_url = self.urlEntry.text()
        self.book_url = book_url
        chapter_number = self.chapterEntry.text()

        self.total_chapters = len(uu_scrapper.process_book(book_url))

        if book_url and chapter_number.isdigit():
            chapter_number = int(chapter_number)
            self.current_chapter = chapter_number
            try:
                self.generateAudioForChapter(book_url, chapter_number)
                QTimer.singleShot(1000, self.playNextInQueue_full)  # Delayed start
            except Exception as e:
                self.statusLabel.setText(f'Error: {str(e)}')
        else:
            self.statusLabel.setText('Please enter a valid URL and chapter number.')
        
    def generateAudioForChapter(self, book_url, chapter_number):
        text = self.extract_chapter_text(book_url, chapter_number)
        self.chapter_text = '\n'.join(text)
        result = slice_gen_audio(text)
        audio_path = result[1]
        self.queue.enqueue(audio_path)
        print(self.queue)
        
    def playNextInQueue_full(self):
        if not self.queue.is_empty():
            # Dequeue and play the current audio
            audio_path = self.queue.dequeue()
            # Increment the current chapter
            self.current_chapter += 1

            # Check if there is a next chapter to prepare
            if self.current_chapter <= self.total_chapters:
                # Use a thread to generate the next chapter's audio without blocking the UI
                threading.Thread(target=self.generateAudioForChapter, args=(self.book_url, self.current_chapter)).start()

            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
            self.player.play()
            self.statusLabel.setText(f'Status: Playing chapter {self.chapter_text}')
            
        else:
            # If the queue is empty, it could be because of the end of the book or some error in generation
            if self.current_chapter > self.total_chapters:
                self.statusLabel.setText('End of the book reached.')
            else:
                self.statusLabel.setText('Waiting for the next chapter audio...')
    ##############################line by line generation###################################
    def generateAndPlayAudio_lbl(self):
        self.queue = AudioQueue(3)
        self.current_chapter = 1
        self.total_chapters = 0
        self.book_url = None
        self.current_index = 0
        # Connect to media status changed signal
        if self.isLBLConnected == False:
            self.player.mediaStatusChanged.connect(self.onMediaStatusChanged_lbl)
            self.isLBLConnected = True
        if self.isFullConnected:
            self.player.mediaStatusChanged.disconnect(self.onMediaStatusChanged)
            self.isFullConnected = False


        book_url = self.urlEntry.text()
        chapter_number = self.chapterEntry.text()

        if book_url and chapter_number.isdigit():
            chapter_number = int(chapter_number)
            try:
                self.text_list = self.extract_chapter_text(book_url, chapter_number)
                self.current_chapter = chapter_number
                self.book_url = book_url
                self.fillQueue()


                # Play the first audio in the queue
                QTimer.singleShot(1000, self.playNextInQueue)
            except Exception as e:
                self.statusLabel.setText(f'Error: {str(e)}')
        else:
            self.statusLabel.setText('Please enter valid URL, chapter number, and starting index.')

    def fillQueue(self):
        while not self.queue.is_full() and self.current_index < len(self.text_list):
            sentence = self.text_list[self.current_index]
            result = slice_gen_audio(sentence)
            audio_path = result[1]
            self.queue.enqueue((audio_path, sentence))
            self.current_index += 1

        # Check if the text list is exhausted and fetch next chapter
        if self.current_index >= len(self.text_list):
            self.current_chapter += 1
            self.text_list = self.extract_chapter_text(self.book_url, self.current_chapter)
            self.current_index = 0

    def playNextInQueue(self):
        if not self.queue.is_empty():
            audio_path, sentence = self.queue.dequeue()
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
            self.player.play()
            self.statusLabel.setText(f'Status: Playing "{sentence}"')

    def onMediaStatusChanged_lbl(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.playNextInQueue()
            if self.queue.is_empty():
                self.fillQueue()
    
    ###############################################################################

    def resumeAudio(self):
        if self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            self.statusLabel.setText('Status: Playing')

    def pauseAudio(self):
        self.player.pause()
        self.statusLabel.setText('Status: Paused')

    def setSliderRange(self, duration):
        self.slider.setRange(0, duration)
        self.totalTimeLabel.setText(self.formatTime(duration))

    def updateSliderPosition(self, position):
        self.slider.blockSignals(True)
        self.slider.setValue(position)
        self.slider.blockSignals(False)
        self.currentTimeLabel.setText(self.formatTime(position))

    def setAudioPosition(self, position):
        self.player.setPosition(position)

    def formatTime(self, ms):
        # Format time from milliseconds to 'mm:ss'
        seconds = int(ms / 1000)
        minutes = int(seconds / 60)
        seconds = seconds % 60
        return f'{minutes:02d}:{seconds:02d}'

    def onMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.playNextInQueue_full()

    def toggle_play_pause(self):
        # Function to toggle between play and pause
        if self.player.state() == QMediaPlayer.PausedState:
            print(1)
            self.player.resumeAudio()
        else:
            print(2)
            self.player.pauseAudio()

    @staticmethod
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioPlayer()
    ex.show()
    sys.exit(app.exec_())
