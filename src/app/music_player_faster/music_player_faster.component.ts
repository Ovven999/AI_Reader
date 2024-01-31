import {
  Component,
  OnInit,
  AfterViewInit,
  ViewChild,
  ElementRef,
  Renderer2,
  ChangeDetectorRef,
} from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {
  FormGroup,
  FormControl,
  Validators,
  FormsModule,
} from '@angular/forms';

import JSZip from 'jszip';
import { AudioQueue } from '../helper/AudioQueue';

interface Chapter {
  name: string;
  url: string;
}

@Component({
  selector: 'app-music-player-faster',
  templateUrl: './music_player_faster.component.html',
  styleUrls: ['./music_player_faster.component.css'],
})
export class MusicPlayerFasterComponent implements OnInit {
  showContextMenu = false;
  menuPosition = { x: '0px', y: '0px' };
  isDarkMode: boolean = false;
  showModal: boolean = true; // Initially true to show the modal, set to false to hide

  bookLinkSource: string = 'assets/links.txt';
  audioSource: string = 'assets/chapter_audio.mp3';
  textSource: string = 'assets/chapter_text.txt';
  currentTime: number = 0; // Current time in seconds
  currentLine = 0;
  duration: number = 0; // Total duration in seconds
  queue = new AudioQueue<Blob>(3);

  current_chapter: string = '牢底 什么实力';
  chapterContent: string;
  lrcData: any[] = [];
  userScrolled = false;
  autoRecenterEnabled = true;
  isProgrammaticScroll: boolean = false;
  scrollTimeout: any;

  backend_url: string = 'http://127.0.0.1:5000';
  // backend_url: string = 'http://10.0.0.131:5000'
  bookUrl: string = '';
  chapterLinks: any;
  groupedChapterLinks: any;
  form: FormGroup;

  chapter_time_text: string;
  audioUrl: string;
  audio: HTMLAudioElement;

  @ViewChild('audioElement') audioElement: ElementRef;
  @ViewChild('lyricsList') lyricsList: ElementRef;
  isPlaying: boolean = false;

  constructor(
    private http: HttpClient,
    private renderer: Renderer2,
    private cdRef: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.audioUrl = this.audioSource;
    this.loadChapterContent();
  }

  ngAfterViewInit() {
    this.audio = this.audioElement.nativeElement as HTMLAudioElement;
    this.audio.addEventListener('timeupdate', () => {
      // console.log('timeupdate event triggered');
      // this.setOffset();
    });
    this.audio.onloadedmetadata = () => {
      this.duration = this.audio.duration;
    };
    this.audio.ontimeupdate = () => {
      this.currentTime = this.audio.currentTime;
    };
  }

  toggleDarkMode(): void {
    this.isDarkMode = !this.isDarkMode;
    if (this.isDarkMode) {
      document.body.classList.toggle('dark');
    } else {
      document.body.classList.toggle('light');
    }
    console.log(this.duration);
  }

  // ------------------------------------------

  loadBook() {
    console.log(this.bookUrl);

    const flaskEndpoint = this.backend_url + '/get-chapters';
    this.http
      .get<{ chapterLinks: { name: string; url: string }[] }>(
        `${flaskEndpoint}?url=${encodeURIComponent(this.bookUrl)}`
      )
      .subscribe(
        (response) => {
          const chapters = response.chapterLinks.map((chapter) => {
            // Remove characters up to and including the first space in the title
            const firstSpaceIndex = chapter.name.indexOf(' ');
            const cleanedTitle =
              firstSpaceIndex !== -1
                ? chapter.name.substring(firstSpaceIndex + 1)
                : chapter.name;

            return { name: cleanedTitle, url: chapter.url };
          });

          this.chapterLinks = chapters;

          // console.log(chapters); // Processed chapters

          this.groupedChapterLinks = [];
          for (let i = 0; i < chapters.length; i += 3) {
            this.groupedChapterLinks.push(chapters.slice(i, i + 3));
          }
        },
        (error) => {
          console.error('Error fetching chapters:', error);
        }
      );
    return;
  }

  onChapterSelect(chapter: Chapter) {
    console.log(chapter.name + ' ' + chapter.url);

    this.current_chapter = chapter.name;
    const flaskEndpoint = this.backend_url + '/get-chapter-content';
    this.http
      .get(`${flaskEndpoint}?url=${encodeURIComponent(chapter.url)}`, {
        responseType: 'blob',
      })
      .subscribe(
        (response) => {
          const jszip = new JSZip();
          jszip.loadAsync(response).then((zip) => {
            const textFile = zip.file('chapter_text.txt');
            if (textFile) {
              textFile.async('string').then((textContent) => {
                this.chapterContent = textContent;
                // console.log(textContent);
                this.parseLrc(this.chapterContent);
              });
            } else {
              console.error('chapter_text.txt not found in the zip file');
            }

            const audioFile = zip.file('chapter_audio.mp3');
            if (audioFile) {
              audioFile.async('blob').then((audioBlob) => {
                // Handle audio file here
                this.audioUrl = window.URL.createObjectURL(audioBlob);
                // console.log("audioUrl: " + this.audioUrl);
                this.audio.load();
              });
            } else {
              console.error('chapter_audio.mp3 not found in the zip file');
            }
          });
        },
        (error) => {
          console.error('Error downloading chapter content:', error);
        }
      );
    return;
  }

  loadChapterContent() {
    this.http.get(this.textSource, { responseType: 'text' }).subscribe(
      (data) => {
        this.chapterContent = data;
        // console.log(this.chapterContent)
        this.parseLrc(this.chapterContent);
      },
      (error) => {
        console.error('There was an error!', error);
      }
    );
  }

  parseLrc(lrc: string): void {
    const lines = lrc.split('\n');
    this.lrcData = lines.map((line) => {
      const parts = line.split(']');
      // console.log(this.parseTime(parts[0].substring(1)))
      // console.log(parts[1])
      return {
        time: this.parseTime(parts[0].substring(1)),
        words: parts[1],
      };
    });
  }

  parseTime(time: string): number {
    const [minutes, seconds] = time.split(':');
    return parseInt(minutes) * 60 + parseFloat(seconds);
  }

  formatTime(timeInSeconds: number): string {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = Math.floor(timeInSeconds % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  }

  seekAudio() {
    const audio = this.audioElement.nativeElement;
    audio.currentTime = this.currentTime;
  }

  onUserScroll() {
    if (!this.autoRecenterEnabled) return;
    if (this.isProgrammaticScroll) {
      this.isProgrammaticScroll = false;
      return;
    }
    this.userScrolled = true;
    clearTimeout(this.scrollTimeout);
    this.scrollTimeout = setTimeout(() => {
      this.userScrolled = false;
    }, 2000); // 2 seconds delay
  }

  syncLyrics() {
    const currentTime = this.audioElement.nativeElement.currentTime;
    this.currentLine = this.findCurrentLine(currentTime);
    console.log('currentline: ' + this.currentLine);
    if (this.userScrolled) return;
    this.scrollLyrics();
  }

  findCurrentLine(currentTime: number): number {
    return this.lrcData.findIndex((line, index) => {
      return (
        currentTime >= line.time &&
        (index === this.lrcData.length - 1 ||
          currentTime < this.lrcData[index + 1].time)
      );
    });
  }

  scrollLyrics() {
    this.isProgrammaticScroll = true;
    const activeLine = this.lyricsList.nativeElement.children[
      this.currentLine
    ] as HTMLElement;
    // console.log('activeline: ' + activeLine);s
    if (activeLine) {
      const offsetTop = activeLine.offsetTop;
      const lyricsContainer = this.lyricsList.nativeElement.parentElement;
      lyricsContainer.scrollTop = offsetTop - lyricsContainer.offsetTop;
    }
  }
  // ------------------------------------------

  togglePlayPause() {
    const audio = this.audioElement.nativeElement;
    if (this.isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    this.isPlaying = !this.isPlaying;
  }

  toggleModal() {
    this.showModal = !this.showModal;
  }
  // -----------------------------------context menu -----------------------------------------------
  openContextMenu(event: MouseEvent): void {
    event.preventDefault();
    this.showContextMenu = true;

    const menuWidth = 150; // Approximate width of your
    const padding = 10; // Some padding from the edge

    const xPosition =
      event.clientX + menuWidth > window.innerWidth
        ? event.clientX - menuWidth - padding
        : event.clientX;

    this.menuPosition.x = xPosition + 'px';
    this.menuPosition.y = event.clientY + 'px';
  }

  onClick() {
    this.showContextMenu = false;
  }

  generateImg(): void {
    const selectedText = window.getSelection()?.toString();
    if (selectedText == '') {
      console.log('nothing selected!');
      return;
    }
    // Now you can use the selectedText variable as needed
    console.log(selectedText); // For example, log it to the console

    // Further logic using selectedText...
  }

  toggleAutoRecenter(): void {
    this.autoRecenterEnabled = !this.autoRecenterEnabled;
    if (this.autoRecenterEnabled) {
      console.log('auto recenter enabled');
    } else {
      console.log('auto recenter disabled');
    }
  }
}
