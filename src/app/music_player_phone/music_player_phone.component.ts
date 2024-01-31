// Component: music_player.component.ts
import { Component } from '@angular/core';

@Component({
  selector: 'app-music-player-phone',
  templateUrl: './music_player_phone.component.html',
  styleUrls: ['./music_player_phone.component.css']
})
export class MusicPlayerPhoneComponent {
    isDarkMode: boolean = false;
    
    toggleDarkMode(): void {
        this.isDarkMode = !this.isDarkMode;
        console.log(this.isDarkMode)
    }


    tumbnailClicked() {
        console.log("tumbnail clicked")
    }
}