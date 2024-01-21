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

@Component({
  selector: 'app-music-player',
  templateUrl: './music_player.component.html',
  styleUrls: ['./music_player.component.css'],
})
export class MusicPlayerComponent implements OnInit {
  isDarkMode: boolean = false;
  showModal: boolean = true; // Initially true to show the modal, set to false to hide


  bookLinkSource: string = 'assets/links.txt';
  audioSource: string = 'assets/chapter_audio.mp3';
  textSource: string = 'assets/chapter_text.txt';
  currentTime: number = 0; // Current time in seconds
  duration: number = 0; // Total duration in seconds
  chapterContent: string;
  lrcData: any[] = [];
  
  @ViewChild('audioElement') audioElement: ElementRef;
  isPlaying: boolean = false;

  constructor(
    private http: HttpClient,
    private renderer: Renderer2,
    private cdRef: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.loadChapterContent();
  }

  ngAfterViewInit() {
    const audio = this.audioElement.nativeElement;
    audio.onloadedmetadata = () => {
      this.duration = audio.duration;
    };
    audio.ontimeupdate = () => {
      this.currentTime = audio.currentTime;
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
}
