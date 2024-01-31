import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { MusicPlayerComponent } from "./music_player/music_player.component";
import { LyricsPlayerComponent } from "./Lyrics/lyrics.component";
import { MusicPlayerPhoneComponent } from "./music_player_phone/music_player_phone.component";
import { MusicPlayerFasterComponent } from "./music_player_faster/music_player_faster.component";

const routes: Routes = [
    { 
        path: 'default', 
        component: MusicPlayerComponent
    },
    { 
        path: 'demo', 
        component: LyricsPlayerComponent
    },
    { 
        path: 'phone', 
        component: MusicPlayerPhoneComponent
    },
    { 
        path: '', 
        component: MusicPlayerFasterComponent
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRountingModule {

}