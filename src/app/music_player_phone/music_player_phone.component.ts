// Component: music_player.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-music-player',
  templateUrl: './music_player.component.html',
  styleUrls: ['./music_player.component.css']
})
export class MusicPlayerComponent {
    isDarkMode: boolean = false;
    
    toggleDarkMode(): void {
        this.isDarkMode = !this.isDarkMode;
        console.log(this.isDarkMode)
    }


    tumbnailClicked() {
        console.log("tumbnail clicked")
    }
}