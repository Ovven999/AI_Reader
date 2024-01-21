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

import { FormGroup, FormControl, Validators } from '@angular/forms';

import JSZip from 'jszip';

interface Chapter {
  name: string;
  url: string;
}

@Component({
  selector: 'app-lyrics',
  templateUrl: './lyrics.component.html',
  styleUrls: ['./lyrics.component.css'],
})
export class LyricsPlayerComponent implements AfterViewInit{
  @ViewChild('audioElement') audioElement: ElementRef;
  backend_url: string = 'http://127.0.0.1:5000'
  // backend_url: string = 'http://10.0.0.131:5000'
  bookUrl: string = '';

  audioSource: string = 'assets/chapter_audio.mp3';
  textSource: string = 'assets/chapter_text.txt';
  bookLinkSource: string = 'assets/links.txt';
  lrcData: any[] = [];
  currentLineIndex: number = 0;
  audio: HTMLAudioElement;

  lyrics = '';

  chapterContent: string;
  chapterLinks: any;
  groupedChapterLinks: any;
  form: FormGroup;
  
  chapter_time_text: string;
  audioUrl: string;

  scrollTimeout: any;
  isAutoScrollEnabled: boolean = true;

  constructor(
    private http: HttpClient,
    private renderer: Renderer2,
    private cdRef: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const lyricsContainer = document.querySelector('.lyrics-container');
    lyricsContainer.addEventListener('scroll', () => {
      this.isAutoScrollEnabled = false;
      clearTimeout(this.scrollTimeout);
      this.scrollTimeout = setTimeout(() => this.enableAutoScroll(), 3000);
    });
  }
  
  ngAfterViewInit(): void {
    // Access the audioElement in ngAfterViewInit
    this.audio = this.audioElement.nativeElement as HTMLAudioElement;
    this.audio.addEventListener('timeupdate', () => {
        // console.log('timeupdate event triggered');
        this.setOffset();
      });
  }

  loadBook(bookUrl: HTMLInputElement) {
    this.bookUrl = bookUrl.value;
    // console.log(this.bookUrl);
  
    const flaskEndpoint = this.backend_url + "/get-chapters";
    this.http.get<{ chapterLinks: { name: string, url: string }[] }>(`${flaskEndpoint}?url=${encodeURIComponent(this.bookUrl)}`).subscribe(
      (response) => {
        const chapters = response.chapterLinks.map(chapter => {
          // Remove characters up to and including the first space in the title
          const firstSpaceIndex = chapter.name.indexOf(' ');
          const cleanedTitle = firstSpaceIndex !== -1 ? chapter.name.substring(firstSpaceIndex + 1) : chapter.name;
          
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

  loadChapterContent() {
    this.http.get(this.textSource, { responseType: 'text' }).subscribe(
      (data) => {
        this.chapterContent = data;
        this.parseLrc(this.chapterContent);
      },
      (error) => {
        console.error('There was an error!', error);
      }
    );
  }

  parseLine(line: string) {
    const parts = line.split(', ');
    if (parts.length !== 2) return null;
  
    const namePart = parts[0].split(': ');
    const urlPart = parts[1].split(': ');
  
    if (namePart.length !== 2 || urlPart.length !== 2) return null;
  
    return { name: namePart[1].trim(), url: urlPart[1].trim() };
  }

  onChapterSelect(chapter: Chapter) {
    console.log(chapter.name + " " + chapter.url);
  
    const flaskEndpoint = this.backend_url + "/get-chapter-content";
    this.http.get(`${flaskEndpoint}?url=${encodeURIComponent(chapter.url)}`, { responseType: 'blob' }).subscribe(
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
  


  parseLrc(lrc: string): void {
    const lines = lrc.split('\n');
    this.lrcData = lines.map((line) => {
      const parts = line.split(']');
      //   console.log(this.parseTime(parts[0].substring(1)))
      //   console.log(parts[1])
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


  findIndex(): number {
    const curTime = this.audio.currentTime;
    // const curTime = this.audio.currentTime;
    // console.log('current time: ' + curTime);
    // console.log('time: ' + this.lrcData[0].time);

    for (let i = 0; i < this.lrcData.length; i++) {
      if (curTime < this.lrcData[0].time) {
        return 0;
      }
      if (
        i > 0 &&
        this.lrcData[i - 1].time < curTime &&
        curTime < this.lrcData[i].time
      ) {
        // console.log('i - 1: ' + this.lrcData[i - 1].time);
        // console.log('cur: ' + curTime);
        // console.log('i: ' + this.lrcData[i].time);
        return i - 1;
      }
    }
    return this.lrcData.length - 1;
  }

  skipTo(time: number) {
    if (this.audioElement && this.audioElement.nativeElement) {
      this.audioElement.nativeElement.currentTime = time;
    }
  }

  setOffset(): void {
    const newIndex = this.findIndex();
    // console.log('current index' + this.currentLineIndex);
    // console.log('new index index' + newIndex);
    if (newIndex !== this.currentLineIndex) {
      this.currentLineIndex = newIndex;
      this.cdRef.detectChanges(); // Detect changes here

      // Now manipulate the DOM
      const lyricsContainer: HTMLElement = this.renderer.selectRootElement(
        '.lyrics-container',
        true
      );
      const currentLyricElement = lyricsContainer.children[
        this.currentLineIndex
      ] as HTMLElement;

      if (currentLyricElement) {
        this.renderer.setStyle(
          lyricsContainer,
          'scrollTop',
          currentLyricElement.offsetTop - lyricsContainer.clientHeight / 2
        );
        Array.from(lyricsContainer.children).forEach((child) =>
          this.renderer.removeClass(child, 'active')
        );
        this.renderer.addClass(currentLyricElement, 'active');
      }
    }
    this.autoScrollToCurrentLine();
  }

  autoScrollToCurrentLine() {
    if (!this.isAutoScrollEnabled) return;

    requestAnimationFrame(() => {
      const activeLineElement = document.querySelector('.lrc-list .active') as HTMLElement;
      const lyricsContainer = document.querySelector('.lyrics-container') as HTMLElement;

      if (activeLineElement && lyricsContainer) {
        const scrollPosition = activeLineElement.offsetTop 
                                - lyricsContainer.offsetTop 
                                - (lyricsContainer.clientHeight / 2) 
                                + (activeLineElement.clientHeight / 2);

        lyricsContainer.scrollTop = scrollPosition;
      }
    });
  }

  enableAutoScroll() {
    this.isAutoScrollEnabled = true;
  }

  playAudio() {
    this.audio.play();
  }
}
